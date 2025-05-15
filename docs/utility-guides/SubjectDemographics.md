# Utility Guide: Subject Demographics

The Subject Demographics utility allows for different updates to subjects to be made.<br>
This includes the following:

1. Updating a subjects DOB to the following age ranges:
   1. 50-70
   2. 75-100

## Table of Contents

- [Utility Guide: Subject Demographics](#utility-guide-subject-demographics)
  - [Table of Contents](#table-of-contents)
  - [Using the Subject Demographics class](#using-the-subject-demographics-class)
  - [Updating DOB](#updating-dob)
    - [Required Args](#required-args)
    - [How to use this method](#how-to-use-this-method)

## Using the Subject Demographics class

You can initialise the Subject Demographics class by using the following code in your test file:

    from utils.subject_demographics import SubjectDemographicUtil

## Updating DOB

Inside of the SubjectDemographicUtil class there is a method called `update_subject_dob`.<br>
This is used to update the date of birth of a subject to a random age between 50-70 and 75-100 depending on if the argument `younger_subject` is set to True or False.<br>
This method will navigate to the subject demographic page automatically and can be called from any page.

### Required Args

- nhs_no:
  - Type: `str`
  - This is the NHS number of the subject you want to update
- younger_subject:
  - Type: `bool`
  - Whether you want the subject to be younger (50-70) or older (75-100).

### How to use this method

To use this method simply import the SubjectDemographicUtil class and call this method, providing the two arguments:

    nhs_no = "9468743977"
    SubjectDemographicUtil(page).update_subject_dob(nhs_no, False)
