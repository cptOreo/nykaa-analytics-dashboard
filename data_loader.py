import pandas as pd
import numpy as np
import os

FINANCIAL_DATA = {
    'Fashion': {
        'GMV': {'FY22': 1751.6, 'FY23': 2569.6, 'FY24': 3385, 'FY25': 3804, 'FY26': 4954},
        'NSV': {'FY22': 572.8, 'FY23': 744.4, 'FY24': 988, 'FY25': 1125, 'FY26': 1447},
        'Revenue from Operations': {'FY22': 325.4, 'FY23': 434.7, 'FY24': 568, 'FY25': 675, 'FY26': 832},
        'Gross Profit': {'FY22': 255.5, 'FY23': 328.9, 'FY24': 443, 'FY25': 552, 'FY26': 692},
        'Fulfilment Expense': {'FY22': 63.1, 'FY23': 80.1, 'FY24': 110, 'FY25': 110, 'FY26': 162},
        'Marketing + S&D': {'FY22': 176.1, 'FY23': 232.8, 'FY24': 271, 'FY25': 354, 'FY26': 382},
        'Contribution Profit': {'FY22': 16.3, 'FY23': 16.1, 'FY24': 62, 'FY25': 89, 'FY26': 147},
        'Other Expenses': {'FY24': 164, 'FY25': 182, 'FY26': 185},
        'EBITDA': {'FY24': -102, 'FY25': -93, 'FY26': -37},
        'Orders (mn)': {'FY22': 5, 'FY23': 6, 'FY24': 7, 'FY25': 7.6, 'FY26': 10.1},
        'AOV': {'FY22': 3400, 'FY23': 3973, 'FY24': 4361, 'FY25': 4609, 'FY26': 4652},
        'AUTC (mn)': {'FY22': 1.8, 'FY23': 2.5, 'FY24': 3, 'FY25': 3.2, 'FY26': 4.3},
        'Owned Brand GMV': {'FY22': 137.2, 'FY23': 331.2, 'FY24': 415, 'FY25': 431, 'FY26': 388},
        'EBITDA Margin': {'FY23': -0.167, 'FY24': -0.103, 'FY25': -0.083, 'FY26': -0.026},
    },
    'Beauty': {
        'GMV': {'FY22': 5008.9, 'FY23': 6649.1, 'FY24': 9055, 'FY25': 11775, 'FY26': 14954},
        'NSV': {'FY22': 3082.3, 'FY23': 4076.5, 'FY24': 5362, 'FY25': 6674, 'FY26': 8504},
        'Revenue from Operations': {'FY22': 3399.7, 'FY23': 4482, 'FY24': 5810, 'FY25': 7251, 'FY26': 9139},
        'Gross Profit': {'FY22': 1372.7, 'FY23': 1890.7, 'FY24': 2292, 'FY25': 2912, 'FY26': 3801},
        'Fulfilment Expense': {'FY22': 325.1, 'FY23': 346.9, 'FY24': 496, 'FY25': 628, 'FY26': 794},
        'Marketing + S&D': {'FY22': 380, 'FY23': 464.2, 'FY24': 600, 'FY25': 813, 'FY26': 1092},
        'Contribution Profit': {'FY22': 667.5, 'FY23': 1079.6, 'FY24': 1195, 'FY25': 1471, 'FY26': 1916},
        'Other Expenses': {'FY24': 730, 'FY25': 878, 'FY26': 1097},
        'EBITDA': {'FY24': 466, 'FY25': 593, 'FY26': 819},
        'Orders (mn)': {'FY22': 26.5, 'FY23': 34.8, 'FY24': 43.7, 'FY25': 54.5, 'FY26': 65.8},
        'AOV': {'FY22': 1857, 'FY23': 1857, 'FY24': 1985, 'FY25': 2021, 'FY26': 2068},
        'AUTC (mn)': {'FY22': 8, 'FY23': 10, 'FY24': 12.4, 'FY25': 15.8, 'FY26': 19.7},
        'Owned Brand GMV': {'FY22': 557.8, 'FY23': 788.9, 'FY24': 1095, 'FY25': 1695, 'FY26': 2788},
        'EBITDA Margin': {'FY23': 0.092, 'FY24': 0.087, 'FY25': 0.089, 'FY26': 0.096},
    }
}

def load_financial_data():
    """
    Creates a clean financial DataFrame in long format: year, segment, metric, value.
    Hardcodes the data as requested for reliability instead of parsing Excel.
    """
    rows = []
    for segment, metrics in FINANCIAL_DATA.items():
        for metric, years in metrics.items():
            for year, value in years.items():
                rows.append({
                    'year': year,
                    'segment': segment,
                    'metric': metric,
                    'value': float(value) if not pd.isna(value) else np.nan
                })
    return pd.DataFrame(rows)

def get_financial_df():
    """Returns the financial DataFrame in long format: year, segment, metric, value"""
    return load_financial_data()

def get_wide_financial_df():
    """Returns a pivoted version for easy segment comparison"""
    df = get_financial_df()
    # Pivot table to have segments as columns
    wide_df = df.pivot_table(index=['year', 'metric'], columns='segment', values='value').reset_index()
    return wide_df

def load_customer_data():
    """
    Reads the CSV file and returns a cleaned DataFrame.
    """
    csv_path = '/run/media/ravid/New Volume/mrv/dashboard/Nykaa_Primary_Research_Dash_Long_200(1).csv'
    
    if not os.path.exists(csv_path):
        print(f"Warning: CSV file not found at {csv_path}")
        return pd.DataFrame()
        
    df = pd.read_csv(csv_path)
    
    # Clean column names
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
    
    # Convert numeric columns properly, errors='coerce' to turn unparseable to NaN
    numeric_cols = [
        'monthly_spend_mid_inr', 'aov_mid_inr', 'return_rate', 
        'repurchase_intent_3m_1_5', 'share_requirements_mid_pct'
    ]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

def get_years():
    """Returns the list of financial years used in the dataset."""
    return ['FY22', 'FY23', 'FY24', 'FY25', 'FY26']
