"""
Field mapping configurations for multimarketplace upload system.

This module contains field name mappings, dropdown value standardizations,
and field type classifications based on Phase 1 analysis.
"""

from typing import Dict, List, Any

# Field name mappings across platforms
FIELD_NAME_MAPPINGS = {
    # Colour variations
    'colour_fields': {
        'Castorama_FR': 'Colour',
        'Castorama_PL': 'Colour',
        'LM_product': 'Main Color',
        'master_template': 'Colour'
    },
    
    # Material variations
    'material_fields': {
        'Castorama_FR': 'Material',
        'Castorama_PL': 'Material',
        'Maxeda_NL': 'Material',
        'Maxeda_BE': 'Material',
        'LM_product': 'Main Material',
        'master_template': 'Material'
    },
    
    # Category variations
    'category_fields': {
        'Castorama_FR': 'Category',
        'Castorama_PL': 'Category',
        'Maxeda_NL': 'Category Code',
        'Maxeda_BE': 'Category Code',
        'LM_product': 'Product Category',
        'master_template': 'Category Code'
    },
    
    # Brand variations
    'brand_fields': {
        'Castorama_FR': 'Manufacturer Name',
        'Castorama_PL': 'Manufacturer Name',
        'Maxeda_NL': 'Brand Name',
        'Maxeda_BE': 'Brand Name',
        'LM_product': 'Brand',
        'master_template': 'Brand'
    },
    
    # Finish variations
    'finish_fields': {
        'Castorama_FR': 'Finish',
        'Maxeda_NL': 'Finish',
        'Maxeda_BE': 'Finish',
        'LM_product': 'Finishing of product',
        'master_template': 'Finish'
    },
    
    # Design variations
    'design_fields': {
        'Castorama_FR': 'Design',
        'Castorama_PL': 'Design',
        'master_template': 'Design'
    },
    
    # Effect variations
    'effect_fields': {
        'Castorama_FR': 'Effect',
        'Castorama_PL': 'Effect',
        'LM_product': 'Type of effect',
        'master_template': 'Effect'
    },
    
    # Timber type variations
    'timber_type_fields': {
        'Castorama_FR': 'Timber type',
        'Maxeda_NL': 'Timber type',
        'Maxeda_BE': 'Timber type',
        'LM_product': 'Timber species',
        'master_template': 'Timber Type'
    },
    
    # Fixing type variations
    'fixing_type_fields': {
        'Castorama_FR': 'Fixing type',
        'LM_product': 'Fixing type',
        'master_template': 'Fixing Type'
    }
}

# Dropdown value standardizations
DROPDOWN_VALUE_MAPPINGS = {
    'colour_values': {
        'master_template': [
            'White', 'Black', 'Brown', 'Grey', 'Beige', 'Blue', 'Red', 'Green',
            'Yellow', 'Orange', 'Purple', 'Pink', 'Multi', 'Natural', 'Oak',
            'Walnut', 'Mahogany', 'Pine', 'Cedar', 'Maple', 'Cherry', 'Teak',
            'Ash', 'Birch', 'Elm', 'Poplar', 'Spruce', 'Fir', 'Larch'
        ],
        'Castorama_FR': {
            'Blanc': 'White', 'Noir': 'Black', 'Brun': 'Brown',
            'Gris': 'Grey', 'Beige': 'Beige', 'Bleu': 'Blue',
            'Rouge': 'Red', 'Vert': 'Green', 'Jaune': 'Yellow',
            'Orange': 'Orange', 'Violet': 'Purple', 'Rose': 'Pink',
            'Naturel': 'Natural', 'Chêne': 'Oak', 'Noyer': 'Walnut',
            'Acajou': 'Mahogany', 'Pin': 'Pine', 'Cèdre': 'Cedar',
            'Érable': 'Maple', 'Cerisier': 'Cherry', 'Teck': 'Teak'
        },
        'Castorama_PL': {
            'Biały': 'White', 'Czarny': 'Black', 'Brązowy': 'Brown',
            'Szary': 'Grey', 'Beżowy': 'Beige', 'Niebieski': 'Blue',
            'Czerwony': 'Red', 'Zielony': 'Green', 'Żółty': 'Yellow',
            'Pomarańczowy': 'Orange', 'Fioletowy': 'Purple', 'Różowy': 'Pink',
            'Naturalny': 'Natural', 'Dąb': 'Oak', 'Orzech': 'Walnut',
            'Mahoń': 'Mahogany', 'Sosna': 'Pine', 'Cedr': 'Cedar',
            'Klon': 'Maple', 'Wiśnia': 'Cherry', 'Tik': 'Teak'
        }
    },
    
    'material_values': {
        'master_template': [
            'Wood', 'Metal', 'Plastic', 'Glass', 'Ceramic', 'Fabric',
            'Leather', 'Synthetic', 'Natural', 'Composite', 'Aluminum',
            'Steel', 'Iron', 'Copper', 'Bronze', 'Stone', 'Marble',
            'Granite', 'Concrete', 'Bamboo', 'Cork', 'Rattan', 'Wicker',
            'Particle Board', 'MDF', 'Plywood', 'Solid Wood', 'Engineered Wood'
        ]
    },
    
    'category_values': {
        'master_template': [
            'Flooring', 'Furniture', 'Lighting', 'Kitchen', 'Bathroom',
            'Garden', 'Tools', 'Paint', 'Hardware', 'Decor', 'Storage',
            'Outdoor', 'Indoor', 'Commercial', 'Residential', 'Wall Covering',
            'Ceiling', 'Window', 'Door', 'Staircase', 'Fencing', 'Decking'
        ]
    },
    
    'brand_values': {
        'master_template': [
            'TimberCraft', 'MetalWorks', 'PlasticPro', 'GlassArt', 'CeramicPlus',
            'FabricSoft', 'LeatherLux', 'SyntheticPro', 'NaturalChoice', 'CompositeCorp',
            'WoodMaster', 'SteelCraft', 'AluminumPro', 'IronWorks', 'CopperCraft',
            'BronzeArt', 'StoneMaster', 'MarbleLux', 'GranitePro', 'ConcreteCraft',
            'BambooNatural', 'CorkEco', 'RattanStyle', 'WickerCraft', 'ParticleBoard',
            'MDFPro', 'PlywoodCraft', 'SolidWood', 'EngineeredWood'
        ]
    },
    
    'finish_values': {
        'master_template': [
            'Natural', 'Stained', 'Painted', 'Varnished', 'Oiled', 'Waxed',
            'Lacquered', 'Distressed', 'Aged', 'Rustic', 'Modern', 'Classic',
            'Glossy', 'Matte', 'Satin', 'Semi-gloss', 'Textured', 'Smooth'
        ]
    },
    
    'design_values': {
        'master_template': [
            'Traditional', 'Modern', 'Contemporary', 'Rustic', 'Industrial',
            'Scandinavian', 'Minimalist', 'Vintage', 'Art Deco', 'Victorian',
            'Mediterranean', 'Asian', 'Bohemian', 'Shabby Chic', 'Farmhouse'
        ]
    },
    
    'effect_values': {
        'master_template': [
            'None', 'Distressed', 'Aged', 'Weathered', 'Antique', 'Vintage',
            'Hand-scraped', 'Wire-brushed', 'Smooth', 'Textured', 'Embossed',
            'Grooved', 'Chamfered', 'Beveled', 'Rounded', 'Square'
        ]
    },
    
    'timber_type_values': {
        'master_template': [
            'Oak', 'Walnut', 'Mahogany', 'Pine', 'Cedar', 'Maple', 'Cherry',
            'Teak', 'Ash', 'Birch', 'Elm', 'Poplar', 'Spruce', 'Fir', 'Larch',
            'Beech', 'Alder', 'Hickory', 'Pecan', 'Bamboo', 'Engineered'
        ]
    },
    
    'fixing_type_values': {
        'master_template': [
            'Glue', 'Nails', 'Screws', 'Clips', 'Click System', 'Tongue and Groove',
            'Floating', 'Glue Down', 'Nail Down', 'Staple Down', 'Self-adhesive',
            'Interlocking', 'Snap-fit', 'Hook and Loop', 'Magnetic'
        ]
    },
    
    'boolean_values': {
        'master_template': ['Yes', 'No'],
        'Castorama_FR': {'Oui': 'Yes', 'Non': 'No'},
        'Castorama_PL': {'Tak': 'Yes', 'Nie': 'No'}
    }
}

# Field type classifications
FIELD_TYPE_STRATEGIES = {
    'dropdown_fixed': {
        'description': 'Fixed dropdown with predefined options',
        'handling': 'Map to standardized master template dropdown',
        'examples': ['Colour', 'Material', 'Category Code', 'Brand', 'Finish', 'Design', 'Effect', 'Timber Type', 'Fixing Type']
    },
    'dropdown_free': {
        'description': 'Dropdown that allows custom entries',
        'handling': 'Preserve as free text with dropdown suggestions',
        'examples': ['Product Name', 'Description', 'USP', 'Code for internal use']
    },
    'free_text': {
        'description': 'Completely free text input',
        'handling': 'No restrictions, full text input',
        'examples': ['Product Title (Mirakl)', 'Description (Mirakl)', 'EAN', 'Category Code']
    },
    'numeric': {
        'description': 'Numeric values with units',
        'handling': 'Validate numeric input with unit options',
        'examples': ['Product weight (kg)', 'Product height (mm)', 'Product width (mm)', 'Product length (mm)', 'Product thickness (mm)']
    },
    'boolean': {
        'description': 'Yes/No or True/False fields',
        'handling': 'Dropdown with Yes/No options',
        'examples': ['CE marked', 'UKCA marked', 'GPSR Exempt', 'Can be cut', 'Contains wood', 'Made in Portugal']
    },
    'image_url': {
        'description': 'Image URL or file path',
        'handling': 'Validate URL format or file existence',
        'examples': ['Image 1', 'Image 2', 'Main Image 1', 'Secondary Image 1', 'Back of Pack Image']
    }
}

# Field type mapping for specific fields
FIELD_TYPE_MAPPINGS = {
    # Dropdown fields
    'Colour': 'dropdown_fixed',
    'Material': 'dropdown_fixed',
    'Category Code': 'dropdown_fixed',
    'Finish': 'dropdown_fixed',
    'Design': 'dropdown_fixed',
    'Effect': 'dropdown_fixed',
    'Timber Type': 'dropdown_fixed',
    'Fixing Type': 'dropdown_fixed',
    'Main Color': 'dropdown_fixed',
    'Main Material': 'dropdown_fixed',
    'Product Category': 'dropdown_fixed',
    'Manufacturer Name': 'dropdown_fixed',
    'Brand Name': 'dropdown_fixed',
    
    # Boolean fields
    'CE marked': 'boolean',
    'UKCA marked': 'boolean',
    'GPSR Exempt': 'boolean',
    'Can be cut': 'boolean',
    'Contains wood': 'boolean',
    'Made in Portugal': 'boolean',
    'Acquisition CE marked': 'boolean',
    
    # Numeric fields
    'Product weight (kg)': 'numeric',
    'Product height (mm)': 'numeric',
    'Product width (mm)': 'numeric',
    'Product length (mm)': 'numeric',
    'Product thickness (mm)': 'numeric',
    'Product weight (g)': 'numeric',
    'Coverage (m²)': 'numeric',
    
    # Image fields
    'Image 1': 'image_url',
    'Image 2': 'image_url',
    'Image 3': 'image_url',
    'Image 4': 'image_url',
    'Image 5': 'image_url',
    'Image 6': 'image_url',
    'Image 7': 'image_url',
    'Image 8': 'image_url',
    'Image 9': 'image_url',
    'Image 10': 'image_url',
    'Main Image 1': 'image_url',
    'Secondary Image 1': 'image_url',
    'Secondary Image 2': 'image_url',
    'Secondary Image 3': 'image_url',
    'Secondary Image 4': 'image_url',
    'Secondary Image 5': 'image_url',
    'Secondary Image 6': 'image_url',
    'Secondary Image 7': 'image_url',
    'Secondary Image 8': 'image_url',
    'Back of Pack Image': 'image_url',
    
    # Auto-filled fields (client-specific)
    'Brand': 'auto_filled',
    'Brand Name': 'auto_filled',
    'Manufacturer Name': 'auto_filled',
    
    # Free text fields (default)
    'Product Title (Mirakl)': 'free_text',
    'Description (Mirakl)': 'free_text',
    'EAN': 'free_text',
    'Code for internal use': 'free_text',
    'Name': 'free_text'
}

def get_field_mapping(field_name: str, source_platform: str, target_platform: str) -> str:
    """Get the mapped field name between platforms."""
    normalized_name = field_name.lower().strip()
    
    # Check each field category
    for category, mappings in FIELD_NAME_MAPPINGS.items():
        if source_platform in mappings and target_platform in mappings:
            source_field = mappings[source_platform]
            target_field = mappings[target_platform]
            
            # Check if the source field matches (case-insensitive)
            if source_field.lower() == normalized_name:
                return target_field
    
    # If no mapping found, return original field name
    return field_name

def get_dropdown_values(field_name: str, platform: str = 'master_template') -> List[str]:
    """Get dropdown values for a specific field and platform."""
    # Find the dropdown category for this field
    for category, values in DROPDOWN_VALUE_MAPPINGS.items():
        if field_name.lower() in category:
            if platform in values:
                return values[platform]
            elif 'master_template' in values:
                return values['master_template']
    
    # Check if it's a boolean field
    if is_boolean_field(field_name):
        return get_boolean_values(platform)
    
    # Check for specific field name mappings
    field_mappings = {
        'Category Code': 'category_values',
        'Product Category': 'category_values',
        'Brand': 'brand_values',
        'Brand Name': 'brand_values',
        'Manufacturer Name': 'brand_values',
        'Main Color': 'colour_values',
        'Main Material': 'material_values'
    }
    
    if field_name in field_mappings:
        category = field_mappings[field_name]
        if category in DROPDOWN_VALUE_MAPPINGS:
            values = DROPDOWN_VALUE_MAPPINGS[category]
            if platform in values:
                return values[platform]
            elif 'master_template' in values:
                return values['master_template']
    
    # Return empty list if no dropdown values found
    return []

def get_field_type(field_name: str) -> str:
    """Get the field type for a specific field."""
    return FIELD_TYPE_MAPPINGS.get(field_name, 'free_text')

def is_dropdown_field(field_name: str) -> bool:
    """Check if a field should have a dropdown."""
    field_type = get_field_type(field_name)
    return field_type in ['dropdown_fixed', 'dropdown_free']

def is_boolean_field(field_name: str) -> bool:
    """Check if a field is a boolean field."""
    return get_field_type(field_name) == 'boolean'

def is_numeric_field(field_name: str) -> bool:
    """Check if a field is a numeric field."""
    return get_field_type(field_name) == 'numeric'

def is_image_field(field_name: str) -> bool:
    """Check if a field is an image field."""
    return get_field_type(field_name) == 'image_url'

def is_auto_filled_field(field_name: str) -> bool:
    """Check if a field is auto-filled (client-specific)."""
    return get_field_type(field_name) == 'auto_filled'

def get_boolean_values(platform: str = 'master_template') -> List[str]:
    """Get boolean values for a specific platform."""
    return DROPDOWN_VALUE_MAPPINGS['boolean_values'].get(platform, ['Yes', 'No'])

def get_all_dropdown_fields() -> List[str]:
    """Get all fields that should have dropdowns."""
    return [field for field, field_type in FIELD_TYPE_MAPPINGS.items() 
            if field_type in ['dropdown_fixed', 'dropdown_free', 'boolean']]

def get_platform_field_variations(field_category: str) -> Dict[str, str]:
    """Get all platform variations for a specific field category."""
    return FIELD_NAME_MAPPINGS.get(field_category, {}) 