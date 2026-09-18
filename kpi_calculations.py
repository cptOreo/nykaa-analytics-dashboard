import pandas as pd
import numpy as np
import math

def _is_valid(val):
    """Helper to check if a value is valid (not None and not NaN)"""
    if val is None:
        return False
    if isinstance(val, (float, np.floating)) and math.isnan(val):
        return False
    return True

def calculate_realisation(nsv, gmv):
    """NSV / GMV × 100"""
    return (nsv / gmv) * 100 if _is_valid(gmv) and gmv != 0 and _is_valid(nsv) else None

def calculate_gmv_leakage(nsv, gmv):
    """(1 - NSV/GMV) × 100"""
    return (1 - nsv / gmv) * 100 if _is_valid(gmv) and gmv != 0 and _is_valid(nsv) else None

def calculate_yoy_growth(current, previous):
    """(current/previous - 1) × 100"""
    return ((current / previous) - 1) * 100 if _is_valid(previous) and previous != 0 and _is_valid(current) else None

def calculate_gross_margin(gross_profit, nsv):
    """Gross Profit / NSV × 100"""
    return (gross_profit / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(gross_profit) else None

def calculate_fulfilment_pct(fulfilment, nsv):
    """Fulfilment / NSV × 100"""
    return (fulfilment / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(fulfilment) else None

def calculate_marketing_sd_pct(marketing_sd, nsv):
    """Marketing+S&D / NSV × 100"""
    return (marketing_sd / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(marketing_sd) else None

def calculate_contribution_margin(contribution_profit, nsv):
    """Contribution Profit / NSV × 100"""
    return (contribution_profit / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(contribution_profit) else None

def calculate_ebitda_margin(ebitda, nsv):
    """EBITDA / NSV × 100"""
    return (ebitda / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(ebitda) else None

def calculate_other_expenses_pct(other_exp, nsv):
    """Other Expenses / NSV × 100"""
    return (other_exp / nsv) * 100 if _is_valid(nsv) and nsv != 0 and _is_valid(other_exp) else None

def calculate_aov(gmv_cr, orders_mn):
    """GMV / Orders in ₹. Convert: (gmv_cr * 1e7) / (orders_mn * 1e6) = gmv_cr * 10 / orders_mn"""
    return (gmv_cr * 10 / orders_mn) if _is_valid(orders_mn) and orders_mn != 0 and _is_valid(gmv_cr) else None

def calculate_nsv_per_order(nsv_cr, orders_mn):
    """NSV / Orders in ₹"""
    return (nsv_cr * 10 / orders_mn) if _is_valid(orders_mn) and orders_mn != 0 and _is_valid(nsv_cr) else None

def calculate_contribution_per_order(contribution_cr, orders_mn):
    """Contribution Profit / Orders in ₹"""
    return (contribution_cr * 10 / orders_mn) if _is_valid(orders_mn) and orders_mn != 0 and _is_valid(contribution_cr) else None

def calculate_logistics_cost_per_order(fulfilment_cr, orders_mn):
    """Fulfilment Expense / Orders in ₹"""
    return (fulfilment_cr * 10 / orders_mn) if _is_valid(orders_mn) and orders_mn != 0 and _is_valid(fulfilment_cr) else None

def calculate_marketing_sd_per_order(marketing_sd_cr, orders_mn):
    """Marketing+S&D / Orders in ₹"""
    return (marketing_sd_cr * 10 / orders_mn) if _is_valid(orders_mn) and orders_mn != 0 and _is_valid(marketing_sd_cr) else None

def calculate_cac_proxy(marketing_sd_cr, autc_mn):
    """Marketing+S&D / AUTC in ₹. CAC proxy."""
    return (marketing_sd_cr * 10 / autc_mn) if _is_valid(autc_mn) and autc_mn != 0 and _is_valid(marketing_sd_cr) else None

def calculate_orders_per_customer(orders_mn, autc_mn):
    """Orders / AUTC"""
    return (orders_mn / autc_mn) if _is_valid(autc_mn) and autc_mn != 0 and _is_valid(orders_mn) else None

def calculate_breakeven_volume(other_exp_cr, contribution_per_order):
    """Other Expenses / Contribution per Order. Convert other_exp to ₹."""
    if not _is_valid(contribution_per_order) or contribution_per_order <= 0 or not _is_valid(other_exp_cr):
        return None
    return (other_exp_cr * 1e7) / contribution_per_order

def calculate_nsv_cagr(nsv_start, nsv_end, years=3):
    """((end/start)^(1/years) - 1) × 100"""
    if not _is_valid(nsv_start) or not _is_valid(nsv_end) or nsv_start <= 0:
        return None
    return ((nsv_end / nsv_start) ** (1 / years) - 1) * 100

def calculate_owned_brand_share(owned_brand_gmv, gmv):
    """Owned Brand GMV / GMV × 100"""
    return (owned_brand_gmv / gmv) * 100 if _is_valid(gmv) and gmv != 0 and _is_valid(owned_brand_gmv) else None

def calculate_return_rate_survey(df, category):
    """Average return_rate for a category"""
    filtered = df[df['category'] == category]
    return filtered['return_rate'].mean() * 100 if len(filtered) > 0 and 'return_rate' in df.columns else None

def calculate_repeat_purchase_rate(df, category):
    """% of respondents with repeat_purchase_flag == 1"""
    filtered = df[df['category'] == category]
    return filtered['repeat_purchase_flag'].mean() * 100 if len(filtered) > 0 and 'repeat_purchase_flag' in df.columns else None

def calculate_purchase_frequency(df, category):
    """Average orders_6m (use midpoint of band). Map bands to numeric midpoints."""
    # Map orders_6m_band to midpoints
    band_map = {'0': 0, '1': 1, '2': 2, '3–4': 3.5, '5–7': 6, '8–10': 9, '11+': 13}
    filtered = df[df['category'] == category].copy()
    if 'orders_6m_band' in filtered.columns:
        filtered['orders_numeric'] = filtered['orders_6m_band'].map(band_map)
        return filtered['orders_numeric'].mean() if len(filtered) > 0 else None
    return None

def calculate_aov_proxy(df, category):
    """Average aov_mid_inr"""
    filtered = df[df['category'] == category]
    return filtered['aov_mid_inr'].mean() if len(filtered) > 0 and 'aov_mid_inr' in df.columns else None

def calculate_share_of_wallet(df, category):
    """Average share_requirements_mid_pct"""
    filtered = df[df['category'] == category]
    return filtered['share_requirements_mid_pct'].mean() if len(filtered) > 0 and 'share_requirements_mid_pct' in df.columns else None

def calculate_repurchase_intent(df, category):
    """Average repurchase_intent_3m_1_5"""
    filtered = df[df['category'] == category]
    return filtered['repurchase_intent_3m_1_5'].mean() if len(filtered) > 0 and 'repurchase_intent_3m_1_5' in df.columns else None

def calculate_discount_dependence(df, category):
    """% of respondents whose first purchase motivation was discount/sale related"""
    # This is a proxy - we don't have a direct column. Use platform preferences instead.
    filtered = df[df['category'] == category]
    # For now, return None if column doesn't exist
    return None

def compute_all_financial_kpis(data_dict, year, segment):
    """Compute all KPIs for a given year and segment from the financial data dict.
    data_dict has structure: data_dict[segment][metric][year] = value
    Returns a dict of KPI name -> value"""
    if segment not in data_dict:
        return {}
        
    d = data_dict[segment]
    
    def get(metric, yr=year):
        val = d.get(metric, {}).get(yr)
        return val if _is_valid(val) else None
    
    gmv = get('GMV')
    nsv = get('NSV')
    gross_profit = get('Gross Profit')
    fulfilment = get('Fulfilment Expense')
    marketing_sd = get('Marketing + S&D')
    contribution = get('Contribution Profit')
    other_exp = get('Other Expenses')
    ebitda = get('EBITDA')
    orders_mn = get('Orders (mn)')
    autc_mn = get('AUTC (mn)')
    aov_reported = get('AOV')
    owned_brand = get('Owned Brand GMV')
    ebitda_margin_reported = get('EBITDA Margin')
    
    contrib_per_order = calculate_contribution_per_order(contribution, orders_mn) if _is_valid(contribution) and _is_valid(orders_mn) else None
    
    return {
        'GMV': gmv,
        'NSV': nsv,
        'Revenue from Operations': get('Revenue from Operations'),
        'Gross Profit': gross_profit,
        'Fulfilment Expense': fulfilment,
        'Marketing + S&D': marketing_sd,
        'Contribution Profit': contribution,
        'Other Expenses': other_exp,
        'EBITDA': ebitda,
        'Orders (mn)': orders_mn,
        'AUTC (mn)': autc_mn,
        'Realisation %': calculate_realisation(nsv, gmv),
        'GMV Leakage %': calculate_gmv_leakage(nsv, gmv),
        'Gross Margin %': calculate_gross_margin(gross_profit, nsv),
        'Fulfilment %': calculate_fulfilment_pct(fulfilment, nsv),
        'Marketing + S&D %': calculate_marketing_sd_pct(marketing_sd, nsv),
        'Contribution Margin %': calculate_contribution_margin(contribution, nsv),
        'Other Expenses %': calculate_other_expenses_pct(other_exp, nsv),
        'EBITDA Margin %': ebitda_margin_reported * 100 if _is_valid(ebitda_margin_reported) else (calculate_ebitda_margin(ebitda, nsv) if _is_valid(ebitda) and _is_valid(nsv) else None),
        'AOV (Reported)': aov_reported,
        'NSV per Order': calculate_nsv_per_order(nsv, orders_mn),
        'Contribution per Order': contrib_per_order,
        'Logistics Cost per Order': calculate_logistics_cost_per_order(fulfilment, orders_mn),
        'Marketing + S&D per Order': calculate_marketing_sd_per_order(marketing_sd, orders_mn),
        'CAC Proxy': calculate_cac_proxy(marketing_sd, autc_mn),
        'Orders per Customer': calculate_orders_per_customer(orders_mn, autc_mn),
        'Break-even Volume': calculate_breakeven_volume(other_exp, contrib_per_order) if _is_valid(other_exp) and _is_valid(contrib_per_order) else None,
        'Owned Brand Share %': calculate_owned_brand_share(owned_brand, gmv),
    }
