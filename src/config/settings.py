"""
Global settings and configuration for the multimarketplace upload system.

This module contains:
- File paths and directories
- Default settings
- Configuration constants
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
TEMPLATES_DIR = DATA_DIR / "templates"
OUTPUT_DIR = DATA_DIR / "output"

# Template files
MASTER_TEMPLATE_FILE = TEMPLATES_DIR / "multimarketplace_master_template.xlsx"
SAMPLE_TEMPLATE_FILE = TEMPLATES_DIR / "sample_master_template.csv"

# Input files (original marketplace files)
INPUT_FILES = {
    'castorama_fr': INPUT_DIR / "Castorama_FR_upload.xlsx",
    'castorama_pl': INPUT_DIR / "Castorama_PL_upload.xlsx",
    'leroy_merlin': INPUT_DIR / "LM_product upload.xlsx",
    'maxeda_be': INPUT_DIR / "Maxeda_BE_upload.xlsx",
    'maxeda_nl': INPUT_DIR / "Maxeda_NL_upload.xlsx"
}

# Default settings
DEFAULT_ENCODING = 'utf-8'
DEFAULT_OUTPUT_FORMAT = 'xlsx'

# Translation settings
TRANSLATION_PLACEHOLDER_PREFIX = True  # Add [LANG] prefix to translated content

# Validation settings
VALIDATE_REQUIRED_FIELDS = True
VALIDATE_FILE_EXISTENCE = True
VALIDATE_DATA_TYPES = True

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Performance settings
BATCH_SIZE = 1000  # Number of rows to process in batches
MAX_WORKERS = 4    # Maximum number of parallel workers

def ensure_directories_exist():
    """Ensure all required directories exist."""
    directories = [DATA_DIR, INPUT_DIR, TEMPLATES_DIR, OUTPUT_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_output_file_path(platform: str) -> Path:
    """Get output file path for a specific platform."""
    from .platforms import get_platform_config
    config = get_platform_config(platform)
    if config:
        return OUTPUT_DIR / config.output_filename
    return OUTPUT_DIR / f"{platform}_generated.xlsx"

def get_template_file_path(template_type: str = 'master') -> Path:
    """Get template file path."""
    if template_type == 'sample':
        return SAMPLE_TEMPLATE_FILE
    return MASTER_TEMPLATE_FILE

def validate_paths():
    """Validate that all required files and directories exist."""
    missing_files = []
    
    # Check input files
    for platform, file_path in INPUT_FILES.items():
        if not file_path.exists():
            missing_files.append(f"Input file for {platform}: {file_path}")
    
    # Check template files
    if not MASTER_TEMPLATE_FILE.exists():
        missing_files.append(f"Master template: {MASTER_TEMPLATE_FILE}")
    
    if missing_files:
        raise FileNotFoundError(f"Missing required files:\n" + "\n".join(missing_files))
    
    return True 