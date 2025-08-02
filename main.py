#!/usr/bin/env python3
"""
Main entry point for the multimarketplace upload system.

This script provides a command-line interface for the main operations:
- MVP template creation
- Sample data generation
- Template transformation
- DeepL translation management
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.transformer import MultimarketplaceTransformer
from src.config.settings import ensure_directories_exist, get_template_file_path
from src.config.platforms import get_all_platforms, get_platform_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def generate_sample_data():
    """Generate sample data for testing."""
    print("🎯 Generating sample product data...")
    print("=" * 60)
    
    # Import here to avoid circular imports
    from tests.generate_sample_data import create_sample_template
    
    sample_file = create_sample_template()
    
    if sample_file:
        print(f"\n✅ Sample template created: {sample_file}")
        print("\n📝 Next steps:")
        print("1. Review the sample data")
        print("2. Run transformation pipeline")
        print("3. Customize the sample data as needed")
    else:
        print("\n❌ Failed to create sample template")

def transform_template():
    """Transform template to platform-specific files."""
    print("🚀 Starting multimarketplace transformation pipeline...")
    print("=" * 60)
    
    ensure_directories_exist()
    
    # Try sample template first, then fall back to master template
    template_file = get_template_file_path('sample')
    if not template_file.exists():
        template_file = get_template_file_path('master')
    
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        print("Please create an MVP template first using: python main.py create-mvp")
        return
    
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
    else:
        print("❌ No files were generated.")

def list_platforms():
    """List all supported platforms."""
    print("📋 Supported Platforms:")
    print("=" * 60)
    
    platforms = get_all_platforms()
    for platform in platforms:
        config = get_platform_config(platform)
        if config:
            print(f"   • {config.name} ({platform})")
            print(f"     - Required fields: {len(config.required_fields)}")
            print(f"     - Language fields: {len([f for f in config.language_fields.values() if f])}")
            print(f"     - Image fields: {len(config.image_fields)}")
            print()

# Removed optimize_template and analyze_fields functions for simplicity

def deepl_setup():
    """Set up DeepL API key."""
    from src.scripts.manage_deepl import setup_api_key
    setup_api_key()

def deepl_usage():
    """Check DeepL usage."""
    from src.scripts.manage_deepl import check_usage
    check_usage()

def deepl_test():
    """Test DeepL translation."""
    from src.scripts.manage_deepl import test_translation
    test_translation()

def create_mvp_template():
    """Create an MVP template with minimum required fields."""
    from src.scripts.create_mvp_template import create_mvp_template
    return create_mvp_template()

def validate_template():
    """Validate template for all platforms."""
    print("🔍 Validating template for all platforms...")
    print("=" * 60)
    
    template_file = get_template_file_path('sample')
    if not template_file.exists():
        template_file = get_template_file_path('master')
    
    if not template_file.exists():
        print(f"❌ Template file not found: {template_file}")
        return
    
    from src.core.transformer import validate_template_for_platforms
    validation_results = validate_template_for_platforms(template_file)
    
    all_valid = True
    for platform, missing_fields in validation_results.items():
        config = get_platform_config(platform)
        platform_name = config.name if config else platform
        
        if missing_fields:
            print(f"❌ {platform_name}: Missing {len(missing_fields)} required fields")
            for field in missing_fields:
                print(f"     - {field}")
            all_valid = False
        else:
            print(f"✅ {platform_name}: All required fields present")
    
    if all_valid:
        print("\n🎉 All platforms validated successfully!")
    else:
        print("\n⚠️  Some platforms have missing required fields.")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Multimarketplace Upload System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py create-mvp          # Create MVP template with minimum fields
  python main.py generate-sample     # Generate sample data for testing
  python main.py transform           # Transform template to platform files
  python main.py list-platforms      # List all supported platforms
  python main.py validate            # Validate template for all platforms
  python main.py deepl-setup         # Setup DeepL API key
  python main.py deepl-usage         # Check DeepL usage
  python main.py deepl-test          # Test DeepL translation
        """
    )
    
    parser.add_argument(
        'command',
        choices=['create-mvp', 'generate-sample', 'transform', 'list-platforms', 'validate', 'deepl-setup', 'deepl-usage', 'deepl-test'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'create-mvp':
        create_mvp_template()
    elif args.command == 'generate-sample':
        generate_sample_data()
    elif args.command == 'transform':
        transform_template()
    elif args.command == 'list-platforms':
        list_platforms()
    elif args.command == 'validate':
        validate_template()
    elif args.command == 'deepl-setup':
        deepl_setup()
    elif args.command == 'deepl-usage':
        deepl_usage()
    elif args.command == 'deepl-test':
        deepl_test()

if __name__ == "__main__":
    main() 