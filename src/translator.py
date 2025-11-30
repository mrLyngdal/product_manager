"""
DeepL translation module.
Translates empty language fields from English version.
"""

import pandas as pd
import requests
import os
from pathlib import Path
from typing import Dict, List, Optional
import logging
import time

from .config import INPUT_DIR

logger = logging.getLogger(__name__)

# DeepL API configuration
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"

# Supported languages and their DeepL codes
LANGUAGE_CODES = {
    'en': 'EN',
    'fr': 'FR',
    'it': 'IT',
    'es': 'ES',
    'de': 'DE',
    'nl': 'NL',
    'pl': 'PL',
    'pt': 'PT'
}


def get_deepl_api_key() -> Optional[str]:
    """Get DeepL API key from environment variable."""
    api_key = os.getenv(DEEPL_API_KEY_ENV)
    if not api_key:
        # Try .env file
        env_file = Path(__file__).parent.parent / '.env'
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    if line.startswith('DEEPL_API_KEY') or line.startswith('DEEPL_key'):
                        api_key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
    return api_key


def translate_text(text: str, target_lang: str, source_lang: str = 'EN') -> Optional[str]:
    """
    Translate text using DeepL API.
    
    Args:
        text: Text to translate
        target_lang: Target language code (e.g., 'FR', 'IT')
        source_lang: Source language code (default: 'EN')
    
    Returns:
        Translated text or None if translation fails
    """
    api_key = get_deepl_api_key()
    if not api_key:
        logger.error("DeepL API key not found. Set DEEPL_API_KEY environment variable or add to .env file")
        return None
    
    try:
        params = {
            'auth_key': api_key,
            'text': text,
            'target_lang': target_lang,
            'source_lang': source_lang
        }
        
        response = requests.post(DEEPL_API_URL, data=params, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        translated_text = result['translations'][0]['text']
        
        logger.debug(f"Translated '{text[:50]}...' to {target_lang}: '{translated_text[:50]}...'")
        return translated_text
        
    except requests.exceptions.RequestException as e:
        logger.error(f"DeepL API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return None


def identify_translatable_fields(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Identify translatable field patterns (title_*, description_*, etc.) and their language variants.
    
    Args:
        df: Input DataFrame
    
    Returns:
        Dict mapping base field to list of language columns: {'title': ['title_en', 'title_fr', ...]}
    """
    translatable_fields = {}
    
    # Common translatable field prefixes
    # Note: 'desciption' is included to handle common typo (missing 'r')
    prefixes = ['title', 'description', 'desciption', 'short_description', 'long_description']
    
    for col in df.columns:
        col_lower = str(col).lower()
        
        # Check if column matches pattern: prefix_langcode
        for prefix in prefixes:
            if col_lower.startswith(prefix + '_'):
                lang_code = col_lower.replace(prefix + '_', '')
                
                # Check if it's a valid language code
                if lang_code in LANGUAGE_CODES:
                    if prefix not in translatable_fields:
                        translatable_fields[prefix] = []
                    translatable_fields[prefix].append(col)
    
    return translatable_fields


def translate_input_file(input_file: str) -> bool:
    """
    Translate empty language fields in input file from English version.
    
    Logic:
    - For each translatable field pattern (title, description, etc.):
      - Find English version (title_en, description_en)
      - For each other language (title_fr, title_it, etc.):
        - If empty and English exists, translate from English
        - If not empty, skip (don't overwrite)
    
    Args:
        input_file: Input filename in data/input/
    
    Returns:
        True if successful, False otherwise
    """
    try:
        input_path = INPUT_DIR / input_file
        if not input_path.exists():
            logger.error(f"Input file not found: {input_path}")
            return False
        
        # Load input file
        df = pd.read_excel(input_path)
        logger.info(f"Loaded {len(df)} products from {input_file}")
        
        # Identify translatable fields
        translatable_fields = identify_translatable_fields(df)
        
        if not translatable_fields:
            logger.info("No translatable fields found in input file")
            return True
        
        logger.info(f"Found translatable field patterns: {list(translatable_fields.keys())}")
        
        # Track translation stats
        translations_made = 0
        translations_skipped = 0
        
        # Process each translatable field pattern
        for base_field, language_columns in translatable_fields.items():
            # Find English column
            en_column = None
            for col in language_columns:
                if str(col).lower().endswith('_en'):
                    en_column = col
                    break
            
            if not en_column:
                logger.warning(f"No English version found for {base_field}, skipping translation")
                continue
            
            # Process each row
            for idx, row in df.iterrows():
                # Get English text
                en_text = row[en_column]
                if pd.isna(en_text) or str(en_text).strip() == '':
                    continue  # No English text to translate from
                
                en_text = str(en_text).strip()
                
                # Translate to each other language
                for lang_col in language_columns:
                    # Skip English column
                    if lang_col == en_column:
                        continue
                    
                    # Check if already filled
                    current_value = row[lang_col]
                    if pd.notna(current_value) and str(current_value).strip() != '':
                        translations_skipped += 1
                        continue  # Already has value, don't overwrite
                    
                    # Extract target language code from column name
                    # Handle both 'title_fr' and 'Title_FR' patterns
                    col_lower = str(lang_col).lower()
                    if not col_lower.startswith(base_field + '_'):
                        continue
                    lang_code = col_lower.replace(base_field + '_', '')
                    if lang_code not in LANGUAGE_CODES:
                        continue
                    
                    # Translate
                    target_lang = LANGUAGE_CODES[lang_code]
                    logger.info(f"Translating {base_field} row {idx+1} to {lang_code}...")
                    
                    translated = translate_text(en_text, target_lang, 'EN')
                    
                    if translated:
                        df.at[idx, lang_col] = translated
                        translations_made += 1
                        logger.info(f"✓ Translated to {lang_code}")
                    else:
                        logger.warning(f"✗ Translation failed for {lang_code}")
                    
                    # Rate limiting - DeepL free tier allows 1 request per second
                    time.sleep(1.1)
        
        # Save translated file (overwrite original)
        df.to_excel(input_path, index=False)
        
        logger.info(f"Translation complete: {translations_made} translations made, {translations_skipped} skipped (already filled)")
        return True
        
    except Exception as e:
        logger.error(f"Error translating input file: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

