"""
Client configuration for multimarketplace upload system.

This module manages client-specific settings like brand names,
platform mappings, and other client configurations.
"""

import csv
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Default client configuration
DEFAULT_CLIENT_CONFIG = {
    'client_name': 'Default Client',
    'brand_mappings': {
        'Castorama_FR': 'Nordic Acoustics',
        'Castorama_PL': 'Nordic Acoustics', 
        'LM_product': 'NORDIC ACOUSTICS',
        'Maxeda_BE': 'Nordic Acoustics',
        'Maxeda_NL': 'Nordic Acoustics'
    },
    'default_values': {
        'Manufacturer Name': 'Nordic Acoustics',
        'Brand Name': 'Nordic Acoustics',
        'Brand': 'NORDIC ACOUSTICS'
    },
    'settings': {
        'auto_fill_brand': True,
        'auto_fill_manufacturer': True,
        'case_sensitive_brand': False
    }
}

class ClientConfig:
    """Manages client-specific configurations."""
    
    def __init__(self, client_name: str = 'Default Client'):
        self.client_name = client_name
        self.config = self._load_client_config(client_name)
    
    def _load_client_config(self, client_name: str) -> Dict:
        """Load client configuration from file or use default."""
        config_file = Path("data/config/clients.csv")
        
        if config_file.exists():
            try:
                return self._load_from_csv(config_file, client_name)
            except Exception as e:
                logger.warning(f"Error loading client config from CSV: {e}")
                return self._create_default_config(client_name)
        else:
            return self._create_default_config(client_name)
    
    def _load_from_csv(self, config_file: Path, client_name: str) -> Dict:
        """Load client configuration from CSV file."""
        config = DEFAULT_CLIENT_CONFIG.copy()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row['client_name'] == client_name:
                    # Parse brand mappings
                    brand_mappings = {}
                    for platform in ['Castorama_FR', 'Castorama_PL', 'LM_product', 'Maxeda_BE', 'Maxeda_NL']:
                        if row.get(f'brand_{platform}'):
                            brand_mappings[platform] = row[f'brand_{platform}']
                    
                    config['client_name'] = client_name
                    config['brand_mappings'] = brand_mappings
                    config['default_values'] = {
                        'Manufacturer Name': brand_mappings.get('Castorama_FR', 'Nordic Acoustics'),
                        'Brand Name': brand_mappings.get('Maxeda_BE', 'Nordic Acoustics'),
                        'Brand': brand_mappings.get('LM_product', 'NORDIC ACOUSTICS')
                    }
                    break
        
        return config
    
    def _create_default_config(self, client_name: str) -> Dict:
        """Create default configuration for a client."""
        config = DEFAULT_CLIENT_CONFIG.copy()
        config['client_name'] = client_name
        return config
    
    def get_brand_for_platform(self, platform: str) -> str:
        """Get brand name for a specific platform."""
        return self.config['brand_mappings'].get(platform, 'Unknown Brand')
    
    def get_default_value(self, field_name: str) -> str:
        """Get default value for a specific field."""
        return self.config['default_values'].get(field_name, '')
    
    def should_auto_fill(self, field_type: str) -> bool:
        """Check if a field type should be auto-filled."""
        return self.config['settings'].get(f'auto_fill_{field_type}', False)
    
    def get_all_brand_mappings(self) -> Dict[str, str]:
        """Get all brand mappings for this client."""
        return self.config['brand_mappings'].copy()
    
    def get_client_name(self) -> str:
        """Get the client name."""
        return self.config['client_name']

def create_client_config_csv():
    """Create a sample client configuration CSV file."""
    config_dir = Path("data/config")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "clients.csv"
    
    # Sample client data
    clients = [
        {
            'client_name': 'Nordic Acoustics',
            'brand_Castorama_FR': 'Nordic Acoustics',
            'brand_Castorama_PL': 'Nordic Acoustics',
            'brand_LM_product': 'NORDIC ACOUSTICS',
            'brand_Maxeda_BE': 'Nordic Acoustics',
            'brand_Maxeda_NL': 'Nordic Acoustics',
            'notes': 'Main client - flooring products'
        },
        {
            'client_name': 'TimberCraft',
            'brand_Castorama_FR': 'TimberCraft',
            'brand_Castorama_PL': 'TimberCraft',
            'brand_LM_product': 'TIMBERCRAFT',
            'brand_Maxeda_BE': 'TimberCraft',
            'brand_Maxeda_NL': 'TimberCraft',
            'notes': 'Sample client - wood products'
        },
        {
            'client_name': 'MetalWorks',
            'brand_Castorama_FR': 'MetalWorks',
            'brand_Castorama_PL': 'MetalWorks',
            'brand_LM_product': 'METALWORKS',
            'brand_Maxeda_BE': 'MetalWorks',
            'brand_Maxeda_NL': 'MetalWorks',
            'notes': 'Sample client - metal products'
        }
    ]
    
    # Write to CSV
    with open(config_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['client_name', 'brand_Castorama_FR', 'brand_Castorama_PL', 
                     'brand_LM_product', 'brand_Maxeda_BE', 'brand_Maxeda_NL', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clients)
    
    logger.info(f"Created client configuration file: {config_file}")
    return config_file

def get_client_config(client_name: str = 'Nordic Acoustics') -> ClientConfig:
    """Get client configuration for a specific client."""
    return ClientConfig(client_name)

def list_available_clients() -> List[str]:
    """List all available clients."""
    config_file = Path("data/config/clients.csv")
    
    if not config_file.exists():
        return ['Default Client']
    
    clients = []
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clients.append(row['client_name'])
    except Exception as e:
        logger.error(f"Error reading client list: {e}")
        clients = ['Default Client']
    
    return clients

def add_new_client(client_name: str, brand_mappings: Dict[str, str], notes: str = ""):
    """Add a new client to the configuration."""
    config_file = Path("data/config/clients.csv")
    
    # Ensure config directory exists
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Prepare row data
    row_data = {
        'client_name': client_name,
        'brand_Castorama_FR': brand_mappings.get('Castorama_FR', ''),
        'brand_Castorama_PL': brand_mappings.get('Castorama_PL', ''),
        'brand_LM_product': brand_mappings.get('LM_product', ''),
        'brand_Maxeda_BE': brand_mappings.get('Maxeda_BE', ''),
        'brand_Maxeda_NL': brand_mappings.get('Maxeda_NL', ''),
        'notes': notes
    }
    
    # Check if file exists and has headers
    file_exists = config_file.exists()
    
    with open(config_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['client_name', 'brand_Castorama_FR', 'brand_Castorama_PL', 
                     'brand_LM_product', 'brand_Maxeda_BE', 'brand_Maxeda_NL', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(row_data)
    
    logger.info(f"Added new client: {client_name}")

def update_client_brand(client_name: str, platform: str, new_brand: str):
    """Update brand name for a specific client and platform."""
    config_file = Path("data/config/clients.csv")
    
    if not config_file.exists():
        logger.error("Client configuration file not found")
        return False
    
    # Read all rows
    rows = []
    with open(config_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['client_name'] == client_name:
                row[f'brand_{platform}'] = new_brand
            rows.append(row)
    
    # Write back to file
    with open(config_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['client_name', 'brand_Castorama_FR', 'brand_Castorama_PL', 
                     'brand_LM_product', 'brand_Maxeda_BE', 'brand_Maxeda_NL', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    logger.info(f"Updated brand for {client_name} on {platform}: {new_brand}")
    return True 