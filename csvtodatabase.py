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
        # Convert to integer or float if it's a number, otherwise return None
        if value.replace('.', '', 1).isdigit():  # Check if value is numeric
            try:
                return float(value)  # Use float to handle decimal values
            except ValueError:
                return None
        return value  # Return text as is if it's not numeric
    return value

try:
    # Read the CSV file into a DataFrame, handling the comma as a decimal separator
    df = pd.read_csv(csv_file_path, thousands=',', skipinitialspace=True)

    # Remove any leading/trailing spaces from column names
    df.columns = [col.strip() for col in df.columns]

    # Ensure the first column is treated as text and other columns are treated as numeric
    df.iloc[:, 0] = df.iloc[:, 0].astype(str)  # Convert the first column to string

    # Apply the cleaning function to all columns
    for col in df.columns[1:]:  # Skip the first column as it's text
        df[col] = df[col].apply(clean_data)

    # Convert columns to appropriate types
    df[df.columns[1:]] = df[df.columns[1:]].astype(float)

    # Handle any remaining missing values or inappropriate data
    df = df.fillna(0)  # Example: Fill missing values with 0, adjust as needed

    # Transpose the DataFrame
    df_transposed = df.transpose()

    # Write Transposed DataFrame to PostgreSQL
    df_transposed.to_sql('relianceprofitlost', engine, if_exists='replace', index=False)

    print("Data inserted successfully into PostgreSQL!")
except Exception as e:
    print(f"Error processing data or inserting into PostgreSQL: {e}"
