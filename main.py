#!/usr/bin/env python3
"""
Main entry point for the multimarketplace upload system.

This script provides a command-line interface for the main operations:
- Header extraction
- Sample data generation
- Template transformation
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.extractor import HeaderExtractor
from src.core.transformer import MultimarketplaceTransformer
from src.config.settings import ensure_directories_exist, get_template_file_path
from src.config.platforms import get_all_platforms, get_platform_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def extract_headers():
    """Extract headers from marketplace files."""
    print("🚀 Starting header extraction process...")
    print("=" * 60)
    
    ensure_directories_exist()
    extractor = HeaderExtractor()
    success = extractor.run_extraction()
    
    if success:
        summary = extractor.get_extraction_summary()
        print("\n" + "=" * 60)
        print("📊 Extraction Summary:")
        print("=" * 60)
        print(f"✅ Total platforms processed: {summary['total_platforms']}")
        print(f"✅ Total unique headers: {summary['total_unique_headers']}")
        print(f"✅ Platforms: {', '.join(summary['platforms_processed'])}")
        print("\nHeaders per platform:")
        for platform, count in summary['headers_per_platform'].items():
            print(f"   • {platform}: {count} headers")
    else:
        print("\n❌ Header extraction failed.")

def generate_sample_data():
    """Generate sample data for testing."""
    print("🎯 Generating sample product data...")
    print("=" * 60)
    
    # Import here to avoid circular imports
    from src.scripts.generate_sample_data import create_sample_template
    
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
        print("Please run header extraction first to create the template.")
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

def optimize_template():
    """Optimize template to XLSX format with color coding."""
    print("🎯 Starting template optimization...")
    print("=" * 60)
    
    # Import here to avoid circular imports
    from src.utils.template_optimizer import optimize_master_template
    from src.config.client_config import list_available_clients
    
    # Show available clients
    clients = list_available_clients()
    print(f"Available clients: {', '.join(clients)}")
    print(f"Using default client: Nordic Acoustics")
    
    success = optimize_master_template('Nordic Acoustics')
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Template Optimization Summary:")
        print("=" * 60)
        print("✅ Converted CSV to XLSX format")
        print("✅ Restructured columns in logical order")
        print("✅ Applied color coding:")
        print("   • 🔴 Red: Required fields (Category Code, EAN, Code for internal use, etc.)")
        print("   • 🟢 Green: Automated fields (client-specific brands, translations, additional images)")
        print("   • 🟡 Yellow: Optional fields (remaining columns)")
        print("✅ Auto-adjusted column widths")
        print("✅ Made template easier for manual data entry")
        
        print("\n📝 Next Steps:")
        print("1. Open the optimized XLSX template")
        print("2. Fill in the required fields (red columns)")
        print("3. Add optional data as needed (yellow columns)")
        print("4. Save and use for transformation")
    else:
        print("\n❌ Template optimization failed. Check the error messages above.")

def analyze_fields():
    """Analyze fields and dropdowns across all input files."""
    print("🔍 Starting comprehensive field analysis...")
    print("=" * 60)
    
    # Import here to avoid circular imports
    from src.scripts.analyze_fields import FieldAnalyzer
    
    ensure_directories_exist()
    
    # Create analyzer and run analysis
    analyzer = FieldAnalyzer()
    results = analyzer.analyze_all_files()
    
    # Save results
    analyzer.save_results()
    
    # Print summary
    analyzer.print_summary()
    
    print("\n✅ Field analysis completed successfully!")
    print("📝 Next steps:")
    print("1. Review analysis_results.json for detailed findings")
    print("2. Create field mapping configurations")
    print("3. Implement dropdown standardization")
    print("4. Update template optimizer with dropdown support")

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
  python main.py extract-headers     # Extract headers from marketplace files
  python main.py generate-sample     # Generate sample data for testing
  python main.py optimize-template   # Optimize template to XLSX with color coding
  python main.py transform           # Transform template to platform files
  python main.py list-platforms      # List all supported platforms
  python main.py validate            # Validate template for all platforms
  python main.py analyze-fields      # Analyze fields and dropdowns across input files
        """
    )
    
    parser.add_argument(
        'command',
        choices=['extract-headers', 'generate-sample', 'optimize-template', 'transform', 'list-platforms', 'validate', 'analyze-fields'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    if args.command == 'extract-headers':
        extract_headers()
    elif args.command == 'generate-sample':
        generate_sample_data()
    elif args.command == 'transform':
        transform_template()
    elif args.command == 'list-platforms':
        list_platforms()
    elif args.command == 'optimize-template':
        optimize_template()
    elif args.command == 'validate':
        validate_template()
    elif args.command == 'analyze-fields':
        analyze_fields()

if __name__ == "__main__":
    main() 