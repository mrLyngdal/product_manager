"""
Core header extraction functionality for the multimarketplace upload system.

This module handles:
- Extracting column headers from Excel files
- Consolidating headers into a unified template
- Managing the extraction process
"""

import pandas as pd
import csv
from pathlib import Path
from typing import List, Set, Dict
import logging

from ..config.settings import INPUT_FILES, MASTER_TEMPLATE_FILE, DEFAULT_ENCODING

logger = logging.getLogger(__name__)

class HeaderExtractor:
    """Extracts and consolidates headers from multiple marketplace files."""
    
    def __init__(self):
        self.all_headers: Set[str] = set()
        self.platform_headers: Dict[str, List[str]] = {}
    
    def extract_headers_from_excel(self, file_path: Path) -> List[str]:
        """Extract column headers from an Excel file."""
        try:
            # Read the Excel file
            df = pd.read_excel(file_path)
            # Get column headers
            headers = list(df.columns)
            logger.info(f"Extracted {len(headers)} headers from {file_path}")
            return headers
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return []
    
    def extract_all_headers(self) -> Dict[str, List[str]]:
        """Extract headers from all input files."""
        platform_headers = {}
        
        for platform, file_path in INPUT_FILES.items():
            if file_path.exists():
                headers = self.extract_headers_from_excel(file_path)
                platform_headers[platform] = headers
                self.all_headers.update(headers)
            else:
                logger.warning(f"File not found: {file_path}")
        
        self.platform_headers = platform_headers
        return platform_headers
    
    def consolidate_headers(self) -> List[str]:
        """Consolidate all headers into a unique sorted list."""
        unique_headers = sorted(list(self.all_headers))
        logger.info(f"Consolidated {len(unique_headers)} unique headers from all platforms")
        return unique_headers
    
    def create_master_template(self, headers: List[str]) -> bool:
        """Create the master template CSV file."""
        try:
            # Ensure templates directory exists
            MASTER_TEMPLATE_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(MASTER_TEMPLATE_FILE, 'w', newline='', encoding=DEFAULT_ENCODING) as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
            
            logger.info(f"Created master template: {MASTER_TEMPLATE_FILE}")
            logger.info(f"Template contains {len(headers)} unique columns")
            return True
        except Exception as e:
            logger.error(f"Error creating master template: {e}")
            return False
    
    def get_extraction_summary(self) -> Dict:
        """Get a summary of the extraction process."""
        summary = {
            'total_platforms': len(self.platform_headers),
            'total_unique_headers': len(self.all_headers),
            'platforms_processed': list(self.platform_headers.keys()),
            'headers_per_platform': {
                platform: len(headers) 
                for platform, headers in self.platform_headers.items()
            }
        }
        return summary
    
    def run_extraction(self) -> bool:
        """Run the complete header extraction process."""
        logger.info("Starting header extraction process...")
        
        # Extract headers from all files
        self.extract_all_headers()
        
        # Consolidate headers
        unique_headers = self.consolidate_headers()
        
        # Create master template
        success = self.create_master_template(unique_headers)
        
        if success:
            summary = self.get_extraction_summary()
            logger.info("Header extraction completed successfully")
            logger.info(f"Summary: {summary}")
        
        return success

def extract_headers_from_files(file_paths: List[Path]) -> List[str]:
    """Extract headers from a list of Excel files."""
    extractor = HeaderExtractor()
    all_headers = set()
    
    for file_path in file_paths:
        if file_path.exists():
            headers = extractor.extract_headers_from_excel(file_path)
            all_headers.update(headers)
        else:
            logger.warning(f"File not found: {file_path}")
    
    return sorted(list(all_headers))

def create_template_from_headers(headers: List[str], output_path: Path) -> bool:
    """Create a template CSV file from a list of headers."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding=DEFAULT_ENCODING) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
        
        logger.info(f"Created template: {output_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating template: {e}")
        return False 