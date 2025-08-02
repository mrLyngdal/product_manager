import pandas as pd
import random
from pathlib import Path

def generate_sample_products(num_products=5):
    """Generate sample product data for the master template."""
    
    # Sample product data
    sample_products = []
    
    products = [
        {
            'name': 'Premium Wood Flooring',
            'brand': 'TimberCraft',
            'category': 'Flooring',
            'ean': '1234567890123',
            'description': 'High-quality oak wood flooring with natural finish',
            'weight_kg': 15.5,
            'height_mm': 15,
            'width_mm': 200,
            'length_mm': 2000,
            'color': 'Natural Oak',
            'material': 'Solid Oak',
            'coverage_m2': 2.4,
            'price': 89.99
        },
        {
            'name': 'Ceramic Wall Tiles',
            'brand': 'TileMaster',
            'category': 'Tiles',
            'ean': '1234567890124',
            'description': 'White ceramic wall tiles with smooth finish',
            'weight_kg': 8.2,
            'height_mm': 8,
            'width_mm': 250,
            'length_mm': 250,
            'color': 'White',
            'material': 'Ceramic',
            'coverage_m2': 1.0,
            'price': 24.50
        },
        {
            'name': 'LED Ceiling Light',
            'brand': 'LightPro',
            'category': 'Lighting',
            'ean': '1234567890125',
            'description': 'Modern LED ceiling light with remote control',
            'weight_kg': 2.1,
            'height_mm': 80,
            'width_mm': 300,
            'length_mm': 300,
            'color': 'White',
            'material': 'Aluminum',
            'coverage_m2': None,
            'price': 45.99
        },
        {
            'name': 'Garden Hose',
            'brand': 'GardenFlow',
            'category': 'Garden',
            'ean': '1234567890126',
            'description': 'Heavy-duty garden hose with brass fittings',
            'weight_kg': 1.8,
            'height_mm': 25,
            'width_mm': 25,
            'length_mm': 25000,
            'color': 'Green',
            'material': 'PVC',
            'coverage_m2': None,
            'price': 32.75
        },
        {
            'name': 'Paint Roller Set',
            'brand': 'PaintPro',
            'category': 'Painting',
            'ean': '1234567890127',
            'description': 'Professional paint roller set with extension pole',
            'weight_kg': 0.9,
            'height_mm': 150,
            'width_mm': 50,
            'length_mm': 2000,
            'color': 'Multi',
            'material': 'Synthetic',
            'coverage_m2': None,
            'price': 18.99
        }
    ]
    
    for i, product in enumerate(products[:num_products]):
        row = {
            # Core product information
            'EAN': product['ean'],
            'Brand': product['brand'],
            'Code for internal use': product['name'],
            'Category': product['category'],
            'Product Title (Mirakl)': product['name'],
            'Description (Mirakl)': product['description'],
            
            # Physical specifications
            'Product weight (kg)': product['weight_kg'],
            'Product height (mm)': product['height_mm'],
            'Product width (mm)': product['width_mm'],
            'Product length (mm)': product['length_mm'],
            'Product weight (g)': product['weight_kg'] * 1000,
            
            # Material and color
            'Material': product['material'],
            'Colour': product['color'],
            'Main Color': product['color'],
            'Main Material': product['material'],
            
            # Coverage (for applicable products)
            'Coverage (m²)': product['coverage_m2'],
            
            # Images (placeholder URLs)
            'Image 1': f'https://example.com/images/{product["ean"]}_1.jpg',
            'Image 2': f'https://example.com/images/{product["ean"]}_2.jpg',
            'Image 3': f'https://example.com/images/{product["ean"]}_3.jpg',
            'Image 4': f'https://example.com/images/{product["ean"]}_4.jpg',
            'Image 5': f'https://example.com/images/{product["ean"]}_5.jpg',
            
            # Language-specific fields (will be translated by pipeline)
            'Product Title (fr_BE)': product['name'],
            'Product Title (nl_BE)': product['name'],
            'Product Title (nl_NL)': product['name'],
            'Description (fr_BE)': product['description'],
            'Description (nl_BE)': product['description'],
            'Description (nl_NL)': product['description'],
            'Short Description (fr_BE)': product['description'][:100] + '...',
            'Short Description (nl_BE)': product['description'][:100] + '...',
            'Short Description (nl_NL)': product['description'][:100] + '...',
            
            # Additional fields
            'Manufacturer Name': product['brand'],
            'Model name/number': f'MODEL-{i+1:03d}',
            'Product type': 'Physical',
            'Made in': 'Europe',
            'Manufacturing country': 'Germany',
            
            # Certifications and compliance
            'CE marked': 'Yes',
            'UKCA marked': 'No',
            'FSC Mark indicator': 'Yes' if 'Wood' in product['material'] else 'No',
            'PEFC mark indicator': 'Yes' if 'Wood' in product['material'] else 'No',
            
            # Safety and warranty
            'Warranty (in years) (includes the legal conformity warranty)': 2,
            'Manufacturer guarantee': 'Yes',
            'Manufacturer\'s commercial warranty (in years)': 2,
            
            # Product specifications
            'Product Category': product['category'],
            'Type of product': 'Standard',
            'Format': 'Individual',
            'Pack type': 'Single',
            'Pack quantity': 1,
            
            # USPs (Unique Selling Points)
            'Unique Selling Point 1': 'High quality materials',
            'Unique Selling Point 2': 'Professional grade',
            'Unique Selling Point 3': 'Easy installation',
            'USP 1 (fr_BE)': 'High quality materials',
            'USP 1 (nl_BE)': 'High quality materials',
            'USP 1 (nl_NL)': 'High quality materials',
            'USP 2 (fr_BE)': 'Professional grade',
            'USP 2 (nl_BE)': 'Professional grade',
            'USP 2 (nl_NL)': 'Professional grade',
            'USP 3 (fr_BE)': 'Easy installation',
            'USP 3 (nl_BE)': 'Easy installation',
            'USP 3 (nl_NL)': 'Easy installation',
        }
        
        sample_products.append(row)
    
    return sample_products

def create_sample_template():
    """Create a sample populated template for testing."""
    
    print("🎯 Generating sample product data...")
    
    # Generate sample products
    sample_data = generate_sample_products(5)
    
    # Create DataFrame
    df = pd.DataFrame(sample_data)
    
    # Load the master template to get all column headers
    master_template = "data/templates/multimarketplace_master_template.xlsx"
    
    if Path(master_template).exists():
        # Read the master template to get all column headers
        template_df = pd.read_excel(master_template)
        all_columns = list(template_df.columns)
        
        # Create a new DataFrame with all columns from the template
        # Fill missing columns with empty values
        for col in all_columns:
            if col not in df.columns:
                df[col] = ''
        
        # Reorder columns to match the template
        df = df[all_columns]
        
        print(f"✅ Created sample template with {len(df)} products and {len(df.columns)} columns")
        
        # Save the sample template
        output_file = "data/templates/sample_master_template.xlsx"
        df.to_excel(output_file, index=False)
        print(f"💾 Saved sample template: {output_file}")
        
        return output_file
    else:
        print("❌ Master template not found. Please run optimize-template first.")
        return None

def main():
    """Main function to generate sample data."""
    print("🚀 Sample Data Generator for Multimarketplace Template")
    print("=" * 60)
    
    sample_file = create_sample_template()
    
    if sample_file:
        print(f"\n✅ Sample template created: {sample_file}")
        print("\n📝 Next steps:")
        print("1. Review the sample data")
        print("2. Run transform_pipeline.py to test the transformation")
        print("3. Customize the sample data as needed")
    else:
        print("\n❌ Failed to create sample template")

if __name__ == "__main__":
    main() 