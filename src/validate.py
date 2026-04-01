REQUIRED_COLUMNS = [
    "case_number", "date", "block",
    "location_description", "arrest", "domestic", "year"
]

def check_schema(df_columns: list) -> tuple[bool, str]:
    """Check if incoming CSV columns match expected schema."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df_columns]
    extra = [c for c in df_columns if c not in REQUIRED_COLUMNS]
    if missing:
        return False, f"Missing columns: {missing}"
    if extra:
        return True, f"Warning - extra columns ignored: {extra}"
    return True, "Schema OK"

def validate_row(row) -> tuple[bool, str]:
    """Validate a single row. Returns (is_valid, reason)."""
    if not row.get("case_number"):
        return False, "Missing case_number"
    if not row.get("date"):
        return False, "Missing date"
    try:
        year = int(row.get("year", 0))
        if year < 1900 or year > 2100:
            return False, f"Invalid year: {year}"
    except (ValueError, TypeError):
        return False, "Year is not a number"
    return True, "OK"