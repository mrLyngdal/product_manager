"""
Core transformation logic - minimalistic and simple.
Maps input data to platform-specific Excel files based on mapping configuration.
"""

import pandas as pd
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter, column_index_from_string
from pathlib import Path
from typing import Dict, List, Optional
import logging

from .config import (
    MAPPING_FILE, ATTRIBUTES_FILE, REF_TEMPLATES,
    INPUT_DIR, OUTPUT_DIR, get_output_file_path
)

logger = logging.getLogger(__name__)


def load_mapping() -> Dict[str, Dict[str, str]]:
    """
    Load column mappings from mapping.xlsx.
    
    Returns:
        Dict structure: {attribute_name: {platform: column_letter}}
        Example: {'height': {'castorama_fr': 'BM', 'leroy_merlin': 'AU'}}
    """
    try:
        df = pd.read_excel(MAPPING_FILE, sheet_name='Column_Mappings')
        
        # Get all platform columns (everything ending with '_column')
        platform_columns = [col for col in df.columns if col.endswith('_column')]
        
        mapping = {}
        for _, row in df.iterrows():
            attribute = str(row['attribute_name']).strip()
            value_type = str(row['input_type']).strip()  # Still called input_type in Excel, but represents value_type
            data_source = str(row['data_source']).strip() if 'data_source' in row and pd.notna(row.get('data_source')) else 'input_file'
            
            platform_mapping = {}
            for col in platform_columns:
                # Extract platform name from column (e.g., 'castorama_fr_column' -> 'castorama_fr')
                platform = col.replace('_column', '')
                column_letter = str(row[col]).strip() if pd.notna(row[col]) else ''
                
                if column_letter:
                    platform_mapping[platform] = column_letter
            
            mapping[attribute] = {
                'value_type': value_type,  # 'same' or 'platform_specific'
                'data_source': data_source,  # 'input_file' or 'punch_card'
                'columns': platform_mapping
            }
        
        logger.info(f"Loaded {len(mapping)} attribute mappings")
        return mapping
        
    except Exception as e:
        logger.error(f"Error loading mapping file: {e}")
        return {}


def load_attributes() -> Dict[str, Dict]:
    """
    Load pre-determined attribute values from attributes.xlsx.
    
    Returns:
        Dict with two keys:
        - 'same': {attribute_name: value} for same-input attributes
        - 'platform_specific': {attribute_name: {platform: value}} for platform-specific attributes
    """
    try:
        attributes = {
            'same': {},
            'platform_specific': {}
        }
        
        # Load same-input attributes
        same_df = pd.read_excel(ATTRIBUTES_FILE, sheet_name='Same_Input_Attributes')
        for _, row in same_df.iterrows():
            attr_name = str(row['attribute_name']).strip()
            value = row['value']
            if pd.notna(value):
                attributes['same'][attr_name] = value
        
        # Load platform-specific attributes
        platform_df = pd.read_excel(ATTRIBUTES_FILE, sheet_name='Platform_Specific_Attributes')
        for _, row in platform_df.iterrows():
            attr_name = str(row['attribute_name']).strip()
            
            # Get all platform value columns
            platform_values = {}
            for col in platform_df.columns:
                if col.endswith('_value') and col != 'attribute_name':
                    platform = col.replace('_value', '')
                    value = row[col]
                    if pd.notna(value) and str(value).strip():
                        platform_values[platform] = str(value).strip()
            
            if platform_values:
                attributes['platform_specific'][attr_name] = platform_values
        
        logger.info(f"Loaded {len(attributes['same'])} same-input attributes")
        logger.info(f"Loaded {len(attributes['platform_specific'])} platform-specific attributes")
        return attributes
        
    except Exception as e:
        logger.error(f"Error loading attributes file: {e}")
        return {'same': {}, 'platform_specific': {}}


def load_input(input_file: str) -> pd.DataFrame:
    """
    Load product input file.
    
    Args:
        input_file: Filename in data/input/ directory (e.g., 'acoustic_panels.xlsx')
    
    Returns:
        DataFrame with one row per product
    """
    try:
        input_path = INPUT_DIR / input_file
        df = pd.read_excel(input_path)
        logger.info(f"Loaded {len(df)} products from {input_file}")
        return df
    except Exception as e:
        logger.error(f"Error loading input file {input_file}: {e}")
        return pd.DataFrame()


def load_reference_template(platform: str) -> Optional[openpyxl.Workbook]:
    """
    Load reference template for a platform preserving exact structure.
    
    Args:
        platform: Platform identifier (e.g., 'castorama_fr')
    
    Returns:
        openpyxl Workbook object with all sheets, formatting, etc., or None if not found
    """
    try:
        ref_path = REF_TEMPLATES.get(platform)
        if not ref_path or not ref_path.exists():
            logger.error(f"Reference template not found for {platform}: {ref_path}")
            return None
        
        # Load workbook preserving all formatting, sheets, etc.
        wb = load_workbook(ref_path)
        
        logger.info(f"Loaded reference template for {platform} with {len(wb.sheetnames)} sheet(s)")
        return wb
        
    except Exception as e:
        logger.error(f"Error loading reference template for {platform}: {e}")
        return None


def transform_product(
    product_row: pd.Series,
    platform: str,
    mapping: Dict,
    attributes: Dict
) -> Dict[str, any]:
    """
    Transform one product row to platform-specific values.
    
    Args:
        product_row: Single row from input DataFrame
        platform: Target platform identifier
        mapping: Column mapping dictionary from load_mapping()
        attributes: Attribute values from load_attributes()
    
    Returns:
        Dict mapping column names/indices to values: {column_name: value}
    """
    result = {}
    
    for attribute, attr_config in mapping.items():
        value_type = attr_config['value_type']  # 'same' or 'platform_specific'
        data_source = attr_config['data_source']  # 'input_file' or 'punch_card'
        columns = attr_config['columns']
        
        # Get target column for this platform
        if platform not in columns:
            continue
        
        column_letter = columns[platform]
        
        # Determine value based on data_source and value_type
        value = None
        
        if data_source == 'punch_card':
            # Get value from attributes file (punch card)
            if value_type == 'same':
                if attribute in attributes['same']:
                    value = attributes['same'][attribute]
            elif value_type == 'platform_specific':
                if attribute in attributes['platform_specific']:
                    platform_values = attributes['platform_specific'][attribute]
                    if platform in platform_values:
                        value = platform_values[platform]
        
        elif data_source == 'input_file':
            # Get value from input file (product row)
            if attribute in product_row.index and pd.notna(product_row[attribute]):
                value = product_row[attribute]
        
        # Skip if no value found
        if value is None:
            continue
        
        # Store with column letter as key (will be converted to column name/index later)
        result[column_letter] = value
    
    return result


def generate_platform_file(platform: str, input_file: str) -> Optional[Path]:
    """
    Generate platform-specific output file, preserving exact structure from reference template.
    
    Args:
        platform: Platform identifier
        input_file: Input filename (e.g., 'acoustic_panels.xlsx')
    
    Returns:
        Path to generated file, or None if failed
    """
    try:
        # Load all configurations
        mapping = load_mapping()
        attributes = load_attributes()
        input_df = load_input(input_file)
        ref_wb = load_reference_template(platform)
        
        if ref_wb is None:
            logger.error(f"Cannot generate file for {platform}: reference template not found")
            return None
        
        if input_df.empty:
            logger.warning(f"No input data to transform")
            return None
        
        # Get the active sheet (first sheet, or you can specify which sheet to use)
        ws = ref_wb.active
        
        # Find the last row with data (to know where to start adding new rows)
        # Usually row 1 is headers, row 2+ is data
        last_data_row = 1
        for row in range(2, ws.max_row + 1):
            if any(cell.value is not None for cell in ws[row]):
                last_data_row = row
        
        # Clear existing data rows (keep header row at row 1)
        # Delete rows from 2 to last_data_row
        if last_data_row > 1:
            ws.delete_rows(2, last_data_row - 1)
        
        # Transform each product and add to worksheet
        next_row = 2  # Start after header row
        for idx, product_row in input_df.iterrows():
            # Get column mappings for this product (returns {column_letter: value})
            column_values = transform_product(product_row, platform, mapping, attributes)
            
            # Auto-map EAN to shop_sku if EAN exists in input and shop_sku is mapped
            if 'ean' in product_row.index and pd.notna(product_row['ean']):
                if 'shop_sku' in mapping and platform in mapping['shop_sku']['columns']:
                    shop_sku_col = mapping['shop_sku']['columns'][platform]
                    column_values[shop_sku_col] = product_row['ean']
                    logger.debug(f"Auto-mapped EAN to shop_sku column {shop_sku_col}")
            
            # Write values to the correct columns
            for col_letter, value in column_values.items():
                try:
                    # Convert column letter to column index (1-based for openpyxl)
                    col_idx = column_index_from_string(col_letter)
                    # Write value to cell
                    ws.cell(row=next_row, column=col_idx, value=value)
                except Exception as e:
                    logger.warning(f"Error writing to column {col_letter} at row {next_row}: {e}")
            
            next_row += 1
        
        # Save output file (preserves all formatting, sheets, etc.)
        output_path = get_output_file_path(platform)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        ref_wb.save(output_path)
        
        logger.info(f"Generated {output_path} with {next_row - 2} product rows")
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating platform file for {platform}: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

