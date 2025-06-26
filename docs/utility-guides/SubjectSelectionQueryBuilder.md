# SubjectSelectionQueryBuilder Utility Guide

## Overview

The `SubjectSelectionQueryBuilder` is a flexible utility for constructing SQL queries to retrieve screening subjects from the NHS BCSS Oracle database. It supports a comprehensive set of filters (subject selection criteria) based on:

- Demographics and GP details
- Screening status and due dates
- Events and episodes
- Kit usage and diagnostic activity
- Appointments, tests, and CADS datasets
- Lynch pathway logic and Notify message status

For example:

- NHS number
- Subject age
- Hub code
- Screening centre code
- GP practice linkage
- Screening status
- and many more, (including date-based and status-based filters).

It also handles special cases such as `unchanged` values and supports modifiers like `NOT:` for negation.

Queries are constructed dynamically based on `criteria`, `user`, and `subject` inputs.

---

## How to Use

### Import and Instantiate the Builder

```python
from utils.oracle.subject_selection_query_builder import SubjectSelectionQueryBuilder

builder = SubjectSelectionQueryBuilder()
```

### Build a subject selection query

Using `build_subject_selection_query`:

```python
query, bind_vars = builder.build_subject_selection_query(
    criteria=criteria_dict,     # Dict[str, str] of selection criteria
    user=test_user,             # User object
    subject=test_subject,       # Subject object
    subjects_to_retrieve=100    # Optional limit
)
```

When you call `build_subject_selection_query(...)`, it returns a tuple containing:

`query` — a complete SQL string with placeholders like :nhs_number, ready to be run against the database.

`bind_vars` — a dictionary mapping those placeholders to their actual values, like {"nhs_number": "1234567890"}.

This approach ensures injection-safe execution (defending against SQL injection attacks) and allows database engines to optimize and cache query plans for repeated execution.

## Example Usage

### Input

```python
criteria = {
    "nhs_number": "1234567890",
    "screening_status": "invited"
}

user = User(user_id=42, organisation=None)     # Optional; used for 'unchanged' logic
subject = Subject()                            # Optional; used for 'unchanged' logic

builder = SubjectSelectionQueryBuilder()
query, bind_vars = builder.build_subject_selection_query(criteria, user, subject)
```

### Output

#### Query

```SQL
SELECT ss.screening_subject_id, ...
FROM screening_subject_t ss
INNER JOIN sd_contact_t c ON c.nhs_number = ss.subject_nhs_number
WHERE 1=1
  AND c.nhs_number = :nhs_number
  AND ss.screening_status_id = 1001
FETCH FIRST 1 ROWS ONLY
```

(Note: 1001 would be the resolved ID for "invited" in ScreeningStatusType.)

#### bind_vars

```python
{
    "nhs_number": "1234567890"
}
```

### What happens next?

You can pass both values directly into your DB layer or test stub:

```python
from utils.oracle.oracle import OracleDB
df = OracleDB().execute_query(query, bind_vars)
```

## Supported Inputs

### 1. criteria (Dict[str, str])

This is the main filter configuration, where each entry represents one selection condition.

The `key` is a string matching one of the `SubjectSelectionCriteriaKey` `values` (e.g. "SUBJECT_AGE", "SCREENING_STATUS", etc.)

The `value` is the actual filter (e.g. "55", "> 60", "yes", "not:null", etc.)

Example:

```python
{
  "subject_has_event_status": "ES01",
  "subject_age": "> 60",
  "date_of_death": "null"
}
```

Each of those triggers a different clause in the generated SQL.

### 2. user (User)

This gives the builder context about who’s requesting the query, including their organisation and permissions.

Some criteria (like "USER_HUB" or "USER_ORGANISATION") don’t refer to a fixed hub code, but instead dynamically map to the hub or screening centre of the user running the search. That’s where this comes into play.

Example:

```python
"SUBJECT_HUB_CODE": "USER_HUB"
```

This means “filter by the hub assigned to this user’s organisation,” not a fixed hub like ABC.

### 3. subject (Subject)

This is an optional parameter that provides context about the subject being queried. It’s particularly important for criteria that require comparison against existing values in the database, such as "unchanged" logic.
It allows the builder to determine if a subject's current value matches a previously recorded value.

If you want to filter subjects based on their current screening status, for example, you would need to provide a `Subject` object.
To know if you need to populate an attribute like `screening_status_id`, you can do so by looking if the method requires the Subject class.

For example, if you look at the following code for a screening status, you can see that the Subject class is required.

```python
case SubjectSelectionCriteriaKey.SCREENING_STATUS:
    self._add_criteria_screening_status(subject)
```

You can set attributes on the `Subject` object like this:

```python
subject = Subject()
subject.set_nhs_number("1234567890")
subject.set_screening_status_id(1001)
```

This allows the builder to use the subject's current screening status in the query.

Together, these three inputs give the builder all it needs to translate human-friendly selection criteria into valid, safe, dynamic SQL.

## Key Behavior Details

Values like `yes`, `no`, `null`, `not null`, `unchanged` are normalized and interpreted internally.

`NOT:` prefix in values flips logic where allowed (e.g. "NOT:ES01").

Most enums (like `YesNoType`, `ScreeningStatusType`, etc.) are resolved by description using .by_description() or .by_description_case_insensitive() calls.

Joins to related datasets are added dynamically only when required (e.g. latest episode, diagnostic test joins).

All dates are handled via Oracle `TRUNC(SYSDATE)` and `TO_DATE()` expressions to ensure consistent date logic.

## Reference

For a full list of supported `SubjectSelectionCriteriaKey` values and expected inputs, refer to the enumeration in:

`classes/subject_selection_criteria_key.py`

Or explore the full `SubjectSelectionQueryBuilder._dispatch_criteria_key()` method to review how each key is implemented.
