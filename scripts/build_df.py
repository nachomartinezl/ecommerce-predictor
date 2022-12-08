import json
import pandas as pd
import numpy as np

def build_df(json_path: str, threshold: int, force_leafs_under_threshold: bool, preprocessed_csv: str = None):     
    # Build base dataframe
    df = build_base_dataframe(json_path, preprocessed_csv)
    
    # Get number of category columns
    number_of_categories_columns = len(get_category_columns(df))
    
    # Replace leaf category according to threshold
    for i in reversed(range(number_of_categories_columns)):
        level = df["category_" + str(i)].copy()
        level_count_series = level.value_counts()
        categories_within_threshold = level_count_series[level_count_series > threshold].reset_index()["index"]
        is_category_in_threshold_and_not_nan = ~(~level.isin(categories_within_threshold) & level.notna())
        df["category_" + str(i)] = level.where(is_category_in_threshold_and_not_nan, 'other')
       
    # "path" column, with a list of all the categories from root to leaf
    df.insert(2,"path",df.apply(lambda row: conditions_path(row, number_of_categories_columns), axis=1))

    # "leaf" column, excluding "other" unless it's a root category
    df.insert(2,"leaf",df.apply(lambda row: conditions_leaf(row, number_of_categories_columns), axis=1))
    
    # "max_depth" column
    df.insert(3,"max_depth",df.apply(lambda row: conditions_max_depth(row, number_of_categories_columns), axis=1))
    
    # If force_leafs_under_threshold, it makes sure that all values in df["leaf"].value_counts() are above the threshold
    # This happens even if the category has more than the threshold
    if force_leafs_under_threshold:
        # Get the leafs not under threshold
        leaf_count_series = df["leaf"].value_counts()
        leafs_to_kill = leaf_count_series[leaf_count_series < threshold].reset_index()["index"]
        # First condition to kill leafs
        condition_leafs = df["leaf"].isin(leafs_to_kill)
        for i in reversed(range(number_of_categories_columns)):
            # Makes sure that only removes the category if it's a leaf
            condition_depth = df["max_depth"] == i + 1
            # Merge two conditions
            final_condition = ~(condition_leafs + condition_depth)
            # Replace each leaf with nan
            df["category_" + str(i)] = df["category_" + str(i)].where(final_condition, np.nan)

        # Assign "other" to nan on category_0 to make possible reassigning columns depending on it
        df["path"] = df.apply(lambda row: conditions_path(row, number_of_categories_columns), axis=1)
        df["max_depth"] = df.apply(lambda row: conditions_max_depth(row, number_of_categories_columns), axis=1)
        df["category_0"] = df["category_0"].where(~(df["max_depth"] == 0), "other")

        # Reasign columns
        # "path" column, with a list of all the categories from root to leaf
        df["path"] = df.apply(lambda row: conditions_path(row, number_of_categories_columns), axis=1)
        # "leaf" column, excluding "other" unless it's a root category
        df["leaf"] = df.apply(lambda row: conditions_leaf(row, number_of_categories_columns), axis=1)
        # "max_depth" column
        df["max_depth"] = df.apply(lambda row: conditions_max_depth(row, number_of_categories_columns), axis=1)

    # Change "other" for np.nan
    df_nan = df.copy()
    for column in get_category_columns(df_nan):
        df_nan[column] = df_nan[column].apply(lambda x: np.nan if x == "other" else x)
    
    return df_nan


### Auxiliary Functions
# Build base dataframe
def build_base_dataframe(json_path, preprocessed_csv=None):
    # Save json into dict
    with open(json_path) as f:
        products_dic = json.load(f)
    
    # Create base DataFrame
    all_cats_dict = []
    for dic in products_dic:
        new_dict = {}
        if preprocessed_csv == None:
            # Add name and description
            new_dict["name"] = dic["name"]
            new_dict["description"] = dic["description"]
        
        # Add category names respecting hierarchy
        for i in range(len(dic["category"])):
            new_dict["category_" + str(i)] = dic["category"][i]["id"]
        all_cats_dict.append(new_dict)
    
    df = pd.DataFrame(all_cats_dict)
    
    if preprocessed_csv != None:
        df.insert(0, "name", pd.read_csv(preprocessed_csv)["name"])
        df.insert(1, "description", pd.read_csv(preprocessed_csv)["description"])
    
    # Fix bad categorized item
    # item's 41319 category_0 is pcmcat248700050021 BUT should be pcmcat312300050015
    df["category_0"].iloc[41319] = "pcmcat312300050015"
    return df

# Conditions for creating the "path" column
def conditions_path(row, number_of_categories_columns):
    path = []
    if row["category_0"] == "other":
        return "other"
    for i in range(number_of_categories_columns):
        if type(row["category_" + str(i)]) == str and row["category_" + str(i)] != 'other':
            path.append(row["category_" + str(i)])
    return path

# Conditions for creating the "leaf" column
def conditions_leaf(row, number_of_categories_columns):
    if row["category_0"] == "other":
        return "other"
    for i in reversed(range(number_of_categories_columns)):
        if type(row["category_" + str(i)]) == str and row["category_" + str(i)] != 'other':
            return row["category_" + str(i)]

# Conditions for creating the "max_depth" column
def conditions_max_depth(row, number_of_categories_columns):
    if row["path"] == "other":
        return 1
    return len(row["path"])

# Get "category_" columns list
def get_category_columns(df):    
    category_columns = []
    for column in df.columns:
            if column.startswith("category_"):
                category_columns.append(column)
    return category_columns