# import pandas as pd
# from sqlalchemy import create_engine
# import os

# # Database connection parameters
# db_name = "concourse"
# db_user = "concourse_user"
# db_password = "concourse_pass"
# db_host = "192.168.3.109"
# db_port = "5432"

# # Path to the CSV file
# csv_file_path = "profit_loss_data/profit_loss_data.csv"

# # Create SQLAlchemy engine
# db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# engine = create_engine(db_url)

# try:
#     # Read the CSV file into a DataFrame
#     df = pd.read_csv(csv_file_path)

#     # Remove any leading/trailing spaces from column names
#     df.columns = [col.strip() for col in df.columns]

#     # Write DataFrame to PostgreSQL
#     df.to_sql('relianceprofitlost', engine, if_exists='replace', index=False)

#     print("Data inserted successfully into PostgreSQL!")
# except Exception as e:
#     print(f"Database connection failed: {e}")

import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# Database connection parameters
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_host = "192.168.3.109"
db_port = "5432"

# Path to the CSV file
csv_file_path = "profit_loss_data/profit_loss_data.csv"

# Create SQLAlchemy engine
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

def clean_data(value):
    # Remove any unwanted symbols like +, %, commas
    if isinstance(value, str):
        value = value.replace("+", "").replace("%", "").replace(",", "").strip()
        # Convert to integer if it's a number, otherwise return None or appropriate value
        if value.isdigit():
            return int(value)
        else:
            try:
                # Try converting to float, which handles decimal values
                return float(value)
            except ValueError:
                return None
    return value

try:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Remove any leading/trailing spaces from column names
    df.columns = [col.strip() for col in df.columns]

    # Apply the cleaning function to all columns
    for col in df.columns:
        df[col] = df[col].apply(clean_data)

    # Handle specific column types
    # EPS in Rs column may have float values, so let's ensure it's treated as float
    if 'EPS in Rs' in df.columns:
        df['EPS in Rs'] = df['EPS in Rs'].astype(float)

    # Drop columns if necessary or handle data types as per requirements
    # Example: Drop rows where 'EPS in Rs' is completely missing if needed
    df = df.dropna(subset=['EPS in Rs'])

    # Write DataFrame to PostgreSQL
    df.to_sql('relianceprofitlost', engine, if_exists='replace', index=False)

    print("Data inserted successfully into PostgreSQL!")
except Exception as e:
    print(f"Database connection failed: {e}")
