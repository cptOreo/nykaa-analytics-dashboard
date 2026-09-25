import pandas as pd
from data_loader import load_customer_data
from kpi_calculations import calculate_repeat_purchase_rate
df = load_customer_data()
f_rep = calculate_repeat_purchase_rate(df, 'Fashion')
b_rep = calculate_repeat_purchase_rate(df, 'Beauty')
print(f"Fashion: {f_rep}, Beauty: {b_rep}")
