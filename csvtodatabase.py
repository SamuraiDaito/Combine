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
# new comment for testing
import pandas as pd
from sqlalchemy import create_engine

# Database connection parameters
db_name = "concourse"
db_user = "concourse_user"
db_password = "concourse_pass"
db_host = "192.168.1.233"
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
    # Read the CSV file into a DataFrame, assuming that the first row contains headers
    df = pd.read_csv(csv_file_path, thousands=',', skipinitialspace=True)

    # Remove any leading/trailing spaces from column names
    df.columns = [col.strip() for col in df.columns]

    # Clean and convert data in all columns except the first one (which is assumed to be non-numeric like years)
    for col in df.columns[1:]:
        df[col] = df[col].apply(clean_data)

    # Handle missing or inappropriate values
    df = df.fillna(0)  # Replace missing values with 0 or adjust as necessary

    # Write the cleaned DataFrame directly into PostgreSQL
    df.to_sql('relianceprofitlost', engine, if_exists='replace', index=False)

    print("Data inserted successfully into PostgreSQL!")
except Exception as e:
    print(f"Error processing data or inserting into PostgreSQL: {e}")
