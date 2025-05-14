# Utility Guide: Screening Subject Page Searcher

The Screening Subject Search utility allows for

- searching for relevant subjects using their NHS Number, forename, last name, DOB, postcode, episode closed date, status or latest event status
- verifying the subject's event status using their NHS number

## Table of Contents

- [Utility Guide: Screening Subject Page Searcher](#utility-guide-screening-subject-page-searcher)
  - [Table of Contents](#table-of-contents)
  - [Functions Overview](#functions-overview)
    - [The page object parameter](#the-page-object-parameter)
    - [Verify subject event status by NHS no](#verify-subject-event-status-by-nhs-no)
      - [Arguments](#arguments)
      - [How This Function Works](#how-this-function-works)
    - [Search subject by NHS number](#search-subject-by-nhs-number)
      - [Arguments](#arguments-1)
      - [How This Function Works](#how-this-function-works-1)
    - [Search subject by surname](#search-subject-by-surname)
      - [Arguments](#arguments-2)
      - [How This Function Works](#how-this-function-works-2)
    - [Search subject by forename](#search-subject-by-forename)
      - [Arguments](#arguments-3)
      - [How This Function Works](#how-this-function-works-3)
    - [Search subject by date of birth](#search-subject-by-date-of-birth)
      - [Arguments](#arguments-4)
      - [How This Function Works](#how-this-function-works-4)
    - [Search subject by postcode](#search-subject-by-postcode)
      - [Arguments](#arguments-5)
      - [How This Function Works](#how-this-function-works-5)
    - [Search subject by episode closed date](#search-subject-by-episode-closed-date)
      - [Arguments](#arguments-6)
      - [How This Function Works](#how-this-function-works-6)
    - [Search subject by status](#search-subject-by-status)
      - [Arguments](#arguments-7)
      - [How This Function Works](#how-this-function-works-7)
    - [Search subject by latest event status](#search-subject-by-latest-event-status)
      - [Arguments](#arguments-8)
      - [How This Function Works](#how-this-function-works-8)
    - [Search subject by search area](#search-subject-by-search-area)
      - [Required Arguments](#required-arguments)
      - [Optional Arguments](#optional-arguments)
      - [How This Function Works](#how-this-function-works-9)
    - [Check clear filters button works](#check-clear-filters-button-works)
      - [Arguments](#arguments-9)
      - [How This Function Works](#how-this-function-works-10)

## Functions Overview

For this utility we have the following functions:

- `verify_subject_event_status_by_nhs_no`
- `search_subject_by_nhs_number`
- `search_subject_by_surname`
- `search_subject_by_forename`
- `search_subject_by_dob`
- `search_subject_by_postcode`
- `search_subject_by_episode_closed_date`
- `search_subject_by_status`
- `search_subject_by_latest_event_status`
- `search_subject_by_search_area`
- `check_clear_filters_button_works`

### The page object parameter

- Is required for all the listed functions above.
- It is listed as an argument just once to avoid repetition.

### Verify subject event status by NHS no

This is used to check that the latest event status of a subject has been updated to what is expected.
The provided NHS no is used to search the whole database and then verifies the latest event status is as expected.

#### Arguments

- `page`:
  - Type: `Page`
  - This is the playwright page object which is used to tell playwright what page the test is currently on
- `nhs_no`:
  - Type: `str`
  - This is the subject's NHS number. For example: 123 456 7890
- `latest_event_status`:
  - Type: `str`
  - This is the expected status of the subject that is being verified

#### How This Function Works

1. It starts off by navigating to the main menu if not already on this page. This is done to ensure that this can be called from any page
2. Once on the main menu it navigates to the screening subject search page
3. From here it fills in the NHS number filter field with the supplied NHS number and chooses the whole area database as the search area option
4. It then clicks the search button
5. Once the subject is returned, it then verifies that the latest event status matches the supplied event status

### Search subject by NHS number

This searches for a subject by their NHS Number

#### Arguments

- `nhs_no`:
  - Type: `str`
  - This is the subject's NHS number. For example: 123 456 7890

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the NHS number filter field with the supplied NHS number and clicks the search button

### Search subject by surname

This searches for a subject by their surname

#### Arguments

- `surname`:
  - Type: `str`
  - This is the subject's surname

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the surname filter field with the supplied surname and clicks the search button

### Search subject by forename

This searches for a subject by their forename

#### Arguments

- `forename`:
  - Type: `str`
  - This is the subject's forename

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the forename filter field with the supplied forename and clicks the search button

### Search subject by date of birth

This searches for a subject by their date of birth

#### Arguments

- `dob`:
  - Type: `str`
  - This is the subject's date of birth

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the date of birth filter field with the supplied DOB and clicks the search button

### Search subject by postcode

This searches for a subject by their postcode

#### Arguments

- `postcode`:
  - Type: `str`
  - This is the subject's postcode

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the postcode filter field with the supplied postcode and clicks the search button

### Search subject by episode closed date

This searches for a subject by their episode closed date

#### Arguments

- `episode_closed_date`:
  - Type: `str`
  - This is the subject's episode closed date

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then fills in the episode closed date filter field with the supplied date and clicks the search button

### Search subject by status

This searches for a subject by their screening status

#### Arguments

- `status`:
  - Type: `str`
  - This is the subject's screening status

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then selects the screening status option that matches the supplied status and clicks the search button

### Search subject by latest event status

This searches for a subject by their latest event status

#### Arguments

- `status`:
  - Type: `str`
  - This is the subject's latest event status

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then selects the episode status option that matches the supplied status and clicks the search button

### Search subject by search area

This searches for a subject by search area

#### Required Arguments

- `status`:
  - Type: `str`
  - This is the subject's screening status
- `search_area`:
  - Type: `str`
  - This is the search area option to use

#### Optional Arguments

- `code`:
  - Type: `str`
- `gp_practice_code`:
  - Type: `str`

#### How This Function Works

1. It starts off by clicking on the **Clear filters** button to remove any persisting filters
2. It then selects the screening status option that matches the supplied status
3. If provided, the code parameter is used to fill the appropriate code filter field
4. If provided, the GP practice code parameter is used to fill the GP Practice in CCG filter field
5. It then clicks the search button

### Check clear filters button works

This checks that the "clear filter" button works as intended

#### Arguments

- `nhs_no`:
  - Type: `str`
  - This is the subject's NHS number. For example: 123 456 7890

#### How This Function Works

1. It fills in the NHS number filter field with the supplied NHS number and verifies that the NHS number filter field contains the entered value
2. It then clicks the clear filters button and verifies that the NHS number filter field is now empty
