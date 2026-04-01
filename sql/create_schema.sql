-- Staging table (raw incoming data)
CREATE TABLE IF NOT EXISTS staging_homicides (
    id SERIAL PRIMARY KEY,
    case_number VARCHAR(50),
    date VARCHAR(50),
    block VARCHAR(255),
    location_description VARCHAR(255),
    arrest BOOLEAN,
    domestic BOOLEAN,
    year INTEGER,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    loaded_at TIMESTAMP DEFAULT NOW()
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

-- Dimension: Location
CREATE TABLE IF NOT EXISTS dim_location (
    location_key SERIAL PRIMARY KEY,
    block VARCHAR(255),
    location_description VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    UNIQUE(block, location_description)
);

-- Fact table
CREATE TABLE IF NOT EXISTS fact_homicide (
    fact_id SERIAL PRIMARY KEY,
    case_number VARCHAR(50),
    date_key INTEGER REFERENCES dim_date(date_key),
    location_key INTEGER REFERENCES dim_location(location_key),
    arrest BOOLEAN,
    domestic BOOLEAN,
    effective_date DATE DEFAULT CURRENT_DATE,
    expiry_date DATE,
    is_current BOOLEAN DEFAULT TRUE
);

-- Quarantine table
CREATE TABLE IF NOT EXISTS quarantine_records (
    quarantine_id SERIAL PRIMARY KEY,
    raw_data TEXT,
    reason VARCHAR(500),
    quarantined_at TIMESTAMP DEFAULT NOW()
);

-- ETL log table
CREATE TABLE IF NOT EXISTS etl_log (
    log_id SERIAL PRIMARY KEY,
    run_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50),
    rows_processed INTEGER,
    rows_inserted INTEGER,
    rows_quarantined INTEGER,
    notes TEXT
);