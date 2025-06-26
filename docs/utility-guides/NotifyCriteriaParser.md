# Utility Guide: Notify Criteria Parser

**Source:** [`utils/notify_criteria_parser.py`](../../utils/notify_criteria_parser.py)

The Notify Criteria Parser is a lightweight utility that extracts structured values from compact Notify message criteria strings. It is used by selection builders to support Notify filter logic—like `"S1 - new"` or `"S1 (S1w) - sending"` — by parsing these inputs into cleanly separated parts: `message type`, `message code (optional)`, and `status`.

## Table of Contents

- [Utility Guide: Notify Criteria Parser](#utility-guide-notify-criteria-parser)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Using the Parser](#using-the-parser)
  - [Expected Input Formats](#expected-input-formats)
  - [Example Usage](#example-usage)
  - [Output Structure](#output-structure)
  - [Edge Case: none](#edge-case-none)
  - [Error Handling](#error-handling)
  - [Integration Points](#integration-points)

---

## Overview

Notify message filters are written as short text descriptions like "S1 - new" or "S1 (S1w) - sending".
The parser splits them into meaningful parts so that the system knows what message type to look for, whether there's a specific message code, and the message's status (like "new", "sending", etc). This parser breaks those strings into usable components for SQL query builders.

- `"S1 - new"`
- `"S1 (S1w) - sending"`
- `"none"`

---

## Using the Parser

Import the parser function and give it a string like "S1 (S1w) - sending", and it gives you back each piece of information separately, like the message type, the code (if there is one), and the status.

```python
from utils.notify_criteria_parser import parse_notify_criteria

parts = parse_notify_criteria("S1 (S1w) - sending")
```

## Expected Input Formats

The parser supports the following input patterns:

| Format                    | Meaning                                        |
| ------------------------- | ---------------------------------------------- |
| `Type - status`           | e.g. `"S1 - new"`                              |
| `Type (Code) - status`    | e.g. `"S1 (S1w) - sending"`                    |
| `none` (case-insensitive) | Special case meaning “no message should exist” |

## Example Usage

Here are a few examples of what the parser returns. Think of it like splitting a sentence into parts so each part can be used in a database search:

```python
parse_notify_criteria("S2 (X9) - failed")
# ➜ {'type': 'S2', 'code': 'X9', 'status': 'failed'}

parse_notify_criteria("S1 - new")
# ➜ {'type': 'S1', 'code': None, 'status': 'new'}

parse_notify_criteria("None")
# ➜ {'status': 'none'}
```

## Output Structure

The returned value is a dictionary containing:

```python
{
    "type": str,              # the main message group (like S1 or M1)
    "code": Optional[str],    # the specific version (optional)
    "status": str             # the message’s progress, such as "new", "sending", or "none"
}
```

## Edge Case: none

If someone enters `none` as the criteria, it means "we're looking for subjects who do not have a matching message." The parser handles this specially, and the SQL builder will write `NOT EXISTS` logic behind the scenes to exclude those cases, so the parser returns:

```python
{'status': 'none'}
```

This signals `NOT EXISTS` logic for Notify message filtering.

## Error Handling

If the input doesn’t match an expected pattern, the parser raises:

```python
ValueError("Invalid Notify criteria format: 'your_input'")
```

e.g. If a tester or user types something like `S1 - banana` or forgets the - status bit, the parser will throw an error. This helps catch typos or unsupported formats early.

## Integration Points

These are the parts of the system that use the parser to decide whether to include or exclude Notify messages from a search:
`SubjectSelectionQueryBuilder._add_criteria_notify_queued_message_status()` – for messages currently in the system

`SubjectSelectionQueryBuilder._add_criteria_notify_archived_message_status()` – for messages already sent or stored

You can also reuse it in any other part of the system that needs to interpret Notify message filters.
