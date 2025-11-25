# Simple Multimarketplace Product Transformer

A minimalistic system to transform product data into platform-specific Excel files.

## Quick Start

1. **Configure mappings** in `data/config/mapping.xlsx`
   - Specify which column each attribute maps to for each platform
   - Mark attributes as "same" or "platform_specific"

2. **Set attribute values** in `data/config/attributes.xlsx`
   - Same-input attributes: One value for all platforms
   - Platform-specific attributes: Different values per platform

3. **Prepare input file** in `data/input/`
   - One row per product
   - One file per product category (e.g., `acoustic_panels.xlsx`)

4. **Transform**:
   ```bash
   python main.py transform --platform castorama_fr --input acoustic_panels.xlsx
   ```

5. **Find output** in `data/output/`

## Project Structure

```
product_manager/
├── data/
│   ├── input/              # Product input files (one per category)
│   ├── output/             # Generated platform files
│   ├── ref/                # Reference templates (platform structures)
│   └── config/
│       ├── mapping.xlsx     # Column mappings per platform
│       └── attributes.xlsx # Pre-determined attribute values
├── src/
│   ├── config.py           # Platform configuration
│   └── transformer.py      # Core transformation logic
└── main.py                 # CLI entry point
```

## Configuration Files

### mapping.xlsx

**Sheet: Column_Mappings**
- `attribute_name`: Name of the attribute (e.g., "height", "category")
- `data_source`: "input_file" or "punch_card" (where the value comes from)
- `input_type`: "same" or "platform_specific" (how the value varies across platforms)
- `{platform}_column`: Excel column letter (e.g., "BM", "AU")

Example:
| attribute_name | data_source | input_type | castorama_fr_column | leroy_merlin_column |
|---------------|-------------|------------|---------------------|---------------------|
| height | input_file | same | BM | AU |
| category | punch_card | platform_specific | X | Y |

**Data Source Options:**
- `input_file`: Value comes from the product input file (one row per product)
- `punch_card`: Value comes from the attributes.xlsx file (pre-determined values)

**Input Type Options:**
- `same`: Same value for all platforms
- `platform_specific`: Different value per platform

### attributes.xlsx

**Sheet: Same_Input_Attributes**
- Attributes that use the same value across all platforms
- Columns: `attribute_name`, `value`, `unit` (optional)

**Sheet: Platform_Specific_Attributes**
- Attributes that differ per platform
- Columns: `attribute_name`, `{platform}_value`

## Adding a New Platform

1. Add platform to `PLATFORMS` in `src/config.py`
2. Add reference template path to `REF_TEMPLATES` in `src/config.py`
3. Add `{platform}_column` column to `mapping.xlsx`
4. Add `{platform}_value` column to `attributes.xlsx` (for platform-specific attributes)
5. Done! The system automatically handles the new platform.

## How It Works

1. **Load mapping**: Reads which column each attribute maps to for each platform
2. **Load attributes**: Gets pre-determined values (same or platform-specific)
3. **Load input**: Reads product data from input file
4. **Load reference template**: Gets exact structure from platform reference file
5. **Transform**: Maps each product's attributes to the correct columns
6. **Save**: Writes platform-specific output file

## Commands

```bash
# Transform input to platform file
python main.py transform --platform castorama_fr --input acoustic_panels.xlsx

# List supported platforms
python main.py list-platforms
```

## Design Principles

- **Excel-based config**: Edit mappings directly in Excel
- **Minimal code**: ~200 lines total, easy to understand
- **Extensible**: Add platforms by editing config files
- **Simple logic**: Clear separation of "where" (mapping) vs "what" (attributes)

