"""
Translation utilities for the multimarketplace upload system.

This module handles:
- Translation service integration
- Language detection and mapping
- Translation quality validation
"""

import pandas as pd
from typing import Optional, Dict
import logging

from ..config.settings import TRANSLATION_PLACEHOLDER_PREFIX

logger = logging.getLogger(__name__)

def translate_content(text: str, target_language: str) -> str:
    """
    Translate content to target language.
    
    This is a placeholder function that should be replaced with actual
    translation service integration. Current options include:
    - Google Translate API
    - DeepL API
    - Azure Translator
    - Custom translation service
    
    Args:
        text: Text to translate
        target_language: Target language code (e.g., 'fr', 'nl', 'pl')
    
    Returns:
        Translated text
    """
    if pd.isna(text) or text == '':
        return ''
    
    # Placeholder translation logic
    # In production, this would call a real translation service
    if TRANSLATION_PLACEHOLDER_PREFIX:
        return f"[{target_language.upper()}] {text}"
    else:
        return text

def translate_batch(texts: list, target_language: str) -> list:
    """
    Translate a batch of texts to target language.
    
    Args:
        texts: List of texts to translate
        target_language: Target language code
    
    Returns:
        List of translated texts
    """
    return [translate_content(text, target_language) for text in texts]

def validate_translation(original: str, translated: str, target_language: str) -> bool:
    """
    Validate translation quality.
    
    Args:
        original: Original text
        translated: Translated text
        target_language: Target language
    
    Returns:
        True if translation is valid, False otherwise
    """
    # Basic validation - check if translation is not empty
    if not translated or translated.strip() == '':
        return False
    
    # Check if translation is not identical to original (for non-English targets)
    if target_language != 'en' and original.lower() == translated.lower():
        logger.warning(f"Translation may be identical to original: {original}")
        return False
    
    return True

def get_supported_languages() -> dict:
    """
    Get list of supported languages for translation.
    
    Returns:
        Dictionary mapping language codes to language names
    """
    return {
        'en': 'English',
        'fr': 'French',
        'nl': 'Dutch',
        'pl': 'Polish',
        'de': 'German',
        'es': 'Spanish',
        'it': 'Italian',
        'pt': 'Portuguese'
    }

def detect_language(text: str) -> Optional[str]:
    """
    Detect the language of the given text.
    
    Args:
        text: Text to analyze
    
    Returns:
        Language code or None if detection fails
    """
    # Placeholder language detection
    # In production, this would use a language detection service
    if not text or pd.isna(text):
        return None
    
    # Simple heuristic-based detection
    text_lower = text.lower()
    
    # French indicators
    if any(word in text_lower for word in ['le', 'la', 'les', 'un', 'une', 'et', 'ou']):
        return 'fr'
    
    # Dutch indicators
    if any(word in text_lower for word in ['de', 'het', 'een', 'en', 'of', 'voor']):
        return 'nl'
    
    # Polish indicators
    if any(word in text_lower for word in ['jest', 'to', 'w', 'na', 'z', 'do']):
        return 'pl'
    
    # Default to English
    return 'en'

def format_translation_error(error: Exception, text: str, target_language: str) -> str:
    """
    Format translation error message.
    
    Args:
        error: Translation error
        text: Original text that failed to translate
        target_language: Target language
    
    Returns:
        Formatted error message
    """
    return f"Translation failed for '{text[:50]}...' to {target_language}: {str(error)}"

# Translation service integration placeholders

class TranslationService:
    """Base class for translation services."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """Translate text to target language."""
        raise NotImplementedError("Subclasses must implement translate method")
    
    def translate_batch(self, texts: list, target_language: str, source_language: Optional[str] = None) -> list:
        """Translate a batch of texts."""
        return [self.translate(text, target_language, source_language) for text in texts]

class GoogleTranslateService(TranslationService):
    """Google Translate API integration."""
    
    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate using Google Translate API.
        
        Requires: pip install google-cloud-translate
        """
        try:
            from google.cloud import translate_v2 as translate
            
            client = translate.Client()
            result = client.translate(
                text,
                target_language=target_language,
                source_language=source_language
            )
            
            return result['translatedText']
        except ImportError:
            logger.error("Google Translate API not available. Install with: pip install google-cloud-translate")
            return translate_content(text, target_language)
        except Exception as e:
            logger.error(f"Google Translate error: {e}")
            return translate_content(text, target_language)

class DeepLService(TranslationService):
    """DeepL API integration with usage tracking."""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        from ..config.deepl_config import DeepLUsageTracker, DEEPL_CONFIG
        self.usage_tracker = DeepLUsageTracker()
        self.config = DEEPL_CONFIG
    
    def translate(self, text: str, target_language: str, source_language: Optional[str] = None) -> str:
        """
        Translate using DeepL API with usage tracking.
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'FR', 'NL', 'PL')
            source_language: Source language code (optional)
        
        Returns:
            Translated text or placeholder if limits exceeded
        """
        if not self.api_key:
            logger.warning("No DeepL API key provided")
            return translate_content(text, target_language)
        
        # Check if translation is allowed within limits
        text_length = len(text)
        if not self.usage_tracker.can_translate(text_length):
            logger.warning(f"Translation skipped due to usage limits: {text_length} chars")
            return translate_content(text, target_language)
        
        try:
            import requests
            
            # Prepare request
            headers = {
                'Authorization': f'DeepL-Auth-Key {self.api_key}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'text': text,
                'target_lang': target_language.upper()
            }
            
            if source_language:
                data['source_lang'] = source_language.upper()
            
            # Make API request
            response = requests.post(
                self.config['api_url'],
                headers=headers,
                data=data,
                timeout=self.config['timeout']
            )
            
            if response.status_code == 200:
                result = response.json()
                translated_text = result['translations'][0]['text']
                
                # Record usage
                self.usage_tracker.record_translation(text_length)
                
                logger.info(f"DeepL translation successful: {text[:50]}... -> {translated_text[:50]}...")
                return translated_text
                
            elif response.status_code == 456:
                logger.error("DeepL quota exceeded")
                return translate_content(text, target_language)
                
            else:
                logger.error(f"DeepL API error: {response.status_code} - {response.text}")
                return translate_content(text, target_language)
                
        except ImportError:
            logger.error("Requests library not available. Install with: pip install requests")
            return translate_content(text, target_language)
        except Exception as e:
            logger.error(f"DeepL translation error: {e}")
            return translate_content(text, target_language)
    
    def get_usage_summary(self) -> Dict:
        """Get current usage summary."""
        return self.usage_tracker.get_usage_summary()
    
    def can_translate(self, text_length: int) -> bool:
        """Check if translation is allowed within limits."""
        return self.usage_tracker.can_translate(text_length) 