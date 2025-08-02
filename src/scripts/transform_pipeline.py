#!/usr/bin/env python3
"""
Transformation pipeline script for multimarketplace upload system.

This script transforms the master template into platform-specific files
with appropriate translations and formatting.
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.transformer import MultimarketplaceTransformer
from src.config.settings import get_template_file_path, ensure_directories_exist
from src.config.platforms import get_all_platforms, get_platform_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to run the transformation pipeline."""
    print("🚀 Starting multimarketplace transformation pipeline...")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories_exist()
    
    # Try sample template first, then fall back to master template
    template_file = get_template_file_path('sample')
    if not template_file.exists():
        template_file = get_template_file_path('master')
    
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        print("Please run generate_sample_data.py first to create sample data.")
        return
    
    # Create transformer and run transformation
    transformer = MultimarketplaceTransformer()
    generated_files = transformer.generate_all_platforms(template_file)
    
    print("\n" + "=" * 60)
    print("📊 Transformation Summary:")
    print("=" * 60)
    
    if generated_files:
        print("✅ Successfully generated platform files:")
        for platform, file_path in generated_files.items():
            config = get_platform_config(platform)
            platform_name = config.name if config else platform
            print(f"   • {platform_name}: {file_path}")
        
        summary = transformer.get_transformation_summary()
        print(f"\n📈 Success rate: {summary['success_rate']:.1f}%")
        print(f"📈 Platforms processed: {summary['total_platforms']}")
        
        print("\n📝 Next Steps:")
        print("1. Review the generated files for accuracy")
        print("2. Integrate with a real translation service")
        print("3. Add validation rules for each platform")
        print("4. Implement data quality checks")
    else:
        print("❌ No files were generated. Check the error messages above.")

if __name__ == "__main__":
    main() 