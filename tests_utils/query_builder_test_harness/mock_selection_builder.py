# mock_selection_builder.py — Development-only testing harness for criteria logic
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from classes.selection_builder_exception import SelectionBuilderException
from classes.subject_selection_criteria_key import SubjectSelectionCriteriaKey

# ------------------------------------------------------------------------
# 🧰 Stubbed Data Classes (for symbolic mapping or subject context)
# ------------------------------------------------------------------------


class Subject:
    def __init__(self, lynch_due_date_change_reason_id):
        self.lynch_due_date_change_reason_id = lynch_due_date_change_reason_id


# ------------------------------------------------------------------------
# 🧪 Enum-Like Mocks (for symbolic value resolution)
# ------------------------------------------------------------------------


class NotifyEventStatus:
    _label_to_id = {
        "S1": 9901,
        "S2": 9902,
        "M1": 9903,
        # Extend as needed
    }

    @classmethod
    def get_id(cls, description: str) -> int:
        key = description.strip().upper()
        if key not in cls._label_to_id:
            raise ValueError(f"Unknown Notify event type: '{description}'")
        return cls._label_to_id[key]


class YesNoType:
    YES = "yes"
    NO = "no"

    _valid = {YES, NO}

    @classmethod
    def from_description(cls, description: str) -> str:
        key = description.strip().lower()
        if key not in cls._valid:
            raise ValueError(f"Expected 'yes' or 'no', got: '{description}'")
        return key


# ------------------------------------------------------------------------
# 🧠 Utility Functions (reused parsing helpers)
# ------------------------------------------------------------------------


def parse_notify_criteria(criteria: str) -> dict:
    """
    Parses criteria strings like 'S1 - new' or 'S1 (S1w) - sending' into parts.
    """
    criteria = criteria.strip()
    if criteria.lower() == "none":
        return {"status": "none"}

    pattern = r"^(?P<type>[^\s(]+)(?:\s+\((?P<code>[^)]+)\))?\s*-\s*(?P<status>\w+)$"
    match = re.match(pattern, criteria, re.IGNORECASE)
    if not match:
        raise ValueError(f"Invalid Notify criteria format: '{criteria}'")

    return {
        "type": match.group("type"),
        "code": match.group("code"),
        "status": match.group("status").lower(),
    }


# ------------------------------------------------------------------------
# 🧪 Mock Query Builder Scaffolding (extend with testable methods)
# ------------------------------------------------------------------------
class MockSelectionBuilder:
    """
    Lightweight test harness that mimics SubjectSelectionQueryBuilder behavior.

    This class is used for local testing of SQL fragment builder methods without requiring
    the full application context. Developers can reimplement individual _add_criteria_*
    methods here for isolated evaluation.

    Usage:
        - Add your _add_criteria_* method to this class
        - Then create tests in utils/oracle/test_subject_criteria_dev.py to run it
        - Use dump_sql() to inspect the generated SQL fragment
    """

    def __init__(self, criteria_key, criteria_value, criteria_comparator=">="):
        self.criteria_key = criteria_key
        self.criteria_key_name = criteria_key.description
        self.criteria_value = criteria_value
        self.criteria_comparator = criteria_comparator
        self.criteria_index: int = 0
        self.sql_where = []
        self.sql_from = []

    # ------------------------------------------------------------------------
    # 🖨️ SQL Inspection Utility (used to inspect the SQL fragments - do not remove)
    # ------------------------------------------------------------------------
    def dump_sql(self):
        parts = []

        if self.sql_from:
            parts.append("-- FROM clause --")
            parts.extend(self.sql_from)

        if self.sql_where:
            parts.append("-- WHERE clause --")
            parts.extend(self.sql_where)

        return "\n".join(parts)

    # ------------------------------------------------------------------------
    # 🔌 Required Internal Stubs (builder compatibility - do not remove)
    # ------------------------------------------------------------------------
    def _add_join_to_latest_episode(self) -> None:
        """
        Mock stub for adding latest episode join. No-op for test harness.
        """
        self.sql_from.append("-- JOIN to latest episode placeholder")

    def _force_not_modifier_is_invalid(self):
        # Placeholder for rule enforcement. No-op in mock builder.
        pass

    def _dataset_source_for_criteria_key(self) -> dict:
        """
        Maps criteria key to dataset table and alias.
        """
        key = self.criteria_key
        if key == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_CANCER_AUDIT_DATASET:
            return {"table": "ds_cancer_audit_t", "alias": "cads"}
        if (
            key
            == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_COLONOSCOPY_ASSESSMENT_DATASET
        ):
            return {"table": "ds_patient_assessment_t", "alias": "dspa"}
        if key == SubjectSelectionCriteriaKey.LATEST_EPISODE_HAS_MDT_DATASET:
            return {"table": "ds_mdt_t", "alias": "mdt"}
        raise SelectionBuilderException(self.criteria_key_name, self.criteria_value)

    def _add_join_to_surveillance_review(self):
        self.sql_from.append("-- JOIN to surveillance review placeholder")


# ------------------------------------------------------------------------
# 🧪 Add Your Custom _add_criteria_* Test Methods Below
# ------------------------------------------------------------------------
# e.g., def _add_criteria_example_filter(self): ...
# then use utils/oracle/test_subject_criteria_dev.py to run your scenarios
