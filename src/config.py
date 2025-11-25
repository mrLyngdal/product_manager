"""
Simple platform configuration.
Easy to add new platforms by extending the dictionaries.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
CONFIG_DIR = DATA_DIR / "config"
REF_DIR = DATA_DIR / "ref"

# Supported platforms (easy to add more)
PLATFORMS = ['castorama_fr', 'leroy_merlin']

# Reference template files for each platform
REF_TEMPLATES = {
    'castorama_fr': REF_DIR / 'Castorama_FR_upload.xlsx',
    'leroy_merlin': REF_DIR / 'LM_product upload.xlsx',
    'castorama_pl': REF_DIR / 'Castorama_PL_upload.xlsx',
    'maxeda_be': REF_DIR / 'Maxeda_BE_upload.xlsx',
    'maxeda_nl': REF_DIR / 'Maxeda_NL_upload.xlsx'
}

# Config files
MAPPING_FILE = CONFIG_DIR / 'mapping.xlsx'
ATTRIBUTES_FILE = CONFIG_DIR / 'attributes.xlsx'

def get_output_file_path(platform: str) -> Path:
    """Get output file path for a platform."""
    platform_names = {
        'castorama_fr': 'Castorama_FR_generated',
        'leroy_merlin': 'LM_product_generated',
        'castorama_pl': 'Castorama_PL_generated',
        'maxeda_be': 'Maxeda_BE_generated',
        'maxeda_nl': 'Maxeda_NL_generated'
    }
    filename = platform_names.get(platform, f'{platform}_generated')
    return OUTPUT_DIR / f'{filename}.xlsx'

