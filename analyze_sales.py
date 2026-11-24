from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'sample_sales.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)

sales = pd.read_csv(DATA, parse_dates=['date'])
sales['revenue'] = sales['quantity'] * sales['unit_price']
sales['month'] = sales['date'].dt.to_period('M').astype(str)

print('DATASET OVERVIEW')
print(f'Rows: {len(sales)}')
print(f'Total revenue: Rs. {sales["revenue"].sum():,.2f}')
print(f'Units sold: {sales["quantity"].sum()}')

monthly = sales.groupby('month', as_index=False)['revenue'].sum()
city = sales.groupby('city', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
category = sales.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
top_products = sales.groupby('product', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False).head(5)

monthly.to_csv(OUT / 'monthly_revenue.csv', index=False)
city.to_csv(OUT / 'city_revenue.csv', index=False)
category.to_csv(OUT / 'category_revenue.csv', index=False)
top_products.to_csv(OUT / 'top_products.csv', index=False)

print('\nREVENUE BY CITY')
print(city.to_string(index=False))
print('\nREVENUE BY CATEGORY')
print(category.to_string(index=False))
print('\nTOP PRODUCTS')
print(top_products.to_string(index=False))

plt.figure(figsize=(8, 4.5))
plt.bar(monthly['month'], monthly['revenue'])
plt.title('Monthly Revenue')
plt.xlabel('Month')
plt.ylabel('Revenue (INR)')
plt.tight_layout()
plt.savefig(OUT / 'monthly_revenue.png', dpi=160)
plt.close()

plt.figure(figsize=(7, 4.5))
plt.bar(category['category'], category['revenue'])
plt.title('Revenue by Category')
plt.xlabel('Category')
plt.ylabel('Revenue (INR)')
plt.tight_layout()
plt.savefig(OUT / 'category_revenue.png', dpi=160)
plt.close()

print(f'\nAnalysis complete. Results saved in: {OUT}')
