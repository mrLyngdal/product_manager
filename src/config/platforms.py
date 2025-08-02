"""
Platform configurations for multimarketplace upload system.

This module contains all platform-specific configurations including:
- Required fields for each platform
- Language mappings
- Field mappings
- Output file specifications
"""

from typing import Dict, List, Optional

class PlatformConfig:
    """Configuration class for marketplace platforms."""
    
    def __init__(self, name: str, required_fields: List[str], 
                 language_fields: Dict[str, Optional[str]], 
                 image_fields: List[str], output_filename: str):
        self.name = name
        self.required_fields = required_fields
        self.language_fields = language_fields
        self.image_fields = image_fields
        self.output_filename = output_filename

# Platform configurations
PLATFORM_CONFIGS = {
    'castorama_fr': PlatformConfig(
        name='Castorama FR',
        required_fields=['EAN', 'Brand', 'Product Title (Mirakl)', 'Description (Mirakl)'],
        language_fields={
            'title': 'Product Title (Mirakl)',
            'description': 'Description (Mirakl)',
            'short_desc': None,
            'long_desc': None
        },
        image_fields=['Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5'],
        output_filename='Castorama_FR_generated.xlsx'
    ),
    
    'castorama_pl': PlatformConfig(
        name='Castorama PL',
        required_fields=['EAN', 'Brand', 'Code for internal use', 'Category'],
        language_fields={
            'title': 'Code for internal use',
            'description': 'Description (Mirakl)',
            'short_desc': None,
            'long_desc': None
        },
        image_fields=['Image 1', 'Image 2', 'Image 3'],
        output_filename='Castorama_PL_generated.xlsx'
    ),
    
    'leroy_merlin': PlatformConfig(
        name='Leroy Merlin',
        required_fields=['EAN', 'Brand', 'Product Title (Mirakl)', 'Category'],
        language_fields={
            'title': 'Product Title (Mirakl)',
            'description': 'Description (Mirakl)',
            'short_desc': None,
            'long_desc': None
        },
        image_fields=['Image 1', 'Image 2', 'Image 3', 'Image 4'],
        output_filename='LM_product_generated.xlsx'
    ),
    
    'maxeda_be': PlatformConfig(
        name='Maxeda BE',
        required_fields=['EAN', 'Brand', 'Product Title (fr_BE)', 'Description (fr_BE)'],
        language_fields={
            'title': 'Product Title (fr_BE)',
            'description': 'Description (fr_BE)',
            'short_desc': 'Short Description (fr_BE)',
            'long_desc': None
        },
        image_fields=['Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5'],
        output_filename='Maxeda_BE_generated.xlsx'
    ),
    
    'maxeda_nl': PlatformConfig(
        name='Maxeda NL',
        required_fields=['EAN', 'Brand', 'Product Title (nl_NL)', 'Description (nl_NL)'],
        language_fields={
            'title': 'Product Title (nl_NL)',
            'description': 'Description (nl_NL)',
            'short_desc': 'Short Description (nl_NL)',
            'long_desc': None
        },
        image_fields=['Image 1', 'Image 2', 'Image 3', 'Image 4'],
        output_filename='Maxeda_NL_generated.xlsx'
    )
}

# Language mapping for translation
LANGUAGE_MAPPING = {
    'castorama_fr': 'fr',
    'castorama_pl': 'pl',
    'leroy_merlin': 'fr',  # Leroy Merlin is primarily French
    'maxeda_be': 'fr',     # Belgian French
    'maxeda_nl': 'nl'      # Dutch
}

# Common columns that are typically needed for all platforms
COMMON_COLUMNS = [
    'EAN', 'Brand', 'Category', 'Product weight (kg)', 
    'Product height (mm)', 'Product width (mm)', 'Product length (mm)',
    'Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5'
]

def get_platform_config(platform: str) -> Optional[PlatformConfig]:
    """Get platform configuration by platform key."""
    return PLATFORM_CONFIGS.get(platform)

def get_language_for_platform(platform: str) -> Optional[str]:
    """Get target language for a platform."""
    return LANGUAGE_MAPPING.get(platform)

def get_all_platforms() -> List[str]:
    """Get list of all supported platforms."""
    return list(PLATFORM_CONFIGS.keys())

def get_platform_columns(platform: str) -> List[str]:
    """Get list of columns needed for a specific platform."""
    config = get_platform_config(platform)
    if not config:
        return []
    
    # Start with common columns
    columns = COMMON_COLUMNS.copy()
    
    # Add platform-specific language fields
    for field_type, field_name in config.language_fields.items():
        if field_name:
            columns.append(field_name)
    
    return columns 