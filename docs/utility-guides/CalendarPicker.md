# Utility Guide: Calendar Picker

The Calendar Picker utility allows us to use the different calendar pickers available on BCSS to select a date.

## Table of Contents
<!-- vale off -->
- [Utility Guide: Calendar Picker](#utility-guide-calendar-picker)
  - [Table of Contents](#table-of-contents)
  - [Functions Overview](#functions-overview)
    - [Calendar Picker ddmmyyyy](#calendar-picker-ddmmyyyy)
      - [Required Arguments](#required-arguments)
      - [How This Function Works](#how-this-function-works)
    - [Calendar Picker ddmonyy](#calendar-picker-ddmonyy)
      - [Required Arguments](#required-arguments-1)
      - [How This Function Works](#how-this-function-works-1)
    - [V1 Calendar Picker](#v1-calendar-picker)
      - [Required Arguments](#required-arguments-2)
      - [How This Function Works](#how-this-function-works-2)
    - [Calculate Years and Months to Traverse](#calculate-years-and-months-to-traverse)
      - [Required Arguments](#required-arguments-3)
      - [Returns](#returns)
      - [How This Function Works](#how-this-function-works-3)
    - [Traverse Years In V1 Calendar Picker](#traverse-years-in-v1-calendar-picker)
      - [Required Arguments](#required-arguments-4)
      - [How This Function Works](#how-this-function-works-4)
    - [Traverse Months In V1 Calendar Picker](#traverse-months-in-v1-calendar-picker)
      - [Required Arguments](#required-arguments-5)
      - [How This Function Works](#how-this-function-works-5)
    - [V2 Calendar Picker](#v2-calendar-picker)
      - [Required Arguments](#required-arguments-6)
      - [How This Function Works](#how-this-function-works-6)
    - [Calculate V2 Calendar Variables](#calculate-v2-calendar-variables)
      - [Required Arguments](#required-arguments-7)
      - [Returns](#returns-1)
      - [How This Function Works](#how-this-function-works-7)
    - [V2 Calendar Picker Traverse Back](#v2-calendar-picker-traverse-back)
      - [Required Arguments](#required-arguments-8)
      - [Returns](#returns-2)
      - [How This Function Works](#how-this-function-works-8)
    - [V2 Calendar Picker Traverse Forward](#v2-calendar-picker-traverse-forward)
      - [Required Arguments](#required-arguments-9)
      - [How This Function Works](#how-this-function-works-9)
    - [Select Day](#select-day)
      - [Required Arguments](#required-arguments-10)
      - [How This Function Works](#how-this-function-works-10)
    - [Book First Eligible Appointment](#book-first-eligible-appointment)
      - [Required Arguments](#required-arguments-11)
      - [How This Function Works](#how-this-function-works-11)
    - [Book Appointments Go To Month](#book-appointments-go-to-month)
      - [Required Arguments](#required-arguments-12)
      - [How This Function Works](#how-this-function-works-12)
    - [Check For Eligible Appointment Dates](#check-for-eligible-appointment-dates)
      - [Required Arguments](#required-arguments-13)
      - [How This Function Works](#how-this-function-works-13)
<!-- vale on -->
## Functions Overview

For this utility we have the following methods:
<!-- vale off -->
- `calendar_picker_ddmmyyyy`
- `calendar_picker_ddmonyy`
- `v1_calender_picker`
  - `calculate_years_and_months_to_traverse`
  - `traverse_years_in_v1_calendar`
  - `traverse_months_in_v1_calendar`
- `v2_calendar_picker`
  - `calculate_v2_calendar_variables`
  - `v2_calendar_picker_traverse_back`
  - `v2_calendar_picker_traverse_forward`
- `select_day`
- `book_first_eligible_appointment`
  - `book_appointments_go_to_month`
  - `check_for_eligible_appointment_dates`

### Calendar Picker ddmmyyyy
<!-- vale on -->
This is called to enter a date in the correct format for the V1 calendar picker.
You provide a date and a playwright locator and it will enter the date in the format `dd/mm/yyyy` (e.g. 16/01/2025).

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to enter
- `locator`:
  - Type: `Locator`
  - This is the locator for the field you want to enter the date into

#### How This Function Works

1. This calls the `format_date` method from DateTimeUtils to get the date in the correct format.
2. Once the date is formatted correctly it enters it into the provided locator.
<!-- vale off -->
### Calendar Picker ddmonyy
<!-- vale on -->
This is called to enter a date in the correct format for the V2 calendar picker.
You provide a date and a playwright locator and it will enter the date in the format `dd month yy` (e.g. 16 Jan 25).

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to enter
- `locator`:
  - Type: `Locator`
  - This is the locator for the field you want to enter the date into

#### How This Function Works

1. This calls the `format_date` method from DateTimeUtils to get the date in the correct format.
   1. As the formatting for the `datetime` function differs between operating systems, there is a check first to see what OS is in use.
   2. From here it calls the correct formatting option.
2. Once the date is formatted correctly it enters it into the provided locator.

### V1 Calendar Picker

This is called to select a date from the V1 calendar picker, which can be seen on the Subject Screening Search page.

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to enter

#### How This Function Works

1. This starts of by getting the current date that the calendar picker is on and storing it in a variable: `current_date`.
2. Once that is done it calls the `calculate_years_and_months_to_traverse` method to know how many times to click each button to increase/decrease the years or months, and stores them in: `years_to_traverse` and `months_to_traverse`.
3. Once we know how many times each button needs to be clicked we call the method: `traverse_years_in_v1_calendar`.
4. After the correct year is selected we call the `traverse_months_in_v1_calendar` method to get to the correct month.
5. Finally, after the correct year and month is displayed we call the `select_day` method.

### Calculate Years and Months to Traverse

This is called to calculate how many times we need to click on the next/prev year and month buttons.

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to enter
- `current_date`:
  - Type: `datetime`
  - This is the date the calendar picker is currently on

#### Returns

- `years_to_traverse`:
  - Type: `int`
  - This is the number of years we need to traverse
- `months_to_traverse`:
  - Type: `int`
  - This is the number of months we need to traverse

#### How This Function Works

1. It converts both dates into just the year as an integer using the DateTimeUtils and subtracts the date from the current year. It then stores the result in `years_to_traverse`
2. The same is done for the months and the result of that calculation is stores in `months_to_traverse`

### Traverse Years In V1 Calendar Picker

This is called to move the V1 calendar picker to the correct year

#### Required Arguments

- `years_to_traverse`:
  - Type: `int`
  - This is the number of years to traverse

#### How This Function Works

1. If `years_to_traverse` is negative, it multiplies it by -1 and runs a `FOR` loop for the value of this variable.
   1. For each iteration of the loop it clicks on the previous year button: `«`
2. If `years_to_traverse` is positive, it runs a `FOR` loop for the value of this variable.
   1. For each iteration of the loop it clicks on the next year button: `»`

### Traverse Months In V1 Calendar Picker

This is called to move the V1 calendar picker to the correct month.

#### Required Arguments

- `months_to_traverse`:
  - Type: `int`
  - This is the number of months to traverse

#### How This Function Works

1. If `months_to_traverse` is negative, it multiplies it by -1 and runs a `FOR` loop for the value of this variable.
   1. For each iteration of the loop it clicks on the previous month button: `‹`
2. If `months_to_traverse` is positive, it runs a `FOR` loop for the value of this variable.
   1. For each iteration of the loop it clicks on the next month button: `›`

### V2 Calendar Picker

This is called to select a date using the V2 calendar picker, which can be seen on the Active Batch List page.

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to select.

#### How This Function Works

1. Firstly it stores the current date in a variable: `current_date`.
2. Then `current_date` and `date` are passed onto the `calculate_v2_calendar_variables` method to calculate the necessary variables to traverse this calendar.
3. Once these variable have been calculated we call the `v2_calendar_picker_traverse_back` method to "go back in time" an expand the view of available years.
4. After we have traversed far back enough to be able to select the years we want, we call the `v2_calendar_picker_traverse_forward` method which will take us to the year and month we want to go to.
5. Finally we call the `select_day` method to select the correct day from the calendar picker.

### Calculate V2 Calendar Variables

This is called to calculate all, of the variables needed to traverse the V2 calendar picker.

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date you want to select.
- `current_date`:
  - Type: `datetime`
  - This is todays date.

#### Returns

- `current_month_long`:
  - Type: `str`
  - This is the current month as a string: *June* / *April*
- `month_long`:
  - Type: `str`
  - This is the month we want to go to as a string: *June* / *April*
- `month_short`:
  - Type: `str`
  - This is the month we want to go to as a shorter string: *Jun* / *Apr*
- `current_year`:
  - Type: `int`
  - This is the current year as an integer in `yyyy` format: *2025*
- `year`:
  - Type: `int`
  - This is the year we want to go to as an integer in `yyyy` format: *1996*
- `current_decade`:
  - Type: `int`
  - This is the current decade we are in: *2020*
- `decade`:
  - Type: `int`
  - This is the decade of the date we want to go to: *1990*
- `current_century`:
  - Type: `int`
  - This is the current century we are in: *2000*
- `century`:
- Type: `int`
  - This is the century of the date we want to go to: *1900*

#### How This Function Works

1. It first calculates `current_month_long`.
   1. This is done by calling the `format_date` method from DateTimeUtils passing along the format string: `"%B"`.
2. Next we calculate `current_year`.
   1. This is done by calling the `format_date` method from DateTimeUtils passing along the format string: `"%Y"`.
3. Then we calculate `current_century`.
   1. This is done by dividing `current_year` by 100 and then multiplying it by 100 to remove the integers at the end.
   2. E.g. 2025 // 100 = 20
   3. 20 * 100 = 2000
4. After we calculate `current_decade`.
   1. This is achieved by subtracting `current_century` from `current_year`, then dividing the result by 10 and multiplying that by 10. Finally we add this result back to `current_century`.
   2. E.g. 2025 - 2000 = 25
   3. 25 // 10 = 2
   4. 2 * 10 = 20
   5. 20 + 2000 = 2020
5. Next we calculate `year`, `century`, `decade`, `month_short` and `month_long` in similar methods to above.
6. Once all of these have been calculated, we return these variables.

### V2 Calendar Picker Traverse Back

This is called to "go back" in the V2 calendar picker. It expands the scope of available years to select which makes traversing this calendar quicker if we need to select a date many years in the future or past.

#### Required Arguments

- `current_month_long`:
  - Type: `str`
  - This is current month as a string: *April*
- `month_long`:
  - Type: `str`
  - This is the month we want to select as a string: *June*
- `current_year`:
  - Type: `int`
  - This is the current year as an integer in `yyyy` format: *2025*
- `year`:
  - Type: `int`
  - This is the year of the date we want to select as an integer in `yyyy` format: *1996*
- `current_decade`
  - Type: `int`
  - This is the current decade we are in: *2020*
- `decade`
  - Type: `int`
  - This is the decade of the date we want to select: *1990*
- `current_century`
  - Type: `int`
  - This is the current century we are in: *2000*
- `century`
  - Type: `int`
  - This is the century of the date we want to select: *1900*

#### Returns

- `click_month`
  - Type: `bool`
  - This is True/False depending on how far back we traverse.
- `click_year`
  - Type: `bool`
  - This is True/False depending on how far back we traverse.
- `click_decade`
  - Type: `bool`
  - This is True/False depending on how far back we traverse.
- `click_century`
  - Type: `bool`
  - This is True/False depending on how far back we traverse.

#### How This Function Works

1. Firstly it checks if `current_month_long` matches `month_long`.
   1. If it does not then it clicks on the picker switch button to traverse back.
   2. Then it sets `click_month` to `True`.
2. Then it checks if `current_year` matches `year`.
   1. If it does not then it clicks on the picker switch button to traverse back.
   2. Then it sets `click_year` to `True`.
3. Next it checks if `current_decade` matches `decade`
   1. If it does not then it clicks on the picker switch button to traverse back.
   2. Then it sets `click_decade` to `True`.
4. After it checks if `current_century` matches `century`.
   1. If it does not then it clicks on the picker switch button to traverse back.
   2. Then it sets `click_century` to `True`.
5. Finally it returns `click_month`, `click_year`, `click_decade` and `click_century`.

### V2 Calendar Picker Traverse Forward

This is called to narrow down the scope of available years on the V2 calendar picker and eventually end up on the year and month we want to select.

#### Required Arguments

- `click_month`:
  - Type: `bool`
  - This contains either `True` or `False` depending on the result from `v2_calendar_picker_traverse_back`.
- `click_year`:
  - Type: `bool`
  - This contains either `True` or `False` depending on the result from `v2_calendar_picker_traverse_back`.
- `click_decade`:
  - Type: `bool`
  - This contains either `True` or `False` depending on the result from `v2_calendar_picker_traverse_back`.
- `click_century`:
  - Type: `bool`
  - This contains either `True` or `False` depending on the result from `v2_calendar_picker_traverse_back`.
- `century`
  - Type: `str`
  - This contains the century we want to select as a string: *1900*
- `decade`
  - Type: `str`
  - This contains the decade we want to select as a string: *1990*
- `year`
  - Type: `year`
  - This contains the year we want to select as a string: *1996*
- `month_short`
  - Type: `str`
  - This contains the month we want to select as a string: *Jun*

#### How This Function Works

1. Firstly it checks if `click_century` is set to `True`.
   1. If it is then it clicks on the cell that contains the string `century`.
2. Then it checks if `click_decade` is set to `True`.
   1. If it is then it clicks on the cell that contains the string `decade`.
3. Next it checks if `click_year` is set to `True`.
   1. If it is then it clicks on the cell that contains the string `year`.
4. Finally it checks if `click_month` is set to `True`.
   1. If it is then it clicks on the cell that contains the string `month_short`.

### Select Day

This is called to select the day of the date we want the calendar picker to go to.

#### Required Arguments

- `date`:
  - Type: `datetime`
  - This is the date we want to select.

#### How This Function Works

1. First it checks what operating system is running.
   1. If Windows is found then it calls the `format_date` method from DateTimeUtils and passes the formatting string `"%#d"`.
   2. Otherwise it calls the `format_date` method from DateTimeUtils and passes the formatting string `"%-d"`.
   3. This is done to get the day without any leading zeros. E.g. *05 11 1996* will turn into *5*.
2. Then it calculates how many cells contain the date we are looking for and stores it in the variable `number_of_cells_with_day`.
   1. This is done as if we were to select the 1st of April,  the 1st of May may also show up on the same screen. The same goes for other low or high dates.
3. Then we store all of the cells with a date in a variable `all_days`.
4. After we check how many of the cells in `all_days` match the date we want to select and store them as a list in the variable `matching_days`.
5. Next we perform a few `IF` statements to see if we need to click the first, last or only cell stored in `matching_days`.
   1. If the date we want to select is less than 15, and `number_of_cells_with_day` is greater than 1, we select the first option in `all_days`.
   2. If the date we want to select is greater than 15 and `number_of_cells_with_day` is greater than 1, we select the last option in `all_days`.
   3. Otherwise if `number_of_cells_with_day` is set to 1, we select that date.

### Book First Eligible Appointment

This is called to select the first date with appointment slots available

#### Required Arguments

- `current_month_displayed`:
  - Type: `str`
  - The current month that is displayed by the calendar
- `locator`:
  - Type: `Locator`
  - The locator of the cells containing the appointment days
- `bg_colours`:
  - Type: `list`
  - A list containing all of the background colours of cells we would like to select

#### How This Function Works

1. Firstly it converts `current_month_displayed` into an integer and stores it in `current_month_displayed_int`.
2. Then it checks what OS in running to convert the current month the calendar is on into an integer.
   1. If it is windows then it calls the `format_date` method from DateTimeUtils and passes the formatting string: `"%#m"` and stores the result in `current_month_int`.
   2. Otherwise it calls the `format_date` method from DateTimeUtils and passes the formatting string: `"%-m"` and stores the result in `current_month_int`.
3. Then it passes `current_month_displayed_int` and `current_month_int` into the `book_appointments_go_to_month` method.
4. Next it runs a `while` loop to see if the calendar is showing any available appointments.
   1. This is done by calling the `check_for_eligible_appointment_dates` method.
   2. If True is returned by the `check_for_eligible_appointment_dates` method then the `while` loop is broken.
   3. Otherwise it carries on the loop 3 more times, advancing the month by 1 each time.
   4. If at the end of the 3 loops it cannot find an appointment, it fails the test.

### Book Appointments Go To Month

This is called to move the book appointments calendar to the month we desire.

#### Required Arguments

- `current_displayed_month`:
  - Type: `int`
  - This is the current month shown on the calendar
- `wanted_month`:
  - Type: `int`
  - This is the month we want the calendar to go to

#### How This Function Works

1. Firstly it calculates the difference between `current_displayed_month` and `wanted_month` and stores the result in `month_difference`.
2. Then if `month_difference` is greater than 0, it runs a for loop for the value of `month_difference` clicking on the previous month button once per loop.
3. If `month_difference` is less than 0, it runs a for loop for the value of `month_difference` clicking on the next month button once per loop.

### Check For Eligible Appointment Dates

This function loops through all of the appointment date cells to click on the first available date.

#### Required Arguments

- `locator`:
  - Type: `Locator`
  - This is the locator for all of the appointment date cells
- `bg_colours`:
  - Type: `list`
  - This is a list containing all of the background colours we want to click on

#### How This Function Works

1. Firstly it gets the number of total cells and stores them in the variable `locator_count`.
2. Then it runs a `FOR` loop for the value stored in `locator_count`.
3. Here it loops through each locator checking if the background colour matches any provided in `bg_colours`.
4. If it find a match then it checks the length on the "name" attribute of that cell.
   1. If it is less than 5 characters long, it belongs to the first calendar on the screen and is clicked.
   2. Otherwise it is ignored.
