"""
DeepL API configuration and usage tracking.

This module handles:
- DeepL API configuration
- Usage tracking and limits
- Free tier management
- Rate limiting
"""

import os
import json
from pathlib import Path
from datetime import datetime, date
from typing import Dict, Optional, List
import logging

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, continue without it
    pass

logger = logging.getLogger(__name__)

# DeepL Free Tier Limits
DEEPL_FREE_LIMITS = {
    'monthly_characters': 500000,  # 500k characters per month
    'daily_requests': 1000,        # 1000 requests per day
    'concurrent_requests': 1        # 1 concurrent request
}

# DeepL API Configuration
DEEPL_CONFIG = {
    'api_url': 'https://api-free.deepl.com/v2/translate',  # Free API endpoint
    'timeout': 30,  # seconds
    'retry_attempts': 3,
    'batch_size': 50,  # characters per batch to stay within limits
}

class DeepLUsageTracker:
    """Track DeepL API usage to stay within free tier limits."""
    
    def __init__(self, usage_file: str = 'data/config/deepl_usage.json'):
        self.usage_file = Path(usage_file)
        self.usage_file.parent.mkdir(parents=True, exist_ok=True)
        self.usage_data = self._load_usage_data()
    
    def _load_usage_data(self) -> Dict:
        """Load usage data from file."""
        if self.usage_file.exists():
            try:
                with open(self.usage_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading usage data: {e}")
                return self._create_default_usage()
        else:
            return self._create_default_usage()
    
    def _create_default_usage(self) -> Dict:
        """Create default usage structure."""
        today = date.today().isoformat()
        return {
            'current_month': today[:7],  # YYYY-MM
            'daily_usage': {
                today: {
                    'characters': 0,
                    'requests': 0
                }
            },
            'monthly_usage': {
                'characters': 0,
                'requests': 0
            },
            'last_reset': today
        }
    
    def _save_usage_data(self):
        """Save usage data to file."""
        try:
            with open(self.usage_file, 'w') as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")
    
    def _reset_monthly_usage(self):
        """Reset monthly usage if it's a new month."""
        current_month = date.today().strftime('%Y-%m')
        if self.usage_data['current_month'] != current_month:
            self.usage_data['current_month'] = current_month
            self.usage_data['monthly_usage'] = {
                'characters': 0,
                'requests': 0
            }
            logger.info(f"Reset monthly usage for {current_month}")
    
    def _reset_daily_usage(self):
        """Reset daily usage if it's a new day."""
        today = date.today().isoformat()
        if today not in self.usage_data['daily_usage']:
            self.usage_data['daily_usage'] = {
                today: {
                    'characters': 0,
                    'requests': 0
                }
            }
            logger.info(f"Reset daily usage for {today}")
    
    def can_translate(self, text_length: int) -> bool:
        """Check if translation is allowed within limits."""
        self._reset_monthly_usage()
        self._reset_daily_usage()
        
        today = date.today().isoformat()
        daily_usage = self.usage_data['daily_usage'][today]
        monthly_usage = self.usage_data['monthly_usage']
        
        # Check daily limits
        if daily_usage['requests'] >= DEEPL_FREE_LIMITS['daily_requests']:
            logger.warning("Daily request limit reached")
            return False
        
        if daily_usage['characters'] + text_length > DEEPL_FREE_LIMITS['monthly_characters']:
            logger.warning("Daily character limit would be exceeded")
            return False
        
        # Check monthly limits
        if monthly_usage['characters'] + text_length > DEEPL_FREE_LIMITS['monthly_characters']:
            logger.warning("Monthly character limit would be exceeded")
            return False
        
        return True
    
    def record_translation(self, text_length: int):
        """Record a translation usage."""
        today = date.today().isoformat()
        
        # Update daily usage
        self.usage_data['daily_usage'][today]['characters'] += text_length
        self.usage_data['daily_usage'][today]['requests'] += 1
        
        # Update monthly usage
        self.usage_data['monthly_usage']['characters'] += text_length
        self.usage_data['monthly_usage']['requests'] += 1
        
        self._save_usage_data()
        
        logger.info(f"Recorded translation: {text_length} chars, "
                   f"Daily: {self.usage_data['daily_usage'][today]['characters']}/{DEEPL_FREE_LIMITS['monthly_characters']} chars, "
                   f"Monthly: {self.usage_data['monthly_usage']['characters']}/{DEEPL_FREE_LIMITS['monthly_characters']} chars")
    
    def get_usage_summary(self) -> Dict:
        """Get current usage summary."""
        self._reset_monthly_usage()
        self._reset_daily_usage()
        
        today = date.today().isoformat()
        daily_usage = self.usage_data['daily_usage'].get(today, {'characters': 0, 'requests': 0})
        monthly_usage = self.usage_data['monthly_usage']
        
        return {
            'daily': {
                'characters': daily_usage['characters'],
                'requests': daily_usage['requests'],
                'limit_characters': DEEPL_FREE_LIMITS['monthly_characters'],
                'limit_requests': DEEPL_FREE_LIMITS['daily_requests']
            },
            'monthly': {
                'characters': monthly_usage['characters'],
                'requests': monthly_usage['requests'],
                'limit_characters': DEEPL_FREE_LIMITS['monthly_characters'],
                'limit_requests': None  # No monthly request limit
            },
            'remaining': {
                'daily_characters': DEEPL_FREE_LIMITS['monthly_characters'] - daily_usage['characters'],
                'daily_requests': DEEPL_FREE_LIMITS['daily_requests'] - daily_usage['requests'],
                'monthly_characters': DEEPL_FREE_LIMITS['monthly_characters'] - monthly_usage['characters']
            }
        }

def get_deepl_api_key() -> Optional[str]:
    """Get DeepL API key from environment or config."""
    # Try environment variable first (DEEPL_key from .env)
    api_key = os.getenv('DEEPL_key')
    if api_key:
        return api_key
    
    # Fallback to DEEPL_API_KEY for compatibility
    api_key = os.getenv('DEEPL_API_KEY')
    if api_key:
        return api_key
    
    # Try config file
    config_file = Path('data/config/deepl_config.json')
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('api_key')
        except Exception as e:
            logger.error(f"Error reading DeepL config: {e}")
    
    return None

def save_deepl_api_key(api_key: str):
    """Save DeepL API key to config file."""
    config_file = Path('data/config/deepl_config.json')
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    config = {
        'api_key': api_key,
        'created_at': datetime.now().isoformat()
    }
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info("DeepL API key saved to config file")
    except Exception as e:
        logger.error(f"Error saving DeepL API key: {e}")

def validate_deepl_api_key(api_key: str) -> bool:
    """Validate DeepL API key by making a test request."""
    try:
        import requests
        
        headers = {
            'Authorization': f'DeepL-Auth-Key {api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'text': 'Hello',
            'target_lang': 'FR'
        }
        
        response = requests.post(
            DEEPL_CONFIG['api_url'],
            headers=headers,
            data=data,
            timeout=DEEPL_CONFIG['timeout']
        )
        
        if response.status_code == 200:
            logger.info("DeepL API key is valid")
            return True
        else:
            logger.error(f"DeepL API key validation failed: {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"Error validating DeepL API key: {e}")
        return False 