import secrets


class CheckDigitGenerator:
    def generate_check_digit(self) -> dict:
        return self.calculate("PMA")["batch_id"]

    # This function calculates the check digit
    def check_digit(self, bso_code: str, sequence: str) -> str:
        base = int(sequence)
        for char in bso_code:
            base += ord(char)

        check_digit_sequence = "ACDEFGHJKLMNPQRTUWX"
        check_digit_index = base % len(check_digit_sequence)
        return check_digit_sequence[check_digit_index]

    # This function generates the batch ID
    def calculate(self, bso_code: str) -> dict:
        bso_code = bso_code.strip().upper()
        if len(bso_code) == 3:
            random_sequence = str(secrets.randbelow(900000) + 100000)
            check = self.check_digit(bso_code, random_sequence)
            batch_id = f"{bso_code}{random_sequence}{check}"
            return {
                "sequence": random_sequence,
                "check_digit": check,
                "batch_id": batch_id,
            }
        else:
            return {"sequence": "", "check_digit": "", "batch_id": ""}

    # This function validates a given batch ID
    def validate(self, bso_batch_id: str) -> str:
        if len(bso_batch_id) != 10:
            return f"Expected 10 length, but was {len(bso_batch_id)}"

        bso_code = bso_batch_id[:3]
        sequence = bso_batch_id[3:9]
        actual_check_digit = bso_batch_id[9]

        if not sequence.isnumeric():
            return f"Invalid sequence number: {sequence}"

        expected_check_digit = self.check_digit(bso_code, sequence)
        if expected_check_digit != actual_check_digit:
            return f"Expected check digit: {expected_check_digit}, but was {actual_check_digit}"

        return "Valid"
