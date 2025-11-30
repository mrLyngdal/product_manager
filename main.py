#!/usr/bin/env python3
"""
Main entry point for the simple multimarketplace transformer.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.transformer import generate_platform_file
from src.translator import translate_input_file
from src.config import PLATFORMS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def translate(input_file: str):
    """
    Translate empty language fields in input file from English version.
    
    Args:
        input_file: Input filename (e.g., 'acoustic_panels.xlsx')
    """
    print(f"🌐 Translating {input_file}...")
    print("=" * 60)
    
    success = translate_input_file(input_file)
    
    if success:
        print(f"\n✅ Translation complete for {input_file}")
    else:
        print(f"\n❌ Translation failed")


def transform(platform: str, input_file: str):
    """
    Transform input file to platform-specific output.
    
    Args:
        platform: Platform identifier (e.g., 'castorama_fr')
        input_file: Input filename (e.g., 'acoustic_panels.xlsx')
    """
    if platform not in PLATFORMS:
        print(f"❌ Unknown platform: {platform}")
        print(f"Available platforms: {', '.join(PLATFORMS)}")
        return
    
    print(f"🚀 Transforming {input_file} for {platform}...")
    print("=" * 60)
    
    output_path = generate_platform_file(platform, input_file)
    
    if output_path:
        print(f"\n✅ Successfully generated: {output_path}")
    else:
        print(f"\n❌ Failed to generate output file")


def list_platforms():
    """List all supported platforms."""
    print("📋 Supported Platforms:")
    print("=" * 60)
    for platform in PLATFORMS:
        print(f"   • {platform}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Simple Multimarketplace Product Transformer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py translate --input acoustic_panels.xlsx
  python main.py transform --platform castorama_fr --input acoustic_panels.xlsx
  python main.py list-platforms
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Translate command
    translate_parser = subparsers.add_parser('translate', help='Translate empty language fields in input file')
    translate_parser.add_argument(
        '--input',
        required=True,
        help='Input filename (e.g., acoustic_panels.xlsx)'
    )
    
    # Transform command
    transform_parser = subparsers.add_parser('transform', help='Transform input to platform file')
    transform_parser.add_argument(
        '--platform',
        required=True,
        help='Platform identifier (e.g., castorama_fr)'
    )
    transform_parser.add_argument(
        '--input',
        required=True,
        help='Input filename (e.g., acoustic_panels.xlsx)'
    )
    
    # List platforms command
    subparsers.add_parser('list-platforms', help='List all supported platforms')
    
    args = parser.parse_args()
    
    if args.command == 'translate':
        translate(args.input)
    elif args.command == 'transform':
        transform(args.platform, args.input)
    elif args.command == 'list-platforms':
        list_platforms()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

