#!/usr/bin/env python3
"""
Client management script for multimarketplace upload system.

This script provides easy management of client configurations,
including adding new clients, updating brand names, and listing clients.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.config.client_config import (
    create_client_config_csv, list_available_clients, 
    add_new_client, update_client_brand, get_client_config
)

def list_clients():
    """List all available clients."""
    print("📋 Available Clients:")
    print("=" * 40)
    
    clients = list_available_clients()
    
    if not clients:
        print("No clients found. Creating default configuration...")
        create_client_config_csv()
        clients = list_available_clients()
    
    for i, client_name in enumerate(clients, 1):
        print(f"{i}. {client_name}")
        
        # Show brand mappings for this client
        config = get_client_config(client_name)
        brand_mappings = config.get_all_brand_mappings()
        
        print("   Brand Mappings:")
        for platform, brand in brand_mappings.items():
            print(f"     • {platform}: {brand}")
        print()

def show_client_details(client_name: str):
    """Show detailed information for a specific client."""
    print(f"📊 Client Details: {client_name}")
    print("=" * 50)
    
    config = get_client_config(client_name)
    brand_mappings = config.get_all_brand_mappings()
    
    print(f"Client Name: {config.get_client_name()}")
    print("\nBrand Mappings:")
    for platform, brand in brand_mappings.items():
        print(f"  • {platform}: {brand}")
    
    print(f"\nDefault Values:")
    default_values = config.config['default_values']
    for field, value in default_values.items():
        print(f"  • {field}: {value}")
    
    print(f"\nSettings:")
    settings = config.config['settings']
    for setting, value in settings.items():
        print(f"  • {setting}: {value}")

def add_client():
    """Add a new client interactively."""
    print("➕ Adding New Client")
    print("=" * 30)
    
    client_name = input("Enter client name: ").strip()
    if not client_name:
        print("❌ Client name cannot be empty")
        return
    
    print("\nEnter brand names for each platform:")
    brand_mappings = {}
    
    platforms = ['Castorama_FR', 'Castorama_PL', 'LM_product', 'Maxeda_BE', 'Maxeda_NL']
    platform_names = {
        'Castorama_FR': 'Castorama FR',
        'Castorama_PL': 'Castorama PL', 
        'LM_product': 'Leroy Merlin',
        'Maxeda_BE': 'Maxeda BE',
        'Maxeda_NL': 'Maxeda NL'
    }
    
    for platform in platforms:
        default = 'Nordic Acoustics' if platform != 'LM_product' else 'NORDIC ACOUSTICS'
        brand = input(f"Brand for {platform_names[platform]} (default: {default}): ").strip()
        if not brand:
            brand = default
        brand_mappings[platform] = brand
    
    notes = input("Notes (optional): ").strip()
    
    # Add the client
    add_new_client(client_name, brand_mappings, notes)
    
    print(f"\n✅ Successfully added client: {client_name}")
    print("Brand mappings:")
    for platform, brand in brand_mappings.items():
        print(f"  • {platform_names[platform]}: {brand}")

def update_brand():
    """Update brand name for a specific client and platform."""
    print("🔄 Update Brand Name")
    print("=" * 30)
    
    # List available clients
    clients = list_available_clients()
    print("Available clients:")
    for i, client in enumerate(clients, 1):
        print(f"{i}. {client}")
    
    try:
        choice = int(input("\nSelect client (number): ")) - 1
        if choice < 0 or choice >= len(clients):
            print("❌ Invalid selection")
            return
        client_name = clients[choice]
    except ValueError:
        print("❌ Invalid input")
        return
    
    # List platforms
    platforms = ['Castorama_FR', 'Castorama_PL', 'LM_product', 'Maxeda_BE', 'Maxeda_NL']
    platform_names = {
        'Castorama_FR': 'Castorama FR',
        'Castorama_PL': 'Castorama PL', 
        'LM_product': 'Leroy Merlin',
        'Maxeda_BE': 'Maxeda BE',
        'Maxeda_NL': 'Maxeda NL'
    }
    
    print(f"\nPlatforms for {client_name}:")
    for i, platform in enumerate(platforms, 1):
        print(f"{i}. {platform_names[platform]}")
    
    try:
        platform_choice = int(input("\nSelect platform (number): ")) - 1
        if platform_choice < 0 or platform_choice >= len(platforms):
            print("❌ Invalid selection")
            return
        platform = platforms[platform_choice]
    except ValueError:
        print("❌ Invalid input")
        return
    
    # Get current brand
    config = get_client_config(client_name)
    current_brand = config.get_brand_for_platform(platform)
    
    new_brand = input(f"\nCurrent brand for {platform_names[platform]}: {current_brand}\nNew brand: ").strip()
    
    if not new_brand:
        print("❌ Brand name cannot be empty")
        return
    
    # Update the brand
    success = update_client_brand(client_name, platform, new_brand)
    
    if success:
        print(f"✅ Successfully updated {client_name} brand for {platform_names[platform]}: {new_brand}")
    else:
        print("❌ Failed to update brand")

def create_sample_config():
    """Create the sample client configuration file."""
    print("📝 Creating sample client configuration...")
    
    config_file = create_client_config_csv()
    
    print(f"✅ Created sample configuration: {config_file}")
    print("\nSample clients added:")
    print("• Nordic Acoustics (main client)")
    print("• TimberCraft (sample client)")
    print("• MetalWorks (sample client)")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Client Management for Multimarketplace Upload System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/scripts/manage_clients.py list                    # List all clients
  python src/scripts/manage_clients.py show Nordic Acoustics   # Show client details
  python src/scripts/manage_clients.py add                     # Add new client
  python src/scripts/manage_clients.py update                  # Update brand name
  python src/scripts/manage_clients.py create-sample           # Create sample config
        """
    )
    
    parser.add_argument(
        'command',
        choices=['list', 'show', 'add', 'update', 'create-sample'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'client_name',
        nargs='?',
        help='Client name (for show command)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_clients()
    elif args.command == 'show':
        if not args.client_name:
            print("❌ Please provide a client name")
            return
        show_client_details(args.client_name)
    elif args.command == 'add':
        add_client()
    elif args.command == 'update':
        update_brand()
    elif args.command == 'create-sample':
        create_sample_config()

if __name__ == "__main__":
    main() 