# 🔑 DEEPL API KEY SETUP WITH .ENV

## ✅ **QUICK SETUP**

### **1. Add API Key to .env File**
```bash
# Create or edit your .env file
echo "DEEPL_key=your_actual_api_key_here" >> .env
```

### **2. Install Dependencies**
```bash
pip install python-dotenv
```

### **3. Test the Setup**
```bash
# Check usage (should work with .env)
python main.py deepl-usage

# Test translation (if API key is valid)
python main.py deepl-test
```

## 🎯 **ENVIRONMENT VARIABLE SUPPORT**

The system now supports multiple ways to provide the DeepL API key:

### **Priority Order:**
1. **`.env` file**: `DEEPL_key=your_api_key`
2. **Environment variable**: `DEEPL_API_KEY=your_api_key`
3. **Config file**: `data/config/deepl_config.json`

### **Example .env File:**
```env
# DeepL API Configuration
DEEPL_key=your_deepl_api_key_here

# Other environment variables
# DEEPL_API_KEY=alternative_key_name
```

## 🚀 **USAGE**

Once your API key is in the `.env` file:

```bash
# Check usage
python main.py deepl-usage

# Test translation
python main.py deepl-test

# Use in template optimization (automatic)
python main.py optimize-template
```

## 📊 **FEATURES**

- ✅ **Automatic .env loading** with python-dotenv
- ✅ **Fallback support** for different env var names
- ✅ **Usage tracking** to stay within free limits
- ✅ **Graceful fallback** to placeholders if limits exceeded

The DeepL integration is now ready to use with your `.env` file! 