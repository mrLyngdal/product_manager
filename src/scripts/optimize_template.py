#!/usr/bin/env python3
"""
Template optimization script for multimarketplace upload system.

This script optimizes the master template by:
- Converting from CSV to XLSX format
- Restructuring columns in logical order
- Applying color coding for field types
- Making it easier for manual data entry
"""

import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.template_optimizer import optimize_master_template
from src.config.settings import ensure_directories_exist

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main function to run template optimization."""
    print("🎯 Starting template optimization...")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories_exist()
    
    # Run optimization
    success = optimize_master_template()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Template Optimization Summary:")
        print("=" * 60)
        print("✅ Converted CSV to XLSX format")
        print("✅ Restructured columns in logical order")
        print("✅ Applied color coding:")
        print("   • 🔴 Red: Required fields (Category Code, EAN, Brand, etc.)")
        print("   • 🟢 Green: Automated fields (translations, additional images)")
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

if __name__ == "__main__":
    main() 