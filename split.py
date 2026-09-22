import pandas as pd
from sklearn.model_selection import train_test_split


def split_dataset(file_path, target_column=None, test_size=0.2, random_state=42):
    """
    Splits any CSV dataset into training and testing sets.

    Parameters:
        file_path (str): Path to the CSV file.
        target_column (str): Name of the target/label column (optional).
        test_size (float): Proportion of data to use for testing (default 0.2).
        random_state (int): Seed for reproducibility.

    Returns:
        Train and test splits of the dataset.
    """
    # Load the dataset
    data = pd.read_csv(file_path)
    print(f"Dataset loaded successfully. Shape: {data.shape}")

    if target_column and target_column not in data.columns:
        print(
            f"Warning: target_column '{target_column}' not found in the dataset. "
            f"Available columns: {list(data.columns)}. "
            f"Falling back to a whole-dataset split (no target column)."
        )
        target_column = None

    if target_column:
        # Split into features (X) and target (y)
        X = data.drop(columns=[target_column])
        y = data[target_column]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        print(f"Training set shape: {X_train.shape}")
        print(f"Testing set shape: {X_test.shape}")
        return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test}

    else:
        # No target column specified (or not found); split the whole dataset
        train_data, test_data = train_test_split(
            data, test_size=test_size, random_state=random_state
        )

        print(f"Training set shape: {train_data.shape}")
        print(f"Testing set shape: {test_data.shape}")
        return {"train": train_data, "test": test_data}


if __name__ == "__main__":
    file_path = "Housing.csv"        # Replace with your dataset path
    target_column = "target"         # Replace with your target column name, or set to None

    result = split_dataset(file_path, target_column, test_size=0.2)

    if "X_train" in result:
        result["X_train"].to_csv("X_train.csv", index=False)
        result["X_test"].to_csv("X_test.csv", index=False)
        result["y_train"].to_csv("y_train.csv", index=False)
        result["y_test"].to_csv("y_test.csv", index=False)
    else:
        result["train"].to_csv("train.csv", index=False)
        result["test"].to_csv("test.csv", index=False)

    print("Train and test datasets saved successfully.")