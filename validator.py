import phonenumbers
from phonenumbers import NumberParseException

def normalize_and_validate_number(raw_number: str, default_region: str = "US") -> str | None:
    """
    Cleans and converts a raw phone string into a standard E.164 format.
    Returns the E.164 string if valid, or None if invalid.
    """
    if not raw_number or not isinstance(raw_number, str):
        return None

    # Strip surrounding whitespace
    clean_raw = raw_number.strip()

    try:
        # Parse number using default country region if + country code is missing
        parsed_number = phonenumbers.parse(clean_raw, default_region)

        # Validate structure and length for that region
        if phonenumbers.is_valid_number(parsed_number):
            # Format to E.164 (+18012345678)
            return phonenumbers.format_number(
                parsed_number, 
                phonenumbers.PhoneNumberFormat.E164
            )
        else:
            return None

    except NumberParseException:
        return None


def sanitize_phone_list(raw_numbers: list[str], default_region: str = "US") -> tuple[list[str], list[str]]:
    """
    Takes a list of raw phone strings, normalizes valid ones,
    and separates out the invalid/rejected ones.
    """
    valid_numbers: list[str] = []
    invalid_numbers: list[str] = []

    for num in raw_numbers:
        normalized = normalize_and_validate_number(num, default_region)
        if normalized:
            valid_numbers.append(normalized)
        else:
            invalid_numbers.append(num)

    return valid_numbers, invalid_numbers

if __name__ == "__main__":
    test_inputs = [
        "08012345678",        # Local Nigerian number
        "+234 802 345 6789",   # With spaces
        "+234-803-456-7890",   # With hyphens
        "0801234",             # Too short (invalid)
        "abc123456",           # Garbage string
        "+14155552671"         # US number with country code
    ]

    valid, invalid = sanitize_phone_list(test_inputs, default_region="NG")

    print("--- VALIDATED NUMBERS (E.164) ---")
    for v in valid:
        print(f"✓ {v}")

    print("\n--- REJECTED / INVALID NUMBERS ---")
    for inv in invalid:
        print(f"✗ {inv}")