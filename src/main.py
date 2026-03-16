from pathlib import Path
import os
import sys

import pandas as pd

os.environ.setdefault("MPLCONFIGDIR", str((Path(__file__).resolve().parents[1] / "data" / ".mplconfig")))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = str(BASE_DIR)
DATA_FOLDER_NAME = "data"
GRAPH_FILE = BASE_DIR / "data" / "genre_average_global_sales.png"


#1 This function loads the CSV file into pandas.
def load_dataset(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find the dataset file: {file_path}")
        print("Make sure the CSV file is inside the data folder.")
        sys.exit(1)
    except Exception as error:
        print(f"Error: The dataset could not be loaded. {error}")
        sys.exit(1)


#2 This function finds all CSV files inside the data folder.
def get_csv_files(data_folder):
    files = []

    for file in os.listdir(data_folder):
        if file.lower().endswith(".csv"):
            files.append(file)

    return files


#3 This function shows the CSV files and lets the user pick one.
def choose_dataset(data_folder):
    csv_files = get_csv_files(data_folder)

    if not csv_files:
        print("No CSV files were found in the data folder.")
        return None

    print("\nAvailable datasets:")
    for index, file in enumerate(csv_files, start=1):
        print(f"{index}. {file}")

    while True:
        choice = input("\nSelect a dataset number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(csv_files):
                return os.path.join(data_folder, csv_files[choice - 1])

        print("Invalid selection. Please enter a valid number.")


#4 This function converts the chosen value column to numbers and removes bad rows.
def clean_dataset(dataframe, category_column, value_column):
    cleaned_df = dataframe.copy()

    cleaned_df[value_column] = pd.to_numeric(cleaned_df[value_column], errors="coerce")
    cleaned_df = cleaned_df.dropna(subset=[category_column, value_column])
    cleaned_df = cleaned_df[cleaned_df[value_column] > 0]

    return cleaned_df


#5 This function finds number columns that can be used for math.
def get_numeric_columns(dataset):
    return dataset.select_dtypes(include=["number"]).columns.tolist()


#6 This function finds text columns that can be used as categories.
def get_category_columns(dataset):
    return dataset.select_dtypes(include=["object", "string"]).columns.tolist()


#7 This function tries to pick the best columns for the analysis.
def choose_columns(dataset, numeric_columns, category_columns):
    preferred_category_columns = [
        "Genre", "genres",
        "Platform", "platforms",
        "Category", "categories",
        "Type", "type",
        "Publisher", "publisher",
        "developer"
    ]

    preferred_value_columns = [
        "Global_Sales",
        "Sales",
        "Revenue",
        "Value",
        "Amount",
        "positive_ratings",
        "price",
        "average_playtime",
        "median_playtime",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales"
    ]

    ignored_numeric_columns = {
        "appid", "Rank", "rank", "ID", "id",
        "english", "required_age"
    }

    category_column = None
    value_column = None

    for column in preferred_category_columns:
        if column in dataset.columns:
            category_column = column
            break

    for column in preferred_value_columns:
        if column in dataset.columns:
            value_column = column
            break

    if category_column is None:
        for column in category_columns:
            if column.lower() != "name":
                category_column = column
                break

    if category_column is None and category_columns:
        category_column = category_columns[0]

    if value_column is None:
        for column in numeric_columns:
            if column not in ignored_numeric_columns:
                value_column = column
                break

    if value_column is None and numeric_columns:
        value_column = numeric_columns[0]

    return category_column, value_column


#8 This function finds the average value for each category.
def find_average_by_category(dataframe, category_column, value_column):
    average_data = (
        dataframe.groupby(category_column)[value_column]
        .mean()
        .sort_values(ascending=False)
        .round(2)
        .reset_index()
    )

    return average_data


#9 This function finds which group shows up the most in the top rows.
def find_top_groups(dataframe, value_column, group_column, top_item_count=100):
    top_rows = dataframe.sort_values(value_column, ascending=False).head(top_item_count)

    group_counts = (
        top_rows.groupby(group_column)
        .size()
        .sort_values(ascending=False)
        .reset_index(name="Top_Count")
    )

    return top_rows, group_counts


#10 This function prints the average results in a cleaner way.
def print_average_report(average_data, category_column, value_column):
    if category_column == "Genre" and value_column == "Global_Sales":
        print("\nQuestion 1: Which genres have the highest average global sales?")
    else:
        print(f"\nQuestion 1: Which {category_column.lower()} values have the highest average {value_column.lower()}?")

    print("-" * 65)

    for row in average_data.head(10).itertuples(index=False):
        label = str(row[0])
        value = row[1]

        if value_column == "Global_Sales":
            print(f"{label:<12} Average Global Sales: {value:.2f}")
        else:
            print(f"{label:<12} Average {value_column}: {value:.2f}")


#11 This function prints the top group results for question 2.
def print_top_group_report(group_counts, top_item_count, group_column, value_column):
    if group_column == "Platform" and value_column == "Global_Sales":
        print("\nQuestion 2: Which platforms have the most top-selling games?")
        print("-" * 63)
        print(f"Top-selling games are defined here as the top {top_item_count} games by global sales.\n")

        for row in group_counts.head(10).itertuples(index=False):
            print(f"{row[0]:<8} Games in Top {top_item_count}: {row[1]}")
    else:
        print(f"\nQuestion 2: Which {group_column.lower()} values appear the most in the top {top_item_count} rows?")
        print("-" * 63)
        print()

        for row in group_counts.head(10).itertuples(index=False):
            print(f"{row[0]:<12} Count: {row[1]}")


#12 This function saves a bar chart for the top average results.
def create_average_chart(average_data, output_path, category_column, value_column):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    top_rows = average_data.head(8)

    plt.figure(figsize=(10, 6))
    plt.bar(top_rows.iloc[:, 0], top_rows.iloc[:, 1], color="steelblue")

    if category_column == "Genre" and value_column == "Global_Sales":
        plt.title("Top Genres by Average Global Sales")
    else:
        plt.title(f"Top {category_column} Values by Average {value_column}")

    plt.xlabel(category_column)
    plt.ylabel(value_column)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


#13 This function prints a quick summary of the dataset.
def print_dataset_summary(dataframe, category_column):
    print("Video Game Sales Data Analysis")
    print("=" * 31)
    print(f"Rows used in analysis: {len(dataframe)}")

    if "Genre" in dataframe.columns:
        print(f"Unique genres: {dataframe['Genre'].nunique()}")

    if "Platform" in dataframe.columns:
        print(f"Unique platforms: {dataframe['Platform'].nunique()}")

    if "Year" in dataframe.columns:
        year_min = int(dataframe["Year"].min()) if dataframe["Year"].notna().any() else "Unknown"
        year_max = int(dataframe["Year"].max()) if dataframe["Year"].notna().any() else "Unknown"
        print(f"Year range in data: {year_min} to {year_max}")
    else:
        print(f"Unique {category_column.lower()} values: {dataframe[category_column].nunique()}")


#14 This function runs the whole program from start to finish.
def main():
    print("Video Game Sales Data Analysis")
    print("=" * 30)

    data_folder = os.path.join(PROJECT_ROOT, DATA_FOLDER_NAME)
    dataset_path = choose_dataset(data_folder)

    if dataset_path is None:
        return

    dataset = load_dataset(dataset_path)

    print("\nDataset Info")
    print("----------------")
    print(f"Rows: {len(dataset)}")
    print(f"Columns: {len(dataset.columns)}")
    print("Column Names:")
    print(dataset.columns.tolist())

    numeric_columns = get_numeric_columns(dataset)
    category_columns = get_category_columns(dataset)

    print("\nDetected numeric columns:")
    print(numeric_columns)

    print("\nDetected category columns:")
    print(category_columns)

    category_column, value_column = choose_columns(dataset, numeric_columns, category_columns)

    if not category_column or not value_column:
        print("Dataset does not contain usable columns.")
        return

    print("\nUsing columns:")
    print(f"Category column: {category_column}")
    print(f"Value column: {value_column}")

    cleaned_data = clean_dataset(dataset, category_column, value_column)

    if cleaned_data.empty:
        print("Error: No usable rows remained after cleaning the dataset.")
        sys.exit(1)

    print_dataset_summary(cleaned_data, category_column)

    average_data = find_average_by_category(cleaned_data, category_column, value_column)

    group_column = "Platform" if "Platform" in cleaned_data.columns else category_column
    top_item_count = 100
    top_rows, group_counts = find_top_groups(cleaned_data, value_column, group_column, top_item_count)

    print_average_report(average_data, category_column, value_column)
    print_top_group_report(group_counts, top_item_count, group_column, value_column)

    print("\nExtra Details")
    print("-" * 13)

    if "Name" in top_rows.columns:
        print("Top 5 rows used in the extra details check:")
        for row in top_rows[["Name", value_column]].head(5).itertuples(index=False):
            print(f"{row[0]} - {row[1]:.2f}")
    elif "name" in top_rows.columns:
        print("Top 5 rows used in the extra details check:")
        for row in top_rows[["name", value_column]].head(5).itertuples(index=False):
            print(f"{row[0]} - {row[1]:.2f}")
    else:
        print("Top 5 rows used in the extra details check:")
        for row in top_rows[[category_column, value_column]].head(5).itertuples(index=False):
            print(f"{row[0]} - {row[1]:.2f}")

    create_average_chart(average_data, GRAPH_FILE, category_column, value_column)
    print(f"\nGraph saved to: {GRAPH_FILE}")


if __name__ == "__main__":
    main()
