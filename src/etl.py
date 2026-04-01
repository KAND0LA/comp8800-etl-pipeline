import pandas as pd
from validate import check_schema, validate_row

def run_etl(filepath: str):
    print(f"Starting ETL run for: {filepath}")
    
    # Extract
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from source")

    # Schema check
    valid_schema, schema_msg = check_schema(list(df.columns))
    print(f"Schema check: {schema_msg}")
    if not valid_schema:
        print("ETL BLOCKED — schema mismatch detected")
        return

    # Validate rows
    valid_rows = []
    quarantine_rows = []
    for _, row in df.iterrows():
        is_valid, reason = validate_row(row.to_dict())
        if is_valid:
            valid_rows.append(row)
        else:
            quarantine_rows.append({"data": str(row.to_dict()), "reason": reason})

    print(f"Valid rows: {len(valid_rows)}")
    print(f"Quarantined rows: {len(quarantine_rows)}")
    for q in quarantine_rows:
        print(f"  QUARANTINED — {q['reason']}")

if __name__ == "__main__":
    run_etl("../data/samples/sample_valid.csv")
```

**File 8: `data\samples\sample_valid.csv`**
```
case_number,date,block,location_description,arrest,domestic,year
HZ123456,2023-01-15,001XX N STATE ST,STREET,False,False,2023
HZ123457,2023-02-20,002XX W LAKE ST,APARTMENT,True,False,2023