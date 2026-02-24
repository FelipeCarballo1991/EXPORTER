"""
Script to generate sample Excel and Parquet files for testing EDA-toolkit.
Run this script to create example.xlsx and example.parquet in the sample_data folder.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

# Create sample_data directory if it doesn't exist
output_dir = Path(__file__).parent
output_dir.mkdir(exist_ok=True)

print(f"Generating sample files in: {output_dir}")
print("-" * 50)

# ============================================================================
# 1. Excel File with Multiple Sheets
# ============================================================================
print("Creating example.xlsx...")

# Sheet 1: Sales Data
sales_data = {
    'sale_id': ['S001', 'S002', 'S003', 'S004', 'S005', 'S006', 'S007', 'S008'],
    'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam', 'Laptop', 'Monitor'],
    'quantity': [2, 15, 8, 3, 12, 5, 1, 2],
    'unit_price': [1299.99, 29.99, 79.99, 349.99, 149.99, 89.99, 1299.99, 349.99],
    'total': [2599.98, 449.85, 639.92, 1049.97, 1799.88, 449.95, 1299.99, 699.98],
    'sale_date': pd.to_datetime([
        '2025-02-10', '2025-02-11', '2025-02-12', '2025-02-13',
        '2025-02-14', '2025-02-15', '2025-02-16', '2025-02-17'
    ]),
    'customer_type': ['Corporate', 'Individual', 'Individual', 'Corporate', 
                      'Individual', 'Corporate', 'Individual', 'Corporate']
}
df_sales = pd.DataFrame(sales_data)

# Sheet 2: Inventory
inventory_data = {
    'sku': ['SKU-001', 'SKU-002', 'SKU-003', 'SKU-004', 'SKU-005', 'SKU-006'],
    'product_name': ['Laptop Pro', 'Wireless Mouse', 'Mechanical Keyboard', 
                     '4K Monitor', 'Noise Cancelling Headphones', 'HD Webcam'],
    'category': ['Computers', 'Accessories', 'Accessories', 
                 'Displays', 'Audio', 'Video'],
    'in_stock': [45, 230, 180, 75, 95, 60],
    'reorder_level': [20, 100, 80, 30, 50, 25],
    'warehouse_location': ['A-101', 'B-205', 'B-203', 'A-105', 'C-310', 'C-308']
}
df_inventory = pd.DataFrame(inventory_data)

# Sheet 3: Financial Summary
financial_data = {
    'month': ['January', 'February', 'March', 'April', 'May'],
    'revenue': [125000.50, 145000.75, 138000.25, 152000.00, 168000.80],
    'expenses': [78000.25, 82000.50, 79000.75, 85000.00, 88000.30],
    'profit': [46999.25, 63000.25, 59000.50, 67000.00, 79999.50],
    'profit_margin_%': [37.6, 43.4, 42.8, 44.1, 47.6]
}
df_financial = pd.DataFrame(financial_data)

# Write to Excel with multiple sheets
excel_path = output_dir / "example.xlsx"
with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
    df_sales.to_excel(writer, sheet_name='Sales Data', index=False)
    df_inventory.to_excel(writer, sheet_name='Inventory', index=False)
    df_financial.to_excel(writer, sheet_name='Financials', index=False)

print(f"  ✓ Created example.xlsx with 3 sheets:")
print(f"    - Sales Data: {df_sales.shape[0]} rows")
print(f"    - Inventory: {df_inventory.shape[0]} rows")
print(f"    - Financials: {df_financial.shape[0]} rows")

# ============================================================================
# 2. Parquet File (IoT Sensor Data)
# ============================================================================
print("\nCreating example.parquet...")

try:
    # Check if pyarrow is available
    import pyarrow
    
    # Generate timestamps
    base_time = datetime(2025, 2, 24, 10, 0, 0)
    timestamps = [base_time + timedelta(minutes=i*10) for i in range(10)]

    sensor_data = {
        'sensor_id': ['SENSOR-001', 'SENSOR-002', 'SENSOR-001', 'SENSOR-003', 'SENSOR-002',
                      'SENSOR-001', 'SENSOR-003', 'SENSOR-002', 'SENSOR-001', 'SENSOR-003'],
        'timestamp': timestamps,
        'temperature': [22.5, 23.1, 22.8, 21.9, 23.5, 22.6, 22.0, 23.8, 22.9, 21.7],
        'humidity': [45.2, 47.8, 46.5, 44.0, 48.2, 45.8, 43.5, 49.0, 46.2, 42.8],
        'pressure': [1013.25, 1012.80, 1013.10, 1014.00, 1012.50, 
                     1013.40, 1014.20, 1012.30, 1013.20, 1014.50],
        'location': ['Warehouse A', 'Warehouse B', 'Warehouse A', 'Office Floor 1', 'Warehouse B',
                     'Warehouse A', 'Office Floor 1', 'Warehouse B', 'Warehouse A', 'Office Floor 1']
    }
    df_sensors = pd.DataFrame(sensor_data)

    # Write to Parquet
    parquet_path = output_dir / "example.parquet"
    df_sensors.to_parquet(parquet_path, index=False, compression='snappy')

    print(f"  ✓ Created example.parquet:")
    print(f"    - {df_sensors.shape[0]} rows x {df_sensors.shape[1]} columns")
    print(f"    - Compression: snappy")
    print(f"    - Size: {parquet_path.stat().st_size / 1024:.2f} KB")
    
    parquet_created = True

except ImportError:
    print("  ⚠ Skipping example.parquet (pyarrow not installed)")
    print("    Install with: pip install pyarrow")
    parquet_created = False

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 50)
print("✓ All sample files created successfully!")
print("=" * 50)

print("\nGenerated files:")
print(f"  1. example.csv        - 10 employee records")
print(f"  2. example.tsv        - 8 product records")
print(f"  3. example_pipe.txt   - 7 order records")
print(f"  4. example.json       - 3 transaction records")
print(f"  5. example.html       - 3 tables (12 total records)")
print(f"  6. example.xlsx       - 3 sheets (19 total records)")
if parquet_created:
    print(f"  7. example.parquet    - 10 sensor readings")
else:
    print(f"  7. example.parquet    - SKIPPED (pyarrow not available)")

print("\nYou can now test these files with EDA-toolkit readers!")
print("See README.md in this folder for usage examples.")
