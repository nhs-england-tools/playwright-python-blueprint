from pypdf import PdfReader
import pandas as pd


def extract_nhs_no_from_pdf(file: str) -> pd.DataFrame:
    """
    Extracts all of the NHS Numbers in a PDF file and stores them in a pandas DataFrame.

    Args:
        file (str): The file path stored as a string.

    Returns:
        nhs_no_df (pd.DataFrame): A DataFrame with the column 'subject_nhs_number' and each NHS number being a record
    """
    reader = PdfReader(file)
    nhs_no_df = pd.DataFrame(columns=["subject_nhs_number"])
    # For loop looping through all pages of the file to find the NHS Number
    for i, pages in enumerate(reader.pages):
        text = pages.extract_text()
        if "NHS No" in text:
            # If NHS number is found split the text by every new line into a list
            text = text.splitlines(True)
            for split_text in text:
                if "NHS No" in split_text:
                    # If a string is found containing "NHS No" only digits are stored into nhs_no
                    nhs_no = "".join([ele for ele in split_text if ele.isdigit()])
                    nhs_no_df.loc[i] = [nhs_no]
    return nhs_no_df
