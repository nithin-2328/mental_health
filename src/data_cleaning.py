"""
Data Cleaning Module for Mental Health in Tech Survey
Provides robust, reproducible cleaning functions for survey data.
"""

import os
import pandas as pd
import numpy as np


def load_raw_data(filepath):
    """
    Load raw survey dataset from CSV file.
    
    Args:
        filepath (str): Relative or absolute path to raw survey.csv
        
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Raw data file not found at: {filepath}")
    df = pd.read_csv(filepath)
    return df


def inspect_missing_and_duplicates(df):
    """
    Compute missing value summary and duplicate row count.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        tuple: (missing_summary_df, duplicate_count)
    """
    missing_counts = df.isnull().sum()
    missing_pct = (missing_counts / len(df)) * 100
    missing_df = pd.DataFrame({
        'missing_count': missing_counts,
        'missing_percentage': missing_pct.round(2)
    })
    duplicate_count = int(df.duplicated().sum())
    return missing_df, duplicate_count


def clean_age(df, min_age=18, max_age=75):
    """
    Clean invalid Age entries (negative, non-adult, or impossible values).
    Imputes outlier values with the median of valid respondents (18 to 75).
    
    Args:
        df (pd.DataFrame): Input DataFrame
        min_age (int): Minimum realistic working age (default: 18)
        max_age (int): Maximum realistic working age (default: 75)
        
    Returns:
        pd.DataFrame: DataFrame with 'Age_Cleaned' column
    """
    df = df.copy()
    valid_mask = (df['Age'] >= min_age) & (df['Age'] <= max_age)
    median_valid_age = int(df.loc[valid_mask, 'Age'].median())
    
    df['Age_Cleaned'] = df['Age']
    df.loc[~valid_mask, 'Age_Cleaned'] = median_valid_age
    df['Age_Cleaned'] = df['Age_Cleaned'].astype(int)
    return df


def create_age_groups(df):
    """
    Bin cleaned ages into standard demographic cohorts.
    
    Args:
        df (pd.DataFrame): DataFrame containing 'Age_Cleaned'
        
    Returns:
        pd.DataFrame: DataFrame with 'Age_Group' categorical column
    """
    df = df.copy()
    bins = [17, 24, 34, 44, 54, 100]
    labels = ['18-24', '25-34', '35-44', '45-54', '55+']
    df['Age_Group'] = pd.cut(df['Age_Cleaned'], bins=bins, labels=labels)
    return df


def clean_gender(df):
    """
    Harmonize the 49 unique free-text gender strings into three standard categories:
    'Male', 'Female', and 'Non-Binary/Other'.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with 'Gender_Cleaned' column
    """
    df = df.copy()
    
    male_terms = {
        'male', 'm', 'male-ish', 'maile', 'mal', 'male (cis)', 'make', 'male ',
        'man', 'msle', 'mail', 'malr', 'cis man', 'cis male'
    }
    
    female_terms = {
        'female', 'f', 'woman', 'female ', 'female (cis)', 'femail',
        'cis-female/femme', 'femake', 'cis female'
    }
    
    def _map_gender(val):
        if pd.isna(val):
            return 'Non-Binary/Other'
        cleaned = str(val).strip().lower()
        if cleaned in male_terms:
            return 'Male'
        elif cleaned in female_terms:
            return 'Female'
        else:
            return 'Non-Binary/Other'
            
    df['Gender_Cleaned'] = df['Gender'].apply(_map_gender)
    return df


def handle_missing_values(df):
    """
    Apply domain-grounded missing value strategies:
    - comments: 87.0% missing (optional field) -> Fill with 'No Comment' and add 'has_comment' flag.
    - state: 40.9% missing (US-only field) -> Fill with 'Outside US / Not Applicable'.
    - work_interfere: 21.0% missing (conditional on having condition) -> Fill with 'Not Applicable / Unreported'.
    - self_employed: 1.4% missing -> Impute with mode ('No').
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with treated missing values
    """
    df = df.copy()
    
    # Comments
    df['has_comment'] = df['comments'].notnull().astype(int)
    df['comments'] = df['comments'].fillna('No Comment')
    
    # State
    df['state'] = df['state'].fillna('Outside US / Not Applicable')
    
    # Work Interfere
    df['work_interfere'] = df['work_interfere'].fillna('Not Applicable / Unreported')
    
    # Self Employed (Mode = 'No')
    mode_val = df['self_employed'].mode()[0] if not df['self_employed'].mode().empty else 'No'
    df['self_employed'] = df['self_employed'].fillna(mode_val)
    
    return df


def convert_timestamps(df):
    """
    Convert Timestamp column to datetime and extract survey year and month.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: DataFrame with parsed datetime and temporal features
    """
    df = df.copy()
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df['Survey_Year'] = df['Timestamp'].dt.year
    df['Survey_Month'] = df['Timestamp'].dt.month
    return df


def clean_survey_data(raw_filepath, output_filepath=None):
    """
    Execute full data cleaning pipeline and optionally save the cleaned dataset.
    
    Args:
        raw_filepath (str): Path to raw survey.csv
        output_filepath (str, optional): Path to save survey_cleaned.csv
        
    Returns:
        pd.DataFrame: Cleaned, analysis-ready DataFrame
    """
    df_raw = load_raw_data(raw_filepath)
    
    # Apply sequential transformations
    df_clean = clean_age(df_raw, min_age=18, max_age=75)
    df_clean = create_age_groups(df_clean)
    df_clean = clean_gender(df_clean)
    df_clean = handle_missing_values(df_clean)
    df_clean = convert_timestamps(df_clean)
    
    if output_filepath:
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df_clean.to_csv(output_filepath, index=False)
        print(f"Cleaned dataset saved successfully to: {output_filepath}")
        
    return df_clean


def generate_data_dictionary(df_raw, df_cleaned, output_filepath=None):
    """
    Generate comprehensive data dictionary comparing raw and engineered variables.
    
    Args:
        df_raw (pd.DataFrame): Raw survey DataFrame
        df_cleaned (pd.DataFrame): Cleaned survey DataFrame
        output_filepath (str, optional): Path to save data_dictionary.csv
        
    Returns:
        pd.DataFrame: Data dictionary DataFrame
    """
    descriptions = {
        "Timestamp": "Date and time of survey submission",
        "Age": "Reported age of respondent in years (raw)",
        "Gender": "Reported gender identity (raw free text)",
        "Country": "Respondent country of residence",
        "state": "US state or territory (if applicable, else Outside US)",
        "self_employed": "Whether the respondent is self-employed (Yes/No)",
        "family_history": "Family history of mental health illness (Yes/No)",
        "treatment": "Whether respondent sought treatment for mental health (Yes/No)",
        "work_interfere": "Frequency of mental health interfering with work (Often, Sometimes, Rarely, Never, Not Applicable)",
        "no_employees": "Company size by employee count bracket",
        "remote_work": "Works remotely at least 50% of the time (Yes/No)",
        "tech_company": "Primary employer is a technology company (Yes/No)",
        "benefits": "Employer provides mental health benefits (Yes/No/Don't know)",
        "care_options": "Knowledge of mental health care options provided by employer (Yes/No/Not sure)",
        "wellness_program": "Employer has discussed mental health in wellness program (Yes/No/Don't know)",
        "seek_help": "Employer provides resources to seek help (Yes/No/Don't know)",
        "anonymity": "Anonymity is protected if taking advantage of resources (Yes/No/Don't know)",
        "leave": "Ease of taking medical leave for a mental health condition",
        "mental_health_consequence": "Discussing mental health with employer has negative consequences (Yes/No/Maybe)",
        "phys_health_consequence": "Discussing physical health with employer has negative consequences (Yes/No/Maybe)",
        "coworkers": "Willingness to discuss mental health with coworkers (Yes/No/Some of them)",
        "supervisor": "Willingness to discuss mental health with direct supervisor (Yes/No/Some of them)",
        "mental_health_interview": "Would bring up mental health with potential employer in interview (Yes/No/Maybe)",
        "phys_health_interview": "Would bring up physical health with potential employer in interview (Yes/No/Maybe)",
        "mental_vs_physical": "Employer takes mental health as seriously as physical health (Yes/No/Don't know)",
        "obs_consequence": "Observed negative consequences for coworkers with mental conditions (Yes/No)",
        "comments": "Optional open-ended comments or additional notes",
        "Age_Cleaned": "Cleaned respondent age with extreme outliers imputed using median (31)",
        "Age_Group": "Binned age cohorts: 18-24, 25-34, 35-44, 45-54, 55+",
        "Gender_Cleaned": "Harmonized gender category: Male, Female, Non-Binary/Other",
        "has_comment": "Binary indicator whether respondent provided text comments (1=Yes, 0=No)",
        "Survey_Year": "Year of survey submission extracted from Timestamp",
        "Survey_Month": "Month of survey submission extracted from Timestamp"
    }
    
    category_types = {
        "Timestamp": "Temporal",
        "Age": "Numerical (Continuous)",
        "Gender": "Categorical (Nominal - Raw)",
        "Country": "Categorical (Geographic)",
        "state": "Categorical (Geographic)",
        "self_employed": "Categorical (Binary)",
        "family_history": "Categorical (Binary)",
        "treatment": "Categorical (Binary - Target)",
        "work_interfere": "Categorical (Ordinal)",
        "no_employees": "Categorical (Ordinal)",
        "remote_work": "Categorical (Binary)",
        "tech_company": "Categorical (Binary)",
        "benefits": "Categorical (Nominal)",
        "care_options": "Categorical (Nominal)",
        "wellness_program": "Categorical (Nominal)",
        "seek_help": "Categorical (Nominal)",
        "anonymity": "Categorical (Nominal)",
        "leave": "Categorical (Ordinal)",
        "mental_health_consequence": "Categorical (Nominal)",
        "phys_health_consequence": "Categorical (Nominal)",
        "coworkers": "Categorical (Nominal)",
        "supervisor": "Categorical (Nominal)",
        "mental_health_interview": "Categorical (Nominal)",
        "phys_health_interview": "Categorical (Nominal)",
        "mental_vs_physical": "Categorical (Nominal)",
        "obs_consequence": "Categorical (Binary)",
        "comments": "Text (Unstructured)",
        "Age_Cleaned": "Numerical (Continuous - Cleaned)",
        "Age_Group": "Categorical (Ordinal)",
        "Gender_Cleaned": "Categorical (Nominal)",
        "has_comment": "Numerical (Binary Flag)",
        "Survey_Year": "Temporal / Integer",
        "Survey_Month": "Temporal / Integer"
    }
    
    records = []
    for col in df_cleaned.columns:
        if col in df_raw.columns:
            miss_count = int(df_raw[col].isnull().sum())
            miss_pct = round((miss_count / len(df_raw)) * 100, 2)
        else:
            miss_count = 0
            miss_pct = 0.0
            
        dtype_str = str(df_cleaned[col].dtype)
        unique_cnt = int(df_cleaned[col].nunique())
        desc = descriptions.get(col, "Survey attribute")
        cat_type = category_types.get(col, "Categorical")
        
        records.append({
            "column_name": col,
            "data_type": dtype_str,
            "description": desc,
            "category_type": cat_type,
            "missing_count": miss_count,
            "missing_percentage": miss_pct,
            "unique_count": unique_cnt
        })
        
    dict_df = pd.DataFrame(records)
    if output_filepath:
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        dict_df.to_csv(output_filepath, index=False)
        print(f"Data dictionary saved successfully to: {output_filepath}")
        
    return dict_df


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    raw_csv = os.path.join(project_root, "data", "raw", "survey.csv")
    cleaned_csv = os.path.join(project_root, "data", "processed", "survey_cleaned.csv")
    dict_csv = os.path.join(project_root, "data", "processed", "data_dictionary.csv")
    
    df_raw = load_raw_data(raw_csv)
    df_cleaned = clean_survey_data(raw_csv, cleaned_csv)
    generate_data_dictionary(df_raw, df_cleaned, dict_csv)
