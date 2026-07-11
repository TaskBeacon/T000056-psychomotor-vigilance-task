from contextlib import nullcontext
from functools import partial
from pathlib import Path

import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import run_trial

MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def run(options: TaskRunOptions):
    """Run the PVT in human, QA, or simulation mode."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None

    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        elif options.mode == "sim":
            participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}
        else:
            subject_data = SubInfo(cfg["subform_config"]).collect()

        settings = TaskSettings.from_dict(cfg["task_config"])
        if output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)
        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        trigger_runtime = (
            initialize_triggers(mock=True)
            if options.mode in ("qa", "sim")
            else initialize_triggers(cfg)
        )
        win, kb = initialize_exp(settings)
        stim_bank = StimBank(win, cfg["stim_config"])
        if options.mode == "human":
            stim_bank = stim_bank.convert_to_voice("instruction_text")
        stim_bank = stim_bank.preload_all()
        settings.save_to_json()

        trigger_runtime.send(settings.triggers.get("exp_onset"))
        instruction = StimUnit(
            "instruction", win, kb, runtime=trigger_runtime
        ).add_stim(stim_bank.get("instruction_text"))
        if options.mode == "human":
            instruction.add_stim(stim_bank.get("instruction_text_voice"))
        instruction.wait_and_continue()

        all_data: list[dict] = []
        for block_idx in range(settings.total_blocks):
            block_id = f"block_{block_idx}"
            (
                BlockUnit(
                    block_id=block_id,
                    block_idx=block_idx,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions()
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(
                        run_trial,
                        stim_bank=stim_bank,
                        trigger_runtime=trigger_runtime,
                        block_id=block_id,
                        block_idx=block_idx,
                    )
                )
                .to_dict(all_data)
            )

        valid_rts = [
            float(row["response_rt"])
            for row in all_data
            if row.get("valid_response") and isinstance(row.get("response_rt"), (int, float))
        ]
        summary = {
            "valid_count": sum(bool(row.get("valid_response")) for row in all_data),
            "lapse_count": sum(bool(row.get("lapse")) for row in all_data),
            "false_start_count": sum(bool(row.get("false_start")) for row in all_data),
            "no_response_count": sum(bool(row.get("no_response")) for row in all_data),
            "mean_rt_ms": (sum(valid_rts) / len(valid_rts) * 1000.0) if valid_rts else 0.0,
        }
        StimUnit("goodbye", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format("good_bye", **summary)
        ).wait_and_continue(terminate=True)

        trigger_runtime.send(settings.triggers.get("exp_end"))
        pd.DataFrame(all_data).to_csv(settings.res_file, index=False)
        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run the Psychomotor Vigilance Task.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
