
from dissertation_intro_qa.core.severity import SEVERITY_ORDER

def sort_defects(defects):
    return sorted(
        defects,
        key=lambda d: (
            SEVERITY_ORDER.get(d.get("severity", ""), 99),
            d.get("code", ""),
            d.get("section", ""),
        ),
    )
