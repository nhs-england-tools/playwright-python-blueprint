import logging
import random
from typing import Dict, List
from utils.oracle.oracle import OracleDB


class WordRepository:
    """
    Python version using oracledb and pandas for random word and subject detail generation.
    Assumes execute_query is available for running SQL and returning a pandas DataFrame.
    """

    def __init__(self):
        """
        db_util: An object that provides the execute_query method as described.
        """
        self.db_util = OracleDB()
        self.forename_weighting = [80, 95, 100]
        self.surname_weighting = [90, 97, 100]
        self.names_max_length = 35

    def get_random_words_by_weighting(
        self, weightings: List[int], max_length: int
    ) -> str:
        """
        Gets a string of random words based on the provided weightings and maximum length.
        Args:
            weightings (List[int]): A list of integers representing cumulative percentage thresholds for word counts.
            max_length (int): The maximum length of the resulting string.
        Returns:
            str: A string of random words.
        """
        logging.debug("START: get_random_words_by_weighting")
        percentage = random.randint(0, 99)
        words = 0
        for i, weighting in enumerate(weightings):
            if percentage < weighting:
                words = i + 1
                break

        sb = []
        for i in range(words):
            new_word = self.get_random_word()
            if sum(len(w) for w in sb) + len(new_word) + len(sb) < max_length:
                sb.append(new_word)
        result = " ".join(sb)
        logging.debug(
            f"RANDOM WORD(S): {result}. Actual length: {len(result)}. Specified Max length: {max_length}"
        )
        logging.debug("END: get_random_words_by_weighting")
        return result

    def get_random_word(self) -> str:
        """
        Gets a single random word from the database, or "TEST" if an error occurs.
        Returns:
            str: A random word or "TEST" if an error occurs.
        """
        logging.debug("START: get_random_word")
        try:
            word = self.find_random_word()
            logging.debug("END: get_random_word")
            return word if word else "TEST"
        except Exception as e:
            logging.debug(f"Caught Exception, returning TEST instead: {e}")
            logging.debug("END: get_random_word")
            return "TEST"

    def find_random_word(self) -> str:
        """
        Finds a random word from the database.
        Returns:
            str: A random word.
        """
        logging.debug("START: find_random_word")
        seq_range_query = (
            "SELECT MIN(SEQ) AS MIN_SEQ, MAX(SEQ) AS MAX_SEQ FROM MPI_ANON.ANON_WORD"
        )
        df_range = self.db_util.execute_query(seq_range_query)
        min_seq_col = next(
            (c for c in df_range.columns if c.lower() == "min_seq"), None
        )
        max_seq_col = next(
            (c for c in df_range.columns if c.lower() == "max_seq"), None
        )
        if (
            df_range.empty
            or min_seq_col is None
            or max_seq_col is None
            or df_range.iloc[0][min_seq_col] is None
            or df_range.iloc[0][max_seq_col] is None
        ):
            logging.debug(
                f"MIN_SEQ or MAX_SEQ column not found in df_range: {df_range.columns}"
            )
            return "TEST"
        min_seq = int(df_range.iloc[0][min_seq_col])
        max_seq = int(df_range.iloc[0][max_seq_col])
        random_seq = random.randint(min_seq, max_seq)
        word_query = "SELECT WORD FROM MPI_ANON.ANON_WORD WHERE SEQ = :seq"
        df_word = self.db_util.execute_query(word_query, {"seq": random_seq})
        word_col = next((c for c in df_word.columns if c.lower() == "word"), None)
        if not df_word.empty and word_col is not None:
            word = df_word.iloc[0][word_col]
        else:
            word = "TEST"
        logging.debug(f"return {word}")
        logging.debug("END: find_random_word")
        return word

    def get_random_subject_details(self) -> Dict[str, str]:
        """
        Gets a dictionary of random subject details.
        Returns:
            Dict[str, str]: A dictionary containing random subject details.
        """
        logging.debug("START: get_random_subject_details")
        details = {}
        # Weighted values
        details["forename"] = self.get_random_words_by_weighting(
            self.forename_weighting, self.names_max_length
        )
        details["forename2"] = self.get_random_words_by_weighting(
            self.forename_weighting, self.names_max_length
        )
        details["surname"] = self.get_random_words_by_weighting(
            self.surname_weighting, self.names_max_length
        )
        details["surname2"] = self.get_random_words_by_weighting(
            self.surname_weighting, self.names_max_length
        )
        # Unweighted values
        details["county"] = self.get_random_word()
        details["locality"] = self.get_random_word()
        details["city"] = self.get_random_word()
        details["town"] = self.get_random_word()
        details["roadPrefix"] = self.get_random_word()
        details["roadSuffix"] = self.get_random_word()
        logging.debug("END: get_random_subject_details")
        return details
