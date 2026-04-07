# Remember AI cannot read a Dataframe. It only understands text, so ingest.py is like a translator
# It takes your dataframe and converts it into meaningful text chunks that the AI can understand and search through

import pandas as pd
from typing import List


# This function takes in a list and returns a list of text strings
def ingest_dataframe(df: pd.DataFrame) -> List[str]:
    texts = []
    # This chink works on the whole dataset and gives the total rows, columns and data types
    # Data Cleaning
    print("Cleaning data...")
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    numeric_cols = df.select_dtypes(include='number').columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

        cat_cols = df.select_dtypes(include='object').columns
        for col in cat_cols:
            df[col] = df[col].fillna('Unknown')

        for col in cat_cols:
            df[col].str.strip()

        df = df.drop_duplicates()

        df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('[^A-Za-z0-9_]', '', regex=True)

        print(f"Data Cleaned!, Shape after cleaning: {df.shape}")

    overview = f"""
    Dataset Overview:
    - Total rows: {len(df)}
    - Total columns: {len(df.columns)}
    - Column names: {', '.join(df.columns.tolist())}
    - Data types: {df.dtypes.to_dict()}
    """
    texts.append(overview)


# This chunk picks the number columns and answers numeric questions from this chunk
    numeric_cols = df.select_dtypes(include = 'number').columns.to_list()
    if numeric_cols:
        stats = df[numeric_cols].describe().to_string()
        texts.append(f"Stastical summary of numeric columns{stats}")


# This chunk cover now the missing values
    missing = df.isnull().sum()
    missing_info = "\n".join([f"{col}: {count} missing values" for col, count in missing.items() if count > 0])
    if missing_info:
        texts.append(f"Missing Values:\n{missing_info}")
    else:
        texts.append("Missing Values: No missing values found in the dataset.")

# This chunk covers for Unique values for categorical columns, columns that can be categorised
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols[:5]:  # Limit to first 5 categorical columns
        unique_vals = df[col].value_counts().head(10)
        texts.append(f"Column '{col}' top values:\n{unique_vals.to_string()}")

# Row-by-row chunks (batched to avoid too many chunks) ---
# Convert rows to readable text in batches of 10 since the ai cannot take all the information at once
    batch_size = 10
    for i in range(0, min(len(df), 500), batch_size):  # Cap at 500 rows
        batch = df.iloc[i:i+batch_size]
        chunk = f"Rows {i+1} to {i+len(batch)}:\n"
        chunk += batch.to_string(index=False)
        texts.append(chunk)

    print(f"Ingested {len(df)} rows into {len(texts)} text chunks.")
    return texts
# Remember AI cannot read a Dataframe. It only understands text, so ingest.py is like a translator
# It takes your dataframe and converts it into meaningful text chunks that the AI can understand and search through

import pandas as pd
from typing import List


# This function takes in a list and returns a list of text strings
def ingest_dataframe(df: pd.DataFrame) -> List[str]:
    texts = []
    # This chink works on the whole dataset and gives the total rows, columns and data types

    overview = f"""
    Dataset Overview:
    - Total rows: {len(df)}
    - Total columns: {len(df.columns)}
    - Column names: {', '.join(df.columns.tolist())}
    - Data types: {df.dtypes.to_dict()}
    """
    texts.append(overview)


# This chunk picks the number columns and answers numeric questions from this chunk
    numeric_cols = df.select_dtypes(include = 'number').columns.to_list()
    if numeric_cols:
        stats = df[numeric_cols].describe().to_string()
        texts.append(f"Stastical summary of numeric columns{stats}")


# This chunk cover now the missing values
    missing = df.isnull().sum()
    missing_info = "\n".join([f"{col}: {count} missing values" for col, count in missing.items() if count > 0])
    if missing_info:
        texts.append(f"Missing Values:\n{missing_info}")
    else:
        texts.append("Missing Values: No missing values found in the dataset.")

# This chunk covers for Unique values for categorical columns, columns that can be categorised
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    for col in cat_cols[:5]:  # Limit to first 5 categorical columns
        unique_vals = df[col].value_counts().head(10)
        texts.append(f"Column '{col}' top values:\n{unique_vals.to_string()}")

# Row-by-row chunks (batched to avoid too many chunks) ---
# Convert rows to readable text in batches of 10 since the ai cannot take all the information at once
    batch_size = 10
    for i in range(0, min(len(df), 500), batch_size):  # Cap at 500 rows
        batch = df.iloc[i:i+batch_size]
        chunk = f"Rows {i+1} to {i+len(batch)}:\n"
        chunk += batch.to_string(index=False)
        texts.append(chunk)

    print(f"Ingested {len(df)} rows into {len(texts)} text chunks.")
    return texts
