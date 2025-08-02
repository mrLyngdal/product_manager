#!/usr/bin/env python3
"""
Header extraction script for multimarketplace upload system.

This script extracts all unique column headers from marketplace Excel files
and creates a unified master template.
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.extractor import HeaderExtractor
from src.config.settings import ensure_directories_exist

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to run header extraction."""
    print("🚀 Starting header extraction process...")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories_exist()
    
    # Create extractor and run extraction
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
        
        print(f"\n✅ Master template created successfully!")
        print("📝 Next steps:")
        print("1. Review the master template")
        print("2. Populate with product data")
        print("3. Run transformation pipeline")
    else:
        print("\n❌ Header extraction failed. Check the error messages above.")

if __name__ == "__main__":
    main() 