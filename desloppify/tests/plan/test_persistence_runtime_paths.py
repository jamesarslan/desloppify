"""Regression tests for runtime-aware plan persistence defaults."""

from __future__ import annotations

from desloppify.base.runtime_state import RuntimeContext, runtime_scope
import desloppify.engine._plan.persistence as persistence_mod
from desloppify.engine._plan.schema import empty_plan


def test_plan_persistence_defaults_follow_runtime_project_root(tmp_path):
    plan = empty_plan()
    plan["queue_order"] = ["review::a.py::issue-1"]

    ctx = RuntimeContext(project_root=tmp_path)
    with runtime_scope(ctx):
        persistence_mod.save_plan(plan)
        loaded = persistence_mod.load_plan()

    expected = tmp_path / ".desloppify" / "plan.json"
    assert expected.exists()
    assert loaded["queue_order"] == ["review::a.py::issue-1"]


def test_plan_persistence_honors_monkeypatched_plan_file(monkeypatch, tmp_path):
    custom_plan_file = tmp_path / "custom" / "plan.json"
    monkeypatch.setattr(persistence_mod, "PLAN_FILE", custom_plan_file)

    plan = empty_plan()
    plan["queue_order"] = ["review::b.py::issue-2"]
    persistence_mod.save_plan(plan)
    loaded = persistence_mod.load_plan()

    assert custom_plan_file.exists()
    assert loaded["queue_order"] == ["review::b.py::issue-2"]
