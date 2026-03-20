from pathlib import Path

from dissertation_intro_qa.core.config import load_config
from dissertation_intro_qa.core.taxonomy import known_codes, load_taxonomy, severity_floor


def test_load_config(tmp_path: Path):
  path = tmp_path / "config.yaml"
  path.write_text("schema_validation: strict\n", encoding="utf-8")
  cfg = load_config(path)
  assert cfg["schema_validation"] == "strict"


def test_taxonomy_helpers(tmp_path: Path):
  path = tmp_path / "taxonomy.json"
  path.write_text('{"taxonomy_version":"1.0.0","groups":{"GAP":{"GAP-01":{"default_severity_floor":"critical"}}}}', encoding="utf-8")
  tx = load_taxonomy(path)
  assert "GAP-01" in known_codes(tx)
  assert severity_floor(tx, "GAP-01") == "critical"
