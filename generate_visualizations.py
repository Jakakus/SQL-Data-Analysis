import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Set style
plt.style.use('seaborn-v0_8')
sns.set_theme()

# Create sample data
np.random.seed(42)

# 1. Monthly Sales Trend
def create_monthly_sales_trend():
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
    sales = np.random.normal(100000, 20000, len(dates)) * (1 + np.sin(np.linspace(0, 4*np.pi, len(dates)))/4)
    sales = sales + np.linspace(0, 20000, len(dates))  # Add upward trend
    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, sales, marker='o', linewidth=2)
    plt.title('Monthly Sales Trend 2023', fontsize=14, pad=20)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Sales ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('images/monthly_sales_trend.png', dpi=300, bbox_inches='tight')
    plt.close()

# 2. Customer Segmentation
def create_customer_segmentation():
    # Generate RFM-like data
    n_customers = 1000
    recency = np.random.exponential(30, n_customers)
    frequency = np.random.gamma(2, 2, n_customers)
    monetary = np.random.lognormal(4, 1, n_customers)
    
    plt.figure(figsize=(10, 8))
    scatter = plt.scatter(recency, frequency, c=monetary, cmap='viridis', 
                         alpha=0.6, s=100)
    plt.colorbar(scatter, label='Monetary Value ($)')
    plt.title('Customer Segmentation (RFM Analysis)', fontsize=14, pad=20)
    plt.xlabel('Recency (days)', fontsize=12)
    plt.ylabel('Frequency (purchases)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('images/customer_segmentation.png', dpi=300, bbox_inches='tight')
    plt.close()

# 3. Best Selling Products
def create_best_selling_products():
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E',
                'Product F', 'Product G', 'Product H', 'Product I', 'Product J']
    sales = np.random.lognormal(4, 0.5, len(products))
    sales = sorted(sales, reverse=True)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(products, sales)
    plt.title('Top 10 Best-Selling Products', fontsize=14, pad=20)
    plt.xlabel('Products', fontsize=12)
    plt.ylabel('Sales Volume', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('images/best_selling_products.png', dpi=300, bbox_inches='tight')
    plt.close()

# 4. Top Customer Spending
def create_top_customer_spending():
    customers = [f'Customer {i+1}' for i in range(10)]
    spending = np.random.lognormal(5, 0.3, len(customers))
    spending = sorted(spending, reverse=True)
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(customers, spending, color='#2ecc71')
    plt.title('Top 10 Customers by Spending', fontsize=14, pad=20)
    plt.xlabel('Customers', fontsize=12)
    plt.ylabel('Total Spending ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${int(height):,}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('images/top_customers_spending.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    # Create all visualizations
    create_monthly_sales_trend()
    create_customer_segmentation()
    create_best_selling_products()
    create_top_customer_spending()
    print("All visualizations have been generated successfully!") 