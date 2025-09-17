"""
test_subject_criteria_dev.py

This is a development-only script used to manually test and debug individual
criteria methods from the SubjectSelectionQueryBuilder or MockSelectionBuilder.

It allows developers to:
    - Pass in a specific SubjectSelectionCriteriaKey and value
    - Invoke selection logic (e.g. _add_criteria_* methods)
    - Inspect the resulting SQL fragments using `dump_sql()`

Note:
    This script is intended for local use only and should NOT be committed with
    test content. Add it to your .gitignore after cloning or copying the template.

See Also:
    - mock_selection_builder.py: Test harness for isolated builder method evaluation
    - subject_selection_query_builder.py: The production SQL builder implementation
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
print("PYTHONPATH set to:", sys.path[0])
from tests_utils.query_builder_test_harness.mock_selection_builder import (
    MockSelectionBuilder,
)
from classes.subject_selection_query_builder.subject_selection_criteria_key import (
    SubjectSelectionCriteriaKey,
)


# Helper for mock sequencing
def make_builder(key, value, index=0, comparator="="):
    b = MockSelectionBuilder(key, value, comparator)
    b.criteria_key = key
    b.criteria_key_name = key.name
    b.criteria_value = value
    b.criteria_index = index
    b.criteria_comparator = comparator
    return b


# === Example usage ===
# Replace the examples below with your tests for the method you want to test

# # === Test: DEMOGRAPHICS_TEMPORARY_ADDRESS (yes) ===
# b = make_builder(SubjectSelectionCriteriaKey.DEMOGRAPHICS_TEMPORARY_ADDRESS, "yes")
# b._add_criteria_has_temporary_address()
# print(b.dump_sql())

# # === Test: DEMOGRAPHICS_TEMPORARY_ADDRESS (no) ===
# b = make_builder(SubjectSelectionCriteriaKey.DEMOGRAPHICS_TEMPORARY_ADDRESS, "no")
# b._add_criteria_has_temporary_address()
# print("=== DEMOGRAPHICS_TEMPORARY_ADDRESS (no) ===")
# print(b.dump_sql(), end="\n\n")
