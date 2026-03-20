from pathlib import Path

from dissertation_intro_qa.cli.benchmark_packager import bootstrap_project, build_demo_pipeline_plan


def test_bootstrap_project(tmp_path: Path):
  result = bootstrap_project(tmp_path / "proj")
  assert result["status"] == "ok"
  assert (tmp_path / "proj" / "benchmark").exists()


def test_demo_pipeline_plan(tmp_path: Path):
  plan = build_demo_pipeline_plan(tmp_path)
  assert plan["project_root"] == str(tmp_path)
  assert len(plan["steps"]) >= 1
