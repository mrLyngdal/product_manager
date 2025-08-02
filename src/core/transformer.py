"""
Core transformation functionality for the multimarketplace upload system.

This module handles:
- Transforming master template into platform-specific files
- Applying translations and field mappings
- Managing the transformation process
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional
import logging

from ..config.platforms import get_platform_config, get_language_for_platform, get_platform_columns
from ..config.settings import get_output_file_path, get_template_file_path, DEFAULT_OUTPUT_FORMAT
from ..utils.translation import translate_content

logger = logging.getLogger(__name__)

class MultimarketplaceTransformer:
    """Transforms master template into platform-specific files."""
    
    def __init__(self):
        self.generated_files: Dict[str, str] = {}
    
    def load_master_template(self, template_path: Path) -> pd.DataFrame:
        """Load the master template file (CSV or XLSX)."""
        try:
            if template_path.suffix.lower() == '.xlsx':
                df = pd.read_excel(template_path)
            else:
                df = pd.read_csv(template_path)
            logger.info(f"Loaded master template with {len(df)} rows and {len(df.columns)} columns")
            return df
        except Exception as e:
            logger.error(f"Error loading master template: {e}")
            return pd.DataFrame()
    
    def validate_required_fields(self, df: pd.DataFrame, platform: str) -> List[str]:
        """Validate that required fields are present and not empty."""
        config = get_platform_config(platform)
        if not config:
            return [f"Unknown platform: {platform}"]
        
        missing_fields = []
        
        for field in config.required_fields:
            if field not in df.columns:
                missing_fields.append(field)
            elif df[field].isna().all():
                missing_fields.append(f"{field} (all empty)")
        
        return missing_fields
    
    def generate_platform_file(self, df: pd.DataFrame, platform: str) -> pd.DataFrame:
        """Generate a platform-specific file from the master template."""
        config = get_platform_config(platform)
        if not config:
            logger.error(f"Unknown platform: {platform}")
            return pd.DataFrame()
        
        target_language = get_language_for_platform(platform)
        
        logger.info(f"Generating {config.name} file...")
        
        # Validate required fields
        missing_fields = self.validate_required_fields(df, platform)
        if missing_fields:
            logger.warning(f"Missing required fields for {platform}: {missing_fields}")
        
        # Create platform-specific dataframe
        platform_df = df.copy()
        
        # Apply translations to language-specific fields
        for field_type, field_name in config.language_fields.items():
            if field_name and field_name in platform_df.columns:
                logger.info(f"Translating {field_name} to {target_language}")
                platform_df[field_name] = platform_df[field_name].apply(
                    lambda x: translate_content(x, target_language)
                )
        
        # Filter columns to only include those needed for this platform
        platform_columns = get_platform_columns(platform)
        available_columns = [col for col in platform_columns if col in platform_df.columns]
        
        platform_df = platform_df[available_columns]
        
        logger.info(f"Generated {config.name} file with {len(platform_df.columns)} columns")
        return platform_df
    
    def save_platform_file(self, df: pd.DataFrame, platform: str) -> str:
        """Save the platform-specific file."""
        config = get_platform_config(platform)
        if not config:
            logger.error(f"Unknown platform: {platform}")
            return ""
        
        output_file = get_output_file_path(platform)
        
        try:
            if DEFAULT_OUTPUT_FORMAT == 'xlsx':
                df.to_excel(output_file, index=False)
            else:
                df.to_csv(output_file, index=False)
            
            logger.info(f"✅ Saved {output_file}")
            return str(output_file)
        except Exception as e:
            logger.error(f"❌ Error saving {output_file}: {e}")
            return ""
    
    def generate_all_platforms(self, template_path: Path) -> Dict[str, str]:
        """Generate files for all platforms."""
        df = self.load_master_template(template_path)
        if df.empty:
            logger.error("Failed to load master template")
            return {}
        
        generated_files = {}
        
        from ..config.platforms import get_all_platforms
        for platform in get_all_platforms():
            platform_df = self.generate_platform_file(df, platform)
            if not platform_df.empty:
                output_file = self.save_platform_file(platform_df, platform)
                if output_file:
                    generated_files[platform] = output_file
        
        self.generated_files = generated_files
        return generated_files
    
    def get_transformation_summary(self) -> Dict:
        """Get a summary of the transformation process."""
        from ..config.platforms import get_all_platforms
        summary = {
            'total_platforms': len(self.generated_files),
            'platforms_processed': list(self.generated_files.keys()),
            'generated_files': self.generated_files,
            'success_rate': len(self.generated_files) / len(get_all_platforms()) * 100
        }
        return summary

def transform_template_to_platforms(template_path: Path, platforms: Optional[List[str]] = None) -> Dict[str, str]:
    """Transform a template file to platform-specific files."""
    transformer = MultimarketplaceTransformer()
    
    if platforms is None:
        from ..config.platforms import get_all_platforms
        platforms = get_all_platforms()
    
    df = transformer.load_master_template(template_path)
    if df.empty:
        return {}
    
    generated_files = {}
    
    for platform in platforms:
        platform_df = transformer.generate_platform_file(df, platform)
        if not platform_df.empty:
            output_file = transformer.save_platform_file(platform_df, platform)
            if output_file:
                generated_files[platform] = output_file
    
    return generated_files

def validate_template_for_platforms(template_path: Path) -> Dict[str, List[str]]:
    """Validate that a template has all required fields for all platforms."""
    df = pd.read_csv(template_path)
    validation_results = {}
    
    from ..config.platforms import get_all_platforms
    for platform in get_all_platforms():
        missing_fields = []
        config = get_platform_config(platform)
        
        if config:
            for field in config.required_fields:
                if field not in df.columns:
                    missing_fields.append(field)
                elif df[field].isna().all():
                    missing_fields.append(f"{field} (all empty)")
        
        validation_results[platform] = missing_fields
    
    return validation_results 