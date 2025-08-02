#!/usr/bin/env python3
"""
MVP Template Creator

Creates a minimal template with only the required fields across all platforms.
This allows for fast product uploads with minimal data entry.
"""

import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MVP Required Fields (common across all platforms)
MVP_FIELDS = [
    'Category Code',        # Maps to Category, Product Category
    'EAN',                 # All platforms require this
    'Product Title (Mirakl)',  # Maps to Name, Product Title FR/IT/ES/PT
    'Description (Mirakl)',    # Maps to Body Copy, Long Description
    'Image 1',            # Maps to Main Image 1, Image Large 1
    'Brand'               # Maps to Brand Name, Acquisition brand, Manufacturer Name
]

def create_mvp_template():
    """Create an MVP template with only the minimum required fields."""
    
    print("🎯 Creating MVP Template (Minimum Required Fields)")
    print("=" * 60)
    
    # Create empty DataFrame with MVP fields
    df = pd.DataFrame(columns=MVP_FIELDS)
    
    # Create output path
    output_path = Path('data/templates/multimarketplace_mvp_template.xlsx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Save as XLSX with styling
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='MVP Template', index=False)
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['MVP Template']
            
            # Apply styling
            _apply_mvp_styling(worksheet, MVP_FIELDS)
            _adjust_mvp_column_widths(worksheet)
            
        logger.info(f"✅ Created MVP template with {len(MVP_FIELDS)} fields")
        logger.info(f"📁 Output: {output_path}")
        
        print(f"\n✅ MVP Template Created Successfully!")
        print(f"📁 File: {output_path}")
        print(f"📊 Fields: {len(MVP_FIELDS)} minimum required fields")
        print("\n🎯 MVP Fields:")
        for i, field in enumerate(MVP_FIELDS, 1):
            print(f"   {i}. {field}")
        
        print("\n📝 Next Steps:")
        print("1. Fill in the MVP template with your product data")
        print("2. Run transformation to generate platform-specific files")
        print("3. Upload to marketplaces for fast product listing")
        print("4. Add additional fields later as needed")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating MVP template: {e}")
        print(f"❌ Error: {e}")
        return False

def _apply_mvp_styling(worksheet, fields):
    """Apply color coding to MVP template."""
    # Colors
    required_color = PatternFill(start_color='FFE6E6', end_color='FFE6E6', fill_type='solid')  # Light red
    
    # Apply red background to all MVP fields (all are required)
    for col_idx, field in enumerate(fields, 1):
        cell = worksheet.cell(row=1, column=col_idx)
        cell.fill = required_color
        cell.font = Font(bold=True)

def _adjust_mvp_column_widths(worksheet):
    """Adjust column widths for MVP template."""
    column_widths = {
        'A': 15,  # Category Code
        'B': 15,  # EAN
        'C': 40,  # Product Title
        'D': 60,  # Description
        'E': 20,  # Image 1
        'F': 15   # Brand
    }
    
    for col, width in column_widths.items():
        worksheet.column_dimensions[col].width = width

def main():
    """Main function to create MVP template."""
    success = create_mvp_template()
    
    if success:
        print("\n🎉 MVP Template ready for use!")
    else:
        print("\n❌ Failed to create MVP template")

if __name__ == "__main__":
    main() 