"""
Field handler utilities for multimarketplace upload system.

This module provides utilities for field processing, name mapping,
dropdown value translation, and field type validation.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import logging

from ..config.field_mappings import (
    get_field_mapping, get_dropdown_values, get_field_type,
    is_dropdown_field, is_boolean_field, is_numeric_field, is_image_field,
    get_boolean_values, get_all_dropdown_fields
)

logger = logging.getLogger(__name__)

class FieldHandler:
    """Handles field processing, mapping, and validation."""
    
    def __init__(self):
        self.validation_errors = []
        self.mapping_warnings = []
    
    def map_field_name(self, field_name: str, source_platform: str, target_platform: str) -> str:
        """Map field names between platforms."""
        mapped_name = get_field_mapping(field_name, source_platform, target_platform)
        
        if mapped_name != field_name:
            logger.info(f"Mapped '{field_name}' ({source_platform}) → '{mapped_name}' ({target_platform})")
        else:
            logger.debug(f"No mapping found for '{field_name}' ({source_platform} → {target_platform})")
        
        return mapped_name
    
    def validate_dropdown_value(self, value: str, field_name: str, platform: str = 'master_template') -> Tuple[bool, Optional[str]]:
        """Validate dropdown values against allowed options."""
        if not is_dropdown_field(field_name):
            return True, None  # Not a dropdown field, no validation needed
        
        dropdown_values = get_dropdown_values(field_name, platform)
        
        if not dropdown_values:
            logger.warning(f"No dropdown values found for field '{field_name}' on platform '{platform}'")
            return True, None  # No validation possible
        
        # Check exact match
        if value in dropdown_values:
            return True, None
        
        # Check case-insensitive match
        value_lower = value.lower()
        for option in dropdown_values:
            if option.lower() == value_lower:
                logger.info(f"Case-insensitive match found: '{value}' → '{option}'")
                return True, option
        
        # Check for partial matches (for user-friendly suggestions)
        suggestions = []
        for option in dropdown_values:
            if value_lower in option.lower() or option.lower() in value_lower:
                suggestions.append(option)
        
        if suggestions:
            logger.warning(f"Invalid value '{value}' for field '{field_name}'. Suggestions: {suggestions}")
            return False, suggestions[0] if len(suggestions) == 1 else None
        
        logger.error(f"Invalid value '{value}' for field '{field_name}'. Valid options: {dropdown_values}")
        return False, None
    
    def validate_numeric_field(self, value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """Validate numeric fields."""
        if not is_numeric_field(field_name):
            return True, None
        
        # Remove common non-numeric characters
        cleaned_value = re.sub(r'[^\d.,]', '', str(value))
        
        try:
            # Try to convert to float
            float(cleaned_value)
            return True, None
        except ValueError:
            logger.error(f"Invalid numeric value '{value}' for field '{field_name}'")
            return False, None
    
    def validate_boolean_field(self, value: str, field_name: str, platform: str = 'master_template') -> Tuple[bool, Optional[str]]:
        """Validate boolean fields."""
        if not is_boolean_field(field_name):
            return True, None
        
        boolean_values = get_boolean_values(platform)
        value_lower = str(value).lower()
        
        # Check for valid boolean values
        for option in boolean_values:
            if option.lower() == value_lower:
                return True, None
        
        # Check for common boolean representations
        if value_lower in ['true', 'false', '1', '0', 'yes', 'no', 'y', 'n']:
            return True, None
        
        logger.error(f"Invalid boolean value '{value}' for field '{field_name}'. Valid options: {boolean_values}")
        return False, None
    
    def validate_image_field(self, value: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """Validate image URL fields."""
        if not is_image_field(field_name):
            return True, None
        
        if not value or value.strip() == '':
            return True, None  # Empty values are allowed for optional image fields
        
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if url_pattern.match(value):
            return True, None
        
        # Check if it's a file path
        if Path(value).exists() or value.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return True, None
        
        logger.warning(f"Invalid image URL/path '{value}' for field '{field_name}'")
        return False, None
    
    def validate_field(self, value: str, field_name: str, platform: str = 'master_template') -> Tuple[bool, Optional[str]]:
        """Validate a field value based on its type."""
        field_type = get_field_type(field_name)
        
        if field_type == 'dropdown_fixed':
            return self.validate_dropdown_value(value, field_name, platform)
        elif field_type == 'boolean':
            return self.validate_boolean_field(value, field_name, platform)
        elif field_type == 'numeric':
            return self.validate_numeric_field(value, field_name)
        elif field_type == 'image_url':
            return self.validate_image_field(value, field_name)
        else:
            # Free text fields - no validation needed
            return True, None
    
    def translate_dropdown_value(self, value: str, field_name: str, source_platform: str, target_platform: str) -> str:
        """Translate dropdown values between platforms."""
        if source_platform == target_platform:
            return value
        
        # Get dropdown mappings for this field
        for category, mappings in get_dropdown_values(field_name, source_platform).items():
            if isinstance(mappings, dict) and value in mappings:
                translated_value = mappings[value]
                logger.info(f"Translated '{value}' ({source_platform}) → '{translated_value}' ({target_platform})")
                return translated_value
        
        # If no translation found, return original value
        logger.debug(f"No translation found for '{value}' ({source_platform} → {target_platform})")
        return value
    
    def process_field_mapping(self, df: 'pd.DataFrame', source_platform: str, target_platform: str) -> 'pd.DataFrame':
        """Process field name mapping for an entire DataFrame."""
        import pandas as pd
        
        if source_platform == target_platform:
            return df
        
        # Create a mapping dictionary for column names
        column_mapping = {}
        for column in df.columns:
            mapped_column = self.map_field_name(column, source_platform, target_platform)
            if mapped_column != column:
                column_mapping[column] = mapped_column
        
        # Rename columns
        if column_mapping:
            df = df.rename(columns=column_mapping)
            logger.info(f"Mapped {len(column_mapping)} columns from {source_platform} to {target_platform}")
        
        return df
    
    def add_dropdown_validation_to_excel(self, worksheet, field_name: str, platform: str = 'master_template'):
        """Add dropdown validation to Excel worksheet cells."""
        from openpyxl.worksheet.datavalidation import DataValidation
        
        dropdown_values = get_dropdown_values(field_name, platform)
        
        if not dropdown_values:
            logger.warning(f"No dropdown values found for field '{field_name}'")
            return
        
        # Create data validation
        validation = DataValidation(
            type="list",
            formula1=f'"{",".join(dropdown_values)}"',
            allow_blank=True,
            show_error_message=True,
            show_input_message=True,
            error_title="Invalid Value",
            error_message=f"Please select a value from the dropdown for {field_name}",
            prompt_title=f"{field_name} Options",
            prompt=f"Select a value for {field_name}"
        )
        
        # Add validation to worksheet
        worksheet.add_data_validation(validation)
        
        # Apply to the appropriate column (you'll need to determine the column)
        # This is a simplified version - in practice, you'd need to find the column index
        logger.info(f"Added dropdown validation for field '{field_name}' with {len(dropdown_values)} options")
    
    def get_field_suggestions(self, field_name: str, partial_value: str, platform: str = 'master_template') -> List[str]:
        """Get field value suggestions based on partial input."""
        if is_dropdown_field(field_name):
            dropdown_values = get_dropdown_values(field_name, platform)
            partial_lower = partial_value.lower()
            
            suggestions = []
            for option in dropdown_values:
                if partial_lower in option.lower():
                    suggestions.append(option)
            
            return suggestions[:5]  # Limit to 5 suggestions
        
        return []
    
    def get_field_help_text(self, field_name: str) -> str:
        """Get help text for a specific field."""
        field_type = get_field_type(field_name)
        
        if field_type == 'dropdown_fixed':
            dropdown_values = get_dropdown_values(field_name)
            return f"Select from predefined options: {', '.join(dropdown_values[:5])}{'...' if len(dropdown_values) > 5 else ''}"
        elif field_type == 'boolean':
            return "Select Yes or No"
        elif field_type == 'numeric':
            return "Enter a numeric value"
        elif field_type == 'image_url':
            return "Enter an image URL or file path"
        else:
            return "Enter text freely"
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get a summary of validation results."""
        return {
            'validation_errors': self.validation_errors,
            'mapping_warnings': self.mapping_warnings,
            'total_errors': len(self.validation_errors),
            'total_warnings': len(self.mapping_warnings)
        }
    
    def clear_validation_results(self):
        """Clear validation results."""
        self.validation_errors = []
        self.mapping_warnings = []

def create_field_handler() -> FieldHandler:
    """Create a new field handler instance."""
    return FieldHandler()

def validate_dataframe_fields(df: 'pd.DataFrame', platform: str = 'master_template') -> Dict[str, List[str]]:
    """Validate all fields in a DataFrame."""
    handler = FieldHandler()
    validation_results = {}
    
    for column in df.columns:
        errors = []
        for idx, value in df[column].items():
            if pd.notna(value):  # Only validate non-null values
                is_valid, suggestion = handler.validate_field(str(value), column, platform)
                if not is_valid:
                    errors.append(f"Row {idx+1}: '{value}' - {suggestion if suggestion else 'Invalid value'}")
        
        if errors:
            validation_results[column] = errors
    
    return validation_results 