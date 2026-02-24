# Sample Data Files

Esta carpeta contiene archivos de ejemplo para testear los diferentes readers del EDA-toolkit.

## Archivos Disponibles

### 1. `example.csv`
- **Formato**: CSV (Comma-Separated Values)
- **Contenido**: Información de empleados (10 registros)
- **Columnas**: id, name, age, department, salary, hire_date
- **Reader**: `CSVReader`
- **Encoding**: UTF-8

### 2. `example.tsv`
- **Formato**: TSV (Tab-Separated Values)
- **Contenido**: Inventario de productos (8 registros)
- **Columnas**: id, product, category, price, stock, last_updated
- **Reader**: `TSVReader`
- **Delimiter**: `\t` (tab)

### 3. `example_pipe.txt`
- **Formato**: Pipe-delimited text file
- **Contenido**: Órdenes de compra (7 registros)
- **Columnas**: order_id, customer_name, city, country, total_amount, order_date, status
- **Reader**: `PipeReader`
- **Delimiter**: `|` (pipe)

### 4. `example.json`
- **Formato**: JSON (JavaScript Object Notation)
- **Contenido**: Transacciones comerciales (3 registros)
- **Estructura**: Array de objetos con datos anidados
- **Reader**: `JSONReader`
- **Features**: Datos jerárquicos (customer, items)

### 5. `example.html`
- **Formato**: HTML con múltiples tablas
- **Contenido**: Reporte empresarial con 3 tablas:
  - Tabla 1: Employee Information (4 registros)
  - Tabla 2: Department Budget 2025 (4 registros)
  - Tabla 3: Project Status (4 registros)
- **Reader**: `HTMLReader`
- **Features**: Múltiples tablas en un mismo archivo, formato HTML completo

### 6. `example.xlsx`
- **Formato**: Excel workbook (.xlsx)
- **Contenido**: Archivo con múltiples hojas (sheets):
  - Sheet 1: Sales Data (8 registros)
  - Sheet 2: Inventory (6 registros)
  - Sheet 3: Financials (5 registros)
- **Reader**: `ExcelReader`
- **Features**: Múltiples hojas, formatos numéricos, fechas

### 7. `example.parquet`
- **Formato**: Apache Parquet (columnar storage)
- **Contenido**: Datos de sensores IoT (10 registros)
- **Columnas**: sensor_id, timestamp, temperature, humidity, pressure, location
- **Reader**: `ParquetReader`
- **Features**: Formato eficiente, compresión automática

## Uso

### Ejemplo con Factory Pattern
```python
from pandas_toolkit.io.factory import ReaderFactory

# Automáticamente detecta el formato
factory = ReaderFactory()

# CSV
df_csv = factory.read("sample_data/example.csv")

# Excel - todas las hojas
dfs_excel = factory.read("sample_data/example.xlsx").read_all()

# HTML - todas las tablas
dfs_html = factory.read("sample_data/example.html").read_all()

# JSON
df_json = factory.read("sample_data/example.json")

# Parquet
df_parquet = factory.read("sample_data/example.parquet")
```

### Ejemplo con Readers Específicos
```python
from pandas_toolkit.io.readers import (
    CSVReader, ExcelReader, HTMLReader, 
    JSONReader, ParquetReader, TSVReader, PipeReader
)

# CSV
csv_reader = CSVReader("sample_data/example.csv")
df_employees = csv_reader.read()

# Excel - leer hoja específica
excel_reader = ExcelReader("sample_data/example.xlsx")
df_sales = excel_reader.read(sheet_name="Sales Data")

# Excel - leer todas las hojas
all_sheets = excel_reader.read_all()

# HTML - leer todas las tablas
html_reader = HTMLReader("sample_data/example.html")
tables = html_reader.read_all()

# JSON
json_reader = JSONReader("sample_data/example.json")
df_transactions = json_reader.read()

# TSV
tsv_reader = TSVReader("sample_data/example.tsv")
df_products = tsv_reader.read()

# Pipe-delimited
pipe_reader = PipeReader("sample_data/example_pipe.txt")
df_orders = pipe_reader.read()

# Parquet
parquet_reader = ParquetReader("sample_data/example.parquet")
df_sensors = parquet_reader.read()
```

### Ejemplo con Export
```python
from pandas_toolkit.io.exporter import FileExporter

exporter = FileExporter(output_dir="sample_data/exports", verbose=True)

# Export simple
exporter.export(df, method="csv", filename="output.csv")
exporter.export(df, method="excel", filename="output.xlsx")

# Export múltiples tablas
html_reader = HTMLReader("sample_data/example.html")
tables = html_reader.read_all()
exporter.export_tables(tables, filename="all_tables.xlsx")

# Export con split automático (tablas grandes)
large_df = pd.DataFrame(...)  # DataFrame con millones de filas
exporter.export_tables(large_df, filename="large_data.xlsx", max_rows_per_sheet=1000000)
```

## Nota

Esta carpeta está en `.gitignore` para uso interno de testing. Los archivos no se suben al repositorio.
