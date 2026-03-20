
from dissertation_intro_qa.core.sort_utils import sort_defects

def test_deterministic_sort():
    defects = [
        {"code": "B", "severity": "major", "section": "X"},
        {"code": "A", "severity": "critical", "section": "X"},
    ]
    sorted_defects = sort_defects(defects)
    assert sorted_defects[0]["code"] == "A"
