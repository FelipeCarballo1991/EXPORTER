"""
Quick test script to verify all readers work with sample data files.
Tests each reader with its corresponding sample file.
"""

import sys
from pathlib import Path

# Add parent directory to path to import pandas_toolkit
sys.path.insert(0, str(Path(__file__).parent.parent))

from pandas_toolkit.io.factory import ReaderFactory
from pandas_toolkit.io.readers import (
    CSVReader, ExcelReader, HTMLReader, 
    JSONReader, TSVReader, PipeReader
)

def print_header(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_dataframe_info(df, name="DataFrame"):
    """Print basic info about a DataFrame."""
    print(f"\n{name}:")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    print(f"\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))

def test_csv_reader():
    """Test CSVReader with example.csv"""
    print_header("Testing CSVReader")
    
    try:
        reader = CSVReader(output_dir="sample_data/test_output")
        df = reader.read("sample_data/example.csv")
        print_dataframe_info(df, "Employee Data")
        print("\n✓ CSVReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ CSVReader: FAILED - {e}")
        return False

def test_tsv_reader():
    """Test TSVReader with example.tsv"""
    print_header("Testing TSVReader")
    
    try:
        reader = TSVReader(output_dir="sample_data/test_output")
        df = reader.read("sample_data/example.tsv")
        print_dataframe_info(df, "Product Inventory")
        print("\n✓ TSVReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ TSVReader: FAILED - {e}")
        return False

def test_pipe_reader():
    """Test PipeReader with example_pipe.txt"""
    print_header("Testing PipeReader")
    
    try:
        reader = PipeReader(output_dir="sample_data/test_output")
        df = reader.read("sample_data/example_pipe.txt")
        print_dataframe_info(df, "Order Data")
        print("\n✓ PipeReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ PipeReader: FAILED - {e}")
        return False

def test_json_reader():
    """Test JSONReader with example.json"""
    print_header("Testing JSONReader")
    
    try:
        reader = JSONReader(output_dir="sample_data/test_output")
        df = reader.read("sample_data/example.json")
        print_dataframe_info(df, "Transaction Data")
        print("\n✓ JSONReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ JSONReader: FAILED - {e}")
        return False

def test_html_reader():
    """Test HTMLReader with example.html"""
    print_header("Testing HTMLReader")
    
    try:
        reader = HTMLReader(output_dir="sample_data/test_output")
        
        # Test read() - first table
        df_first = reader.read("sample_data/example.html")
        print_dataframe_info(df_first, "First Table (Employee Information)")
        
        # Test read_all() - all tables
        all_tables = reader.read_all("sample_data/example.html")
        print(f"\n\nTotal tables found: {len(all_tables)}")
        for i, df in enumerate(all_tables, 1):
            print(f"\nTable {i}: {df.shape[0]} rows × {df.shape[1]} columns")
        
        print("\n✓ HTMLReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ HTMLReader: FAILED - {e}")
        return False

def test_excel_reader():
    """Test ExcelReader with example.xlsx"""
    print_header("Testing ExcelReader")
    
    try:
        reader = ExcelReader(output_dir="sample_data/test_output")
        
        # Test read() - first sheet
        df_first = reader.read("sample_data/example.xlsx")
        print_dataframe_info(df_first, "First Sheet (Sales Data)")
        
        # Test read_all() - all sheets
        all_sheets = reader.read_all("sample_data/example.xlsx")
        print(f"\n\nTotal sheets found: {len(all_sheets)}")
        for i, df in enumerate(all_sheets, 1):
            print(f"\nSheet {i}: {df.shape[0]} rows × {df.shape[1]} columns")
        
        print("\n✓ ExcelReader: SUCCESS")
        return True
    except Exception as e:
        print(f"\n✗ ExcelReader: FAILED - {e}")
        return False

def test_factory():
    """Test ReaderFactory with auto-detection"""
    print_header("Testing ReaderFactory (Auto-Detection)")
    
    test_files = [
        ("sample_data/example.csv", "CSV"),
        ("sample_data/example.tsv", "TSV"),
        ("sample_data/example.json", "JSON"),
        ("sample_data/example.html", "HTML"),
        ("sample_data/example.xlsx", "Excel"),
    ]
    
    results = []
    for filepath, format_name in test_files:
        try:
            reader = ReaderFactory.create_reader(filepath, output_dir="sample_data/test_output")
            df = reader.read(filepath)
            print(f"\n{format_name:10s} → {df.shape[0]:3d} rows × {df.shape[1]:2d} cols ✓")
            results.append(True)
        except Exception as e:
            print(f"\n{format_name:10s} → FAILED: {e}")
            results.append(False)
    
    if all(results):
        print("\n✓ ReaderFactory: SUCCESS (all formats detected)")
        return True
    else:
        print(f"\n⚠ ReaderFactory: PARTIAL ({sum(results)}/{len(results)} passed)")
        return False

def test_read_all_consistency():
    """Test that read_all() returns list for all readers"""
    print_header("Testing read_all() Consistency")
    
    test_cases = [
        ("CSV", CSVReader, "sample_data/example.csv"),
        ("TSV", TSVReader, "sample_data/example.tsv"),
        ("Pipe", PipeReader, "sample_data/example_pipe.txt"),
        ("JSON", JSONReader, "sample_data/example.json"),
        ("HTML", HTMLReader, "sample_data/example.html"),
        ("Excel", ExcelReader, "sample_data/example.xlsx"),
    ]
    
    results = []
    for reader_name, reader_class, filepath in test_cases:
        try:
            reader = reader_class(output_dir="sample_data/test_output")
            result = reader.read_all(filepath)
            is_list = isinstance(result, list)
            all_dfs = all(hasattr(df, 'shape') for df in result)
            
            print(f"\n{reader_name:10s} → Returns list: {is_list}, "
                  f"Count: {len(result)}, All DataFrames: {all_dfs}")
            
            results.append(is_list and all_dfs)
        except Exception as e:
            print(f"\n{reader_name:10s} → FAILED: {e}")
            results.append(False)
    
    if all(results):
        print("\n✓ read_all() Consistency: SUCCESS")
        return True
    else:
        print(f"\n⚠ read_all() Consistency: PARTIAL ({sum(results)}/{len(results)} passed)")
        return False

def main():
    """Run all tests."""
    print("\n" + "█" * 70)
    print("  EDA-TOOLKIT SAMPLE DATA TEST SUITE")
    print("█" * 70)
    
    results = {
        "CSVReader": test_csv_reader(),
        "TSVReader": test_tsv_reader(),
        "PipeReader": test_pipe_reader(),
        "JSONReader": test_json_reader(),
        "HTMLReader": test_html_reader(),
        "ExcelReader": test_excel_reader(),
        "ReaderFactory": test_factory(),
        "read_all() API": test_read_all_consistency(),
    }
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(results.values())
    total = len(results)
    
    print()
    for test_name, passed_test in results.items():
        status = "✓ PASS" if passed_test else "✗ FAIL"
        print(f"  {test_name:20s} {status}")
    
    print(f"\n{'─' * 70}")
    print(f"  Total: {passed}/{total} tests passed")
    print(f"{'─' * 70}\n")
    
    if passed == total:
        print("🎉 All tests passed! EDA-toolkit is working correctly.\n")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
