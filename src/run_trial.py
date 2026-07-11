from __future__ import annotations

from functools import partial

from psyflow import StimUnit, next_trial_id, set_trial_context

from .utils import prepare_dynamic_counter


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    trigger_runtime,
    block_id=None,
    block_idx=None,
):
    """Run one PVT event: random ISI, millisecond counter, and RT feedback."""
    trial_id = next_trial_id()
    condition_label = str(condition)
    block_id_val = str(block_id or "block_0")
    block_idx_val = int(block_idx or 0)
    condition_id = f"{condition_label}_{block_idx_val}_{trial_id}"
    valid_keys = [str(key) for key in settings.key_list]
    response_key_code = {
        key: settings.triggers.get("target_response") for key in valid_keys
    }
    false_start_key_code = {
        key: settings.triggers.get("false_start_response") for key in valid_keys
    }

    trial_data = {
        "trial_id": int(trial_id),
        "block_id": block_id_val,
        "block_idx": block_idx_val,
        "condition": condition_label,
        "condition_id": condition_id,
        "responded": False,
        "valid_response": False,
        "false_start": False,
        "lapse": False,
        "no_response": False,
        "response_key": "",
        "response_rt": None,
        "outcome": "pending",
    }
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)
    isi_duration = list(settings.isi_duration)
    isi = make_unit(unit_label="isi").add_stim(stim_bank.get("blank_screen"))
    set_trial_context(
        isi,
        trial_id=trial_id,
        phase="isi",
        deadline_s=max(float(value) for value in isi_duration),
        valid_keys=valid_keys,
        block_id=block_id_val,
        condition_id=condition_id,
        task_factors={"stage": "isi", "condition": condition_label},
        stim_id="blank_screen",
    )
    isi.capture_response(
        keys=valid_keys,
        duration=isi_duration,
        onset_trigger=settings.triggers.get("isi_onset"),
        response_trigger=false_start_key_code,
        terminate_on_response=True,
    ).to_dict(trial_data)

    premature_key = isi.get_state("response", None)
    if premature_key is not None:
        trial_data.update(
            responded=True,
            false_start=True,
            response_key=str(premature_key),
            false_start_rt=isi.get_state("rt", None),
            outcome="false_start",
        )
        return trial_data

    counter = prepare_dynamic_counter(stim_bank.get("target_counter"))
    response_window = float(settings.response_window_duration)
    target = make_unit(unit_label="target").add_stim(counter)
    set_trial_context(
        target,
        trial_id=trial_id,
        phase="target",
        deadline_s=response_window,
        valid_keys=valid_keys,
        block_id=block_id_val,
        condition_id=condition_id,
        task_factors={"stage": "target", "condition": condition_label},
        stim_id="target_counter",
    )
    target.capture_response(
        keys=valid_keys,
        duration=response_window,
        onset_trigger=settings.triggers.get("target_onset"),
        response_trigger=response_key_code,
        timeout_trigger=settings.triggers.get("target_timeout"),
    ).to_dict(trial_data)

    response_key = target.get_state("response", None)
    response_rt = target.get_state("rt", None)
    if response_key is None or not isinstance(response_rt, (int, float)):
        trial_data.update(no_response=True, outcome="no_response")
        return trial_data

    response_rt = float(response_rt)
    false_start = response_rt < float(settings.false_start_threshold)
    lapse = response_rt > float(settings.lapse_threshold)
    trial_data.update(
        responded=True,
        valid_response=not false_start,
        false_start=false_start,
        lapse=bool(lapse and not false_start),
        response_key=str(response_key),
        response_rt=response_rt,
        response_rt_ms=int(round(response_rt * 1000.0)),
        outcome="false_start" if false_start else ("lapse" if lapse else "valid_response"),
    )

    if false_start:
        return trial_data

    feedback_duration = float(settings.feedback_duration)
    feedback = make_unit(unit_label="feedback").add_stim(
        stim_bank.get_and_format("rt_feedback", rt_ms=trial_data["response_rt_ms"])
    )
    set_trial_context(
        feedback,
        trial_id=trial_id,
        phase="feedback",
        deadline_s=feedback_duration,
        valid_keys=[],
        block_id=block_id_val,
        condition_id=condition_id,
        task_factors={
            "stage": "feedback",
            "condition": condition_label,
            "lapse": bool(trial_data["lapse"]),
        },
        stim_id="rt_feedback",
    )
    feedback.show(
        duration=feedback_duration,
        onset_trigger=settings.triggers.get("feedback_onset"),
    ).to_dict(trial_data)
    return trial_data
