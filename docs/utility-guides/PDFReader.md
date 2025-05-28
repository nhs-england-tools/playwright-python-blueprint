# Utility Guide: PDF Reader

The PDF Reader utility allows for reading PDF files and extracting NHS numbers from them.

## Table of Contents

- [Utility Guide: PDF Reader](#utility-guide-pdf-reader)
  - [Table of Contents](#table-of-contents)
  - [Functions Overview](#functions-overview)
    - [Extract NHS No From PDF](#extract-nhs-no-from-pdf)
      - [Required Arguments](#required-arguments)
      - [How This Function Works](#how-this-function-works)
      - [Example Usage](#example-usage)

## Functions Overview

For this utility, the following function is available:

- `extract_nhs_no_from_pdf`

### Extract NHS No From PDF

This function extracts all NHS numbers from a PDF file by searching for the string **"NHS No:"** on each page.

#### Required Arguments

- `file`:
  - Type: `str`
  - The file path to the PDF file as a string.

#### How This Function Works

1. Loads the PDF file using the `PdfReader` object from the `pypdf` package.
2. Loops through each page of the PDF.
3. Searches for the string *"NHS No"* on each page.
4. If found, extracts the NHS number, removes any whitespaces, and adds it to a pandas DataFrame (`nhs_no_df`).
5. If no NHS numbers are found on that page, it goes to the next page.
6. Returns the DataFrame containing all extracted NHS numbers.

#### Example Usage

You can use this utility to extract NHS numbers from a PDF file as part of the [`Batch Processing`](BatchProcessing.md) utility or by providing the file path as a string.

**Extracting NHS numbers using a file path:**

```python
from utils.pdf_reader import extract_nhs_no_from_pdf
file_path = "path/to/your/file.pdf"
nhs_no_df = extract_nhs_no_from_pdf(file_path)
```

**Extracting NHS numbers using batch processing:**

```python
from utils.pdf_reader import extract_nhs_no_from_pdf
get_subjects_from_pdf = True
file = download_file.suggested_filename # This is done via playwright when the "Retrieve button" on a batch is clicked.

nhs_no_df = (
  extract_nhs_no_from_pdf(file)
  if file.endswith(".pdf") and get_subjects_from_pdf
  else None
  )
```
