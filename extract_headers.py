import pandas as pd
import csv
from pathlib import Path

def extract_headers_from_excel(file_path):
    """Extract column headers from an Excel file."""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        # Get column headers
        headers = list(df.columns)
        print(f"Extracted {len(headers)} headers from {file_path}")
        return headers
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    # List of Excel files to process
    excel_files = [
        "Castorama_FR_upload.xlsx",
        "Castorama_PL_upload.xlsx", 
        "LM_product upload.xlsx",
        "Maxeda_BE_upload.xlsx",
        "Maxeda_NL_upload.xlsx"
    ]
    
    # Set to store all unique headers
    all_headers = set()
    
    # Extract headers from each file
    for file_path in excel_files:
        if Path(file_path).exists():
            headers = extract_headers_from_excel(file_path)
            all_headers.update(headers)
        else:
            print(f"File not found: {file_path}")
    
    # Convert to sorted list for consistent ordering
    unique_headers = sorted(list(all_headers))
    
    print(f"\nTotal unique headers found: {len(unique_headers)}")
    print("Headers:")
    for i, header in enumerate(unique_headers, 1):
        print(f"{i:3d}. {header}")
    
    # Create the CSV template
    output_file = "multimarketplace_master_template.csv"
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(unique_headers)
    
    print(f"\nCreated unified template: {output_file}")
    print(f"Template contains {len(unique_headers)} unique columns")

if __name__ == "__main__":
    main() 