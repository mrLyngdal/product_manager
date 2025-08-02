#!/usr/bin/env python3
"""
DeepL API Management Script

This script provides a command-line interface for:
- Setting up DeepL API key
- Checking usage limits
- Testing translations
- Managing free tier usage
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config.deepl_config import (
    get_deepl_api_key, save_deepl_api_key, validate_deepl_api_key,
    DeepLUsageTracker
)
from src.utils.translation import DeepLService

def setup_api_key():
    """Interactive setup for DeepL API key."""
    print("🔑 DeepL API Key Setup")
    print("=" * 40)
    
    # Check if API key already exists
    existing_key = get_deepl_api_key()
    if existing_key:
        print(f"✅ Existing API key found: {existing_key[:8]}...")
        replace = input("Do you want to replace it? (y/N): ").lower().strip()
        if replace != 'y':
            print("Setup cancelled.")
            return
    
    print("\n📋 To get your DeepL API key:")
    print("1. Go to https://www.deepl.com/pro-api")
    print("2. Sign up for a free account")
    print("3. Get your API key from the dashboard")
    print("4. The free tier includes 500,000 characters per month")
    print("\n💡 Tip: You can also add your API key to a .env file as DEEPL_key=your_api_key_here")
    
    api_key = input("\n🔑 Enter your DeepL API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return
    
    # Validate the API key
    print("\n🔍 Validating API key...")
    if validate_deepl_api_key(api_key):
        save_deepl_api_key(api_key)
        print("✅ API key saved and validated successfully!")
    else:
        print("❌ API key validation failed. Please check your key and try again.")

def check_usage():
    """Display current usage summary."""
    print("📊 DeepL Usage Summary")
    print("=" * 40)
    
    usage_tracker = DeepLUsageTracker()
    summary = usage_tracker.get_usage_summary()
    
    print(f"📅 Daily Usage:")
    print(f"   Characters: {summary['daily']['characters']:,} / {summary['daily']['limit_characters']:,}")
    print(f"   Requests: {summary['daily']['requests']} / {summary['daily']['limit_requests']}")
    print(f"   Remaining: {summary['remaining']['daily_characters']:,} chars, {summary['remaining']['daily_requests']} requests")
    
    print(f"\n📅 Monthly Usage:")
    print(f"   Characters: {summary['monthly']['characters']:,} / {summary['monthly']['limit_characters']:,}")
    print(f"   Requests: {summary['monthly']['requests']}")
    print(f"   Remaining: {summary['remaining']['monthly_characters']:,} chars")
    
    # Calculate percentages
    daily_char_pct = (summary['daily']['characters'] / summary['daily']['limit_characters']) * 100
    daily_req_pct = (summary['daily']['requests'] / summary['daily']['limit_requests']) * 100
    monthly_char_pct = (summary['monthly']['characters'] / summary['monthly']['limit_characters']) * 100
    
    print(f"\n📈 Usage Percentages:")
    print(f"   Daily Characters: {daily_char_pct:.1f}%")
    print(f"   Daily Requests: {daily_req_pct:.1f}%")
    print(f"   Monthly Characters: {monthly_char_pct:.1f}%")
    
    # Warnings
    if daily_char_pct > 80:
        print(f"\n⚠️  Warning: Daily character usage is at {daily_char_pct:.1f}%")
    if daily_req_pct > 80:
        print(f"\n⚠️  Warning: Daily request usage is at {daily_req_pct:.1f}%")
    if monthly_char_pct > 80:
        print(f"\n⚠️  Warning: Monthly character usage is at {monthly_char_pct:.1f}%")

def test_translation():
    """Test DeepL translation with a sample text."""
    print("🧪 DeepL Translation Test")
    print("=" * 40)
    
    api_key = get_deepl_api_key()
    if not api_key:
        print("❌ No DeepL API key found. Run 'setup' first.")
        return
    
    # Create DeepL service
    deepl_service = DeepLService(api_key)
    
    # Test texts
    test_texts = [
        ("Hello, how are you?", "FR", "French"),
        ("Premium wood flooring", "NL", "Dutch"),
        ("High quality materials", "PL", "Polish"),
        ("Professional installation", "DE", "German")
    ]
    
    print("Testing translations...")
    print()
    
    for text, target_lang, lang_name in test_texts:
        print(f"🇬🇧 English: {text}")
        print(f"🌍 Target: {lang_name} ({target_lang})")
        
        # Check if translation is allowed
        if deepl_service.can_translate(len(text)):
            translated = deepl_service.translate(text, target_lang)
            print(f"✅ Translated: {translated}")
        else:
            print("❌ Translation skipped due to usage limits")
        
        print("-" * 50)
    
    # Show usage after test
    print("\n📊 Usage after test:")
    summary = deepl_service.get_usage_summary()
    print(f"   Daily characters: {summary['daily']['characters']:,}")
    print(f"   Daily requests: {summary['daily']['requests']}")

def reset_usage():
    """Reset usage data (for testing purposes)."""
    print("🔄 Reset Usage Data")
    print("=" * 40)
    
    confirm = input("Are you sure you want to reset usage data? This is for testing only. (y/N): ").lower().strip()
    if confirm != 'y':
        print("Reset cancelled.")
        return
    
    usage_file = Path('data/config/deepl_usage.json')
    if usage_file.exists():
        usage_file.unlink()
        print("✅ Usage data reset successfully!")
    else:
        print("ℹ️  No usage data found to reset.")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="DeepL API Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/scripts/manage_deepl.py setup     # Set up API key
  python src/scripts/manage_deepl.py usage     # Check usage
  python src/scripts/manage_deepl.py test      # Test translation
  python src/scripts/manage_deepl.py reset     # Reset usage (testing)
        """
    )
    
    parser.add_argument(
        'command',
        choices=['setup', 'usage', 'test', 'reset'],
        help='Command to execute'
    )
    
    args = parser.parse_args()
    
    print("🌐 DeepL API Management Tool")
    print("=" * 50)
    
    if args.command == 'setup':
        setup_api_key()
    elif args.command == 'usage':
        check_usage()
    elif args.command == 'test':
        test_translation()
    elif args.command == 'reset':
        reset_usage()
    
    print("\n✨ Done!")

if __name__ == "__main__":
    main() 