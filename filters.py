
import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import gdown


def convert_damage(value):
    """Convert damage strings like '10K' or '2.5M' to numbers"""
    if pd.isna(value) or value == '' or value == 0:
        return 0
    if isinstance(value, (int, float)):
        return float(value)
    try:
        val_str = str(value).strip().upper()
        multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        if val_str[-1] in multipliers:
            num = float(val_str[:-1])
            return num * multipliers[val_str[-1]]
        else:
            return float(val_str)
    except:
        return 0


@st.cache_resource
def load_data(data_folder):
    """Download compiled CSV from Google Drive if not present, then load it."""
    file_path = os.path.join(data_folder, "compiled.csv")

    if not os.path.exists(file_path):
        os.makedirs(data_folder, exist_ok=True)
        gdown.download(
            "https://drive.google.com/uc?id=1Yi5Wi4YWXIqmZvz7SGdlmnCxZoBddW0l",
            file_path,
            quiet=False
        )

    df = pd.read_csv(file_path, low_memory=False, encoding="latin-1")
    return _clean_data(df)


def _clean_data(df):
    # clean column names
    df.columns = df.columns.str.strip().str.lower()

    # parse dates
    if 'begin_date_time' in df.columns:
        df['begin_date_time'] = pd.to_datetime(df['begin_date_time'], errors='coerce')
        df['begin_date'] = df['begin_date_time']
    elif 'begin_date' in df.columns:
        df['begin_date'] = pd.to_datetime(df['begin_date'], errors='coerce')

    if 'end_date_time' in df.columns:
        df['end_date_time'] = pd.to_datetime(df['end_date_time'], errors='coerce')
        df['end_date'] = df['end_date_time']
    elif 'end_date' in df.columns:
        df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')

    # convert damage columns
    for col in ['damage_property', 'damage_crops']:
        if col in df.columns:
            df[col] = df[col].apply(convert_damage)

    # extract year
    if 'begin_date' in df.columns:
        df['year'] = df['begin_date'].dt.year
    else:
        df['year'] = np.nan

    # infer year from source filename if available
    if '_source_file' in df.columns:
        def _year_from_filename(name):
            if not isinstance(name, str):
                return None
            m = re.search(r'd(20\d{2}|19\d{2})', name)
            if m:
                try:
                    return int(m.group(1))
                except:
                    return None
            return None
        inferred = df['_source_file'].apply(_year_from_filename)
        df['year'] = df['year'].fillna(inferred)

    # fallback column mappings
    if 'fatality_location' in df.columns and 'state' not in df.columns:
        df['state'] = df['fatality_location']
    if 'fatality_type' in df.columns and 'event_type' not in df.columns:
        df['event_type'] = np.where(df['fatality_type'].isna(), 'Unknown', df['fatality_type'])

    # ensure required numeric columns exist
    for col in ['damage_property', 'damage_crops', 'deaths_direct', 'injuries_direct', 'magnitude']:
        if col not in df.columns:
            df[col] = 0

    # clean string columns
    if 'event_type' in df.columns:
        df['event_type'] = df['event_type'].astype(str).str.strip()
    if 'state' in df.columns:
        df['state'] = df['state'].astype(str).str.strip()

    # fill NaN damage with 0
    for col in ['damage_property', 'damage_crops']:
        if col in df.columns:
            df[col] = df[col].fillna(0)

    return df


def get_unique_values(df, column):
    """Get sorted unique values from a column for dropdowns"""
    if column not in df.columns:
        return []
    vals = df[column].dropna().astype(str).str.strip()
    vals = vals[vals != '']
    return sorted(vals.unique())


def apply_filters(df, year_range, states, event_types, search_term, damage_range):
    """Apply all sidebar filters to the dataframe"""
    filtered = df.copy()

    if year_range and 'year' in filtered.columns:
        filtered = filtered[
            (filtered['year'] >= year_range[0]) &
            (filtered['year'] <= year_range[1])
        ]

    if states and 'state' in filtered.columns:
        filtered = filtered[filtered['state'].isin(states)]

    if event_types and 'event_type' in filtered.columns:
        filtered = filtered[filtered['event_type'].isin(event_types)]

    if damage_range and 'damage_property' in filtered.columns:
        filtered = filtered[
            (filtered['damage_property'] >= damage_range[0]) &
            (filtered['damage_property'] <= damage_range[1])
        ]

    if search_term and search_term.strip() and 'event_type' in filtered.columns and 'state' in filtered.columns:
        search_lower = search_term.lower().strip()
        filtered = filtered[
            (filtered['event_type'].str.lower().str.contains(search_lower, na=False)) |
            (filtered['state'].str.lower().str.contains(search_lower, na=False))
        ]

    return filtered
