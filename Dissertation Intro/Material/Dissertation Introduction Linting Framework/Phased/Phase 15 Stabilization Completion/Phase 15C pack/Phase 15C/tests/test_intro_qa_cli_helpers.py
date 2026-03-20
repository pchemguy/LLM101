from dissertation_intro_qa.cli.intro_qa import generate_repair_plan, run_gate


def test_generate_repair_plan():
  report = {
      "defects": [
          {
              "code": "GAP-02",
              "severity": "major",
              "section": "Gap",
              "description": "desc",
              "evidence": "evi",
              "recommendation": "rec",
          }
      ]
  }
  text = generate_repair_plan(report)
  assert "GAP-02" in text


def test_run_gate():
  report = {
      "summary": {"critical_count": 0, "major_count": 0},
      "scores": {"SC1": 2},
      "gost_compliance": {"relevance": True},
  }
  cfg = {"profiles": {"strict": {"max_critical": 0, "max_major": 0, "min_scores": {"SC1": 2}, "require_gost": ["relevance"]}}}
  out = run_gate(report, cfg, "strict")
  assert out["passed"] is True
