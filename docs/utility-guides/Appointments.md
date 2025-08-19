# Utility Guide: Appointments Utility

This guide explains the purpose and usage of the `setup_appointments` utility found in [`utils/appointments.py`](../../utils/appointments.py).
It is designed to automate the setup of practitioner appointments at a screening centre using Playwright.

---

## Table of Contents

- [Utility Guide: Appointments Utility](#utility-guide-appointments-utility)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Required Arguments](#required-arguments)
  - [How It Works](#how-it-works)
  - [Example Usage](#example-usage)
  - [Best Practices](#best-practices)

---

## Overview

The `setup_appointments` function automates the process of logging in as a Screening Centre Manager, navigating through the appointments workflow, and creating appointment slots for multiple practitioners at a specified screening centre.
It is useful for preparing test data and ensuring practitioners have available appointment slots for test scenarios.

---

## Required Arguments

```python
def setup_appointments(page: Page, no_of_practitioners: int, max: bool = False) -> None:
```

- `page` (`Page`): The Playwright page object.
- `no_of_practitioners` (`int`): Number of practitioners to set up appointments for.
- `max` (`bool`, optional): If `True`, sets up appointments for all practitioners at the site. Defaults to `False`.

---

## How It Works

1. **Login**

   Logs in as "Screening Centre Manager at BCS001" using the `UserTools` utility.

2. **Determine Practitioner Count**

   If `max=True`, navigates to the practitioner availability page, selects the site, and counts the number of practitioners available.

3. **Appointment Setup Loop**

   For each practitioner:
   - Navigates to the practitioner appointments workflow.
   - Selects the site and practitioner.
   - Opens the calendar and selects today's date.
   - Sets start and end times, calculates slots, and saves the appointment for one week.

4. **Logout**

   Logs out after all appointments are set.

---

## Example Usage

```python
from playwright.sync_api import Page
from utils.appointments import setup_appointments

def test_setup_practitioner_appointments(page: Page):
    # Set up appointments for the first 5 practitioners
    setup_appointments(page, no_of_practitioners=5)

def test_setup_all_practitioner_appointments(page: Page):
    # Set up appointments for all practitioners at the site
    setup_appointments(page, no_of_practitioners=0, max=True)
```

---

## Best Practices

- Use this utility in test setup steps to ensure practitioners have available slots before running appointment-related tests.
- Use `max=True` for bulk setup, or specify `no_of_practitioners` for targeted setup.

---
