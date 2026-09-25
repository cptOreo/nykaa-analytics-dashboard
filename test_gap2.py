import pandas as pd
from data_loader import load_customer_data
from kpi_calculations import calculate_repeat_purchase_rate
df = load_customer_data()
f_rep = calculate_repeat_purchase_rate(df, 'Fashion')
b_rep = calculate_repeat_purchase_rate(df, 'Beauty')
print(f"f_rep: {f_rep} ({type(f_rep)}), b_rep: {b_rep} ({type(b_rep)})")
