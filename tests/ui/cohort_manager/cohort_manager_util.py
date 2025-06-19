def subject_count_by_nhs_number(db_util, nhs_number, table_name):
    subject_search = (
        f"""select count(1) as count from {table_name} where nhs_number = %s """
    )
    df = db_util.get_results(subject_search, [nhs_number])
    return df["count"][0]


def fetch_all_audit_subjects(db_util, nhs_number):
    import pandas as pd

    subject_search = f"""select * from audit_subjects where nhs_number = %s order by transaction_db_date_time desc"""
    results = db_util.get_results(subject_search, [nhs_number])
    return pd.DataFrame(results)


def fetch_subject_column_value(db_util, nhs_number, table_column):
    subject_search = f"""select {table_column} from subjects where nhs_number = %s """
    results = db_util.get_results(subject_search, [nhs_number])
    assert len(results) == 1, f"Expected only 1 but returned {len(results)}"
    return results[table_column][0]
