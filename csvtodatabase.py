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
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, thousands=',', skipinitialspace=True)

    # Remove any leading/trailing spaces from column names
    df.columns = [col.strip() for col in df.columns]

    # Apply the cleaning function to all columns
    df.iloc[:, 1] = df.iloc[:, 1].apply(clean_data)  # Clean the values column

    # Pivot the DataFrame
    df_pivoted = df.pivot_table(index=df.columns[0], columns=df.columns[1], values=df.columns[2], aggfunc='sum')

    # Reset index to convert multi-index DataFrame to regular DataFrame
    df_pivoted = df_pivoted.reset_index()

    # Rename columns to ensure they are suitable for SQL insertion
    df_pivoted.columns.name = None  # Remove the columns' name if exists

    # Handle any remaining missing values or inappropriate data
    df_pivoted = df_pivoted.fillna(0)  # Example: Fill missing values with 0, adjust as needed

    # Write DataFrame to PostgreSQL
    df_pivoted.to_sql('relianceprofitlost', engine, if_exists='replace', index=False)

    print("Data inserted successfully into PostgreSQL!")
except Exception as e:
    print(f"Error processing data or inserting into PostgreSQL: {e}")
