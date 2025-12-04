# languages.py

## 📋 Overview
Comprehensive multi-language support module that defines supported Indian languages and provides translation mappings for the KrishiSaathi application interface.

## 🎯 Purpose
- Support for 26 Indian languages and dialects
- Localized user interface translations
- Cultural and linguistic accessibility for Indian farmers
- Standardized language codes and display names

## 🌍 Supported Languages

### INDIAN_LANGUAGES Dictionary
```python
INDIAN_LANGUAGES = {
    'en': 'English',
    'hi': 'हिन्दी (Hindi)',
    'bn': 'বাংলা (Bengali)',
    'te': 'తెలుగు (Telugu)',
    'mr': 'मराठी (Marathi)',
    'ta': 'தமிழ் (Tamil)',
    'gu': 'ગુજરાતી (Gujarati)',
    'kn': 'ಕನ್ನಡ (Kannada)',
    'ml': 'മലയാളം (Malayalam)',
    'pa': 'ਪੰਜਾਬੀ (Punjabi)',
    'or': 'ଓଡ଼ିଆ (Odia)',
    'as': 'অসমীয়া (Assamese)',
    'ur': 'اردو (Urdu)',
    'sa': 'संस्कृत (Sanskrit)',
    'ks': 'कॉशुर (Kashmiri)',
    'sd': 'سنڌي (Sindhi)',
    'ne': 'नेपाली (Nepali)',
    'si': 'සිංහල (Sinhala)',
    'my': 'မြန်မာ (Myanmar)',
    'dz': 'རྫོང་ཁ (Dzongkha)',
    'bh': 'भोजपुरी (Bhojpuri)',
    'mai': 'मैथिली (Maithili)',
    'sat': 'ᱥᱟᱱᱛᱟᱲᱤ (Santali)',
    'kok': 'कोंकणी (Konkani)',
    'mni': 'মৈতৈলোন্ (Manipuri)',
    'doi': 'डोगरी (Dogri)'
}
```

## 📝 Translation System

### Core Interface Elements
The TRANSLATIONS dictionary provides localized text for key UI elements:

#### English (Base Language)
```python
'en': {
    'welcome': 'Welcome to AgriSmart AI',
    'login': 'Login',
    'register': 'Register',
    'username': 'Username',
    'password': 'Password',
    'email': 'Email',
    'language': 'Language',
    'crop_recommendation': 'Crop Recommendation',
    'fertilizer_recommendation': 'Fertilizer Recommendation',
    'disease_detection': 'Disease Detection',
    'logout': 'Logout'
}
```

#### Hindi Translation Example
```python
'hi': {
    'welcome': 'एग्रीस्मार्ट एआई में आपका स्वागत है',
    'login': 'लॉगिन',
    'register': 'पंजीकरण',
    'username': 'उपयोगकर्ता नाम',
    'password': 'पासवर्ड',
    'crop_recommendation': 'फसल सिफारिश',
    'fertilizer_recommendation': 'उर्वरक सिफारिश',
    'disease_detection': 'रोग का पता लगाना'
}
```

## 🔧 Technical Implementation

### Language Code Standards
- **ISO 639-1**: Two-letter language codes (hi, bn, te)
- **Extended Codes**: Three-letter codes for specific dialects (mai, sat, kok)
- **Regional Variants**: Support for regional language variations

### Translation Categories

#### 1. Authentication & Navigation
- Login/Register forms
- User account management
- Navigation menus
- System messages

#### 2. Agricultural Features
- Crop recommendation interface
- Fertilizer suggestion forms
- Disease detection labels
- Input field descriptions

#### 3. Data Input Labels
```python
'nitrogen': 'Nitrogen (N)',
'phosphorus': 'Phosphorus (P)',
'potassium': 'Potassium (K)',
'temperature': 'Temperature (°C)',
'humidity': 'Humidity (%)',
'ph_level': 'pH Level',
'rainfall': 'Rainfall (mm)'
```

## 🌐 Regional Coverage

### Major Language Families
1. **Indo-Aryan**: Hindi, Bengali, Marathi, Gujarati, Punjabi, Urdu
2. **Dravidian**: Telugu, Tamil, Kannada, Malayalam
3. **Sino-Tibetan**: Assamese, Manipuri, Myanmar
4. **Others**: Sanskrit, Santali, Konkani

### Agricultural Regions
- **North India**: Hindi, Punjabi, Urdu
- **South India**: Telugu, Tamil, Kannada, Malayalam
- **East India**: Bengali, Assamese, Odia
- **West India**: Marathi, Gujarati, Konkani
- **Northeast**: Manipuri, Assamese
- **Tribal Languages**: Santali, Bhojpuri

## 🚀 Usage Examples

### Language Selection
```python
from languages import INDIAN_LANGUAGES

# Display language options in UI
for code, name in INDIAN_LANGUAGES.items():
    print(f"{code}: {name}")
```

### Translation Retrieval
```python
from languages import TRANSLATIONS

def get_translation(key, language='en'):
    return TRANSLATIONS.get(language, {}).get(key, TRANSLATIONS['en'][key])

# Usage
welcome_text = get_translation('welcome', 'hi')
print(welcome_text)  # Output: एग्रीस्मार्ट एआई में आपका स्वागत है
```

### API Integration
```python
@app.get("/languages")
def get_languages():
    return INDIAN_LANGUAGES

@app.get("/translations/{language}")
def get_translations_endpoint(language: str):
    return TRANSLATIONS.get(language, TRANSLATIONS['en'])
```

## 📊 Language Statistics

### Script Systems Supported
- **Devanagari**: Hindi, Marathi, Sanskrit, Nepali
- **Bengali**: Bengali, Assamese
- **Tamil**: Tamil script
- **Telugu**: Telugu script
- **Kannada**: Kannada script
- **Malayalam**: Malayalam script
- **Gujarati**: Gujarati script
- **Gurmukhi**: Punjabi script
- **Arabic**: Urdu, Sindhi
- **Latin**: English
- **Ol Chiki**: Santali

### Coverage by Region
- **22 Official Languages**: Covered
- **Regional Dialects**: 4 additional
- **Total Coverage**: 26 languages

## 🔄 Extension Guidelines

### Adding New Languages
1. **Add to INDIAN_LANGUAGES**:
```python
'new_code': 'नया भाषा (New Language)'
```

2. **Add Translation Set**:
```python
'new_code': {
    'welcome': 'Translated welcome message',
    'login': 'Translated login',
    # ... all required keys
}
```

### Translation Quality
- **Native Speakers**: Use native speaker translations
- **Agricultural Context**: Ensure agricultural terminology accuracy
- **Cultural Sensitivity**: Respect cultural nuances
- **Consistency**: Maintain consistent terminology

## 🎯 Accessibility Features

### Font Support
- **Unicode Compliance**: All languages use proper Unicode encoding
- **Font Fallbacks**: System fonts support for all scripts
- **RTL Support**: Right-to-left text for Arabic scripts (Urdu)

### User Experience
- **Language Persistence**: User language preference saved
- **Fallback Mechanism**: English fallback for missing translations
- **Dynamic Switching**: Real-time language switching

## 📈 Performance Considerations

### Memory Usage
- **Static Data**: Translations loaded once at startup
- **Lazy Loading**: Consider lazy loading for large translation sets
- **Caching**: Translation results cached for performance

### Network Optimization
- **Minimal Payload**: Only send required language data
- **Compression**: Use gzip compression for translation data
- **CDN**: Consider CDN for static translation files

## 🔧 Integration Points

### Frontend Integration
```javascript
// React component usage
import { useTranslation } from './hooks/useTranslation';

const { t } = useTranslation(userLanguage);
return <h1>{t('welcome')}</h1>;
```

### Backend Integration
```python
# FastAPI endpoint
from languages import TRANSLATIONS

def get_localized_response(message, language):
    translations = TRANSLATIONS.get(language, TRANSLATIONS['en'])
    return translations.get(message, message)
```

---

**File Location**: `/languages.py`  
**Type**: Python Module  
**Dependencies**: None (pure Python)  
**Used By**: FastAPI endpoints, React components, translation services  
**Encoding**: UTF-8 (required for multi-script support)