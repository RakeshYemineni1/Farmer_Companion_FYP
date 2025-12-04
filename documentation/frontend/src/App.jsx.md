# frontend/src/App.jsx

## 📋 Overview
Main React application component that serves as the central hub for KrishiSaathi's user interface, integrating crop recommendations, fertilizer suggestions, disease detection, and AI chatbot functionality.

## 🎯 Purpose
- Unified dashboard for all agricultural AI services
- Responsive design for desktop and mobile devices
- Multi-language support with real-time translation
- User authentication and session management
- Seamless integration with backend API services

## 🏗️ Component Architecture

### Main App Component
```jsx
const App = () => {
  // State management for user, languages, translations, and UI
  const [user, setUser] = useState(null);
  const [languages, setLanguages] = useState({});
  const [translations, setTranslations] = useState({});
  const [activeTab, setActiveTab] = useState('crop');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [showComingSoon, setShowComingSoon] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const [showChatBot, setShowChatBot] = useState(() => {
    return localStorage.getItem('krishisaathi_show_chat') === 'true';
  });
```

## 🔧 State Management

### User Authentication State
```jsx
const [user, setUser] = useState(null);

// Load saved user from localStorage
useEffect(() => {
  const savedUser = localStorage.getItem('user');
  if (savedUser) {
    setUser(JSON.parse(savedUser));
  }
}, []);

const handleLogin = (userData) => {
  setUser(userData);
  localStorage.setItem('user', JSON.stringify(userData));
};

const handleLogout = () => {
  setUser(null);
  setResult(null);
  localStorage.removeItem('user');
};
```

### Form State Management
```jsx
// Crop recommendation form
const [cropForm, setCropForm] = useState({
  N: '', P: '', K: '', temperature: '', humidity: '', ph: '', rainfall: ''
});

// Fertilizer recommendation form
const [fertForm, setFertForm] = useState({
  temperature: '', humidity: '', moisture: '', soil_type: '', crop_type: '', N: '', P: '', K: ''
});

// Disease detection
const [diseaseImage, setDiseaseImage] = useState(null);
```

## 🌐 API Integration

### Configuration
```jsx
const API_BASE = 'http://127.0.0.1:8000';
```

### Language Management
```jsx
const fetchLanguages = async () => {
  try {
    const response = await fetch(`${API_BASE}/languages`);
    const data = await response.json();
    setLanguages(data);
  } catch (error) {
    console.error('Failed to fetch languages:', error);
  }
};

const fetchTranslations = async (language) => {
  try {
    const response = await fetch(`${API_BASE}/translations/${language}`);
    const data = await response.json();
    setTranslations(data);
  } catch (error) {
    console.error('Failed to fetch translations:', error);
  }
};
```

## 🌾 Agricultural AI Services

### 1. Crop Recommendation
```jsx
const handleCropSubmit = async () => {
  setLoading(true);
  try {
    const response = await fetch(`${API_BASE}/predict/crop`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        N: parseFloat(cropForm.N),
        P: parseFloat(cropForm.P),
        K: parseFloat(cropForm.K),
        temperature: parseFloat(cropForm.temperature),
        humidity: parseFloat(cropForm.humidity),
        ph: parseFloat(cropForm.ph),
        rainfall: parseFloat(cropForm.rainfall)
      })
    });
    const data = await response.json();
    if (data.success) {
      setResult(data.data);
    } else {
      setResult({ error: data.error });
    }
  } catch (error) {
    setResult({ error: 'Failed to get prediction' });
  }
  setLoading(false);
};
```

### 2. Fertilizer Recommendation
```jsx
const handleFertSubmit = async () => {
  setLoading(true);
  try {
    const response = await fetch(`${API_BASE}/predict/fertilizer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        temperature: parseFloat(fertForm.temperature),
        humidity: parseFloat(fertForm.humidity),
        moisture: parseFloat(fertForm.moisture),
        soil_type: fertForm.soil_type,
        crop_type: fertForm.crop_type,
        N: parseFloat(fertForm.N),
        P: parseFloat(fertForm.P),
        K: parseFloat(fertForm.K)
      })
    });
    const data = await response.json();
    if (data.success) {
      setResult(data.data);
    }
  } catch (error) {
    setResult({ error: 'Failed to get prediction' });
  }
  setLoading(false);
};
```

### 3. Disease Detection
```jsx
const handleDiseaseSubmit = async () => {
  if (!diseaseImage) return;
  
  setLoading(true);
  try {
    const formData = new FormData();
    formData.append('file', diseaseImage);
    
    const response = await fetch(`${API_BASE}/predict/disease`, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    if (data.success) {
      setResult(data.data);
    }
  } catch (error) {
    setResult({ error: 'Failed to get prediction' });
  }
  setLoading(false);
};
```

## 🎨 UI Components

### Navigation Header
```jsx
<header className="bg-white shadow-sm border-b border-green-100">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-green-600 rounded-xl flex items-center justify-center">
          <Leaf className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            <TranslatedText text="KrishiSaathi" language={user?.language} />
          </h1>
          <p className="text-sm text-gray-600">
            <TranslatedText text="Intelligent Farming Solutions" language={user?.language} />
          </p>
        </div>
      </div>
    </div>
  </div>
</header>
```

### Service Tabs
```jsx
<div className="flex flex-wrap justify-center gap-4 mb-8">
  <button
    onClick={() => { setActiveTab('crop'); setResult(null); }}
    className={`px-6 py-3 rounded-xl font-medium transition-all duration-200 flex items-center gap-2 ${
      activeTab === 'crop' 
        ? 'bg-green-500 text-white shadow-lg' 
        : 'bg-white text-gray-700 hover:bg-green-50 border border-green-200'
    }`}
  >
    <Leaf className="w-5 h-5" />
    <TranslatedText text="Crop Recommendation" language={user?.language} />
  </button>
  {/* Similar buttons for fertilizer and disease */}
</div>
```

## 📱 Responsive Design

### Mobile Menu Implementation
```jsx
const [showMobileMenu, setShowMobileMenu] = useState(false);

// Mobile menu toggle
<div className="sm:hidden relative">
  <button
    onClick={() => setShowMobileMenu(!showMobileMenu)}
    className="p-2 text-gray-600 hover:text-gray-800"
  >
    {showMobileMenu ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
  </button>
  
  {/* Mobile dropdown menu */}
  {showMobileMenu && (
    <div className="absolute right-0 top-full mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
      {/* Menu items */}
    </div>
  )}
</div>
```

### Responsive Grid Layout
```jsx
<div className="grid lg:grid-cols-2 gap-8">
  {/* Form Section */}
  <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
    {/* Form content */}
  </div>
  
  {/* Results Section */}
  <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
    {/* Results content */}
  </div>
</div>
```

## 🌍 Internationalization

### Language Switching
```jsx
const changeLanguage = async (newLanguage) => {
  try {
    const response = await fetch(`${API_BASE}/auth/language`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user.username, language: newLanguage })
    });
    if (response.ok) {
      const updatedUser = {...user, language: newLanguage};
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      fetchTranslations(newLanguage);
    }
  } catch (error) {
    console.error('Failed to update language:', error);
  }
};
```

### Translation Component Usage
```jsx
<TranslatedText text="Welcome to KrishiSaathi" language={user?.language} />
```

## 🤖 Chatbot Integration

### Chat State Management
```jsx
const [showChatBot, setShowChatBot] = useState(() => {
  return localStorage.getItem('krishisaathi_show_chat') === 'true';
});

// Save chat visibility state
useEffect(() => {
  localStorage.setItem('krishisaathi_show_chat', showChatBot.toString());
}, [showChatBot]);
```

### Chat Button
```jsx
<button
  onClick={() => setShowChatBot(true)}
  className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-r from-green-500 to-blue-500 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center justify-center z-50 hover:scale-110"
  title="Chat with KrishiSaathi AI"
>
  <MessageCircle className="w-5 h-5 sm:w-6 sm:h-6" />
</button>
```

## 📊 Form Validation & Input Handling

### Input Field Styling
```jsx
const inputClass = "w-full px-4 py-3 border border-green-200 rounded-lg focus:ring-2 focus:ring-green-400 focus:border-transparent outline-none transition-all";
const buttonClass = "w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 px-6 rounded-lg hover:from-green-600 hover:to-green-700 transition-all duration-200 flex items-center justify-center gap-2 font-medium cursor-pointer";
```

### Crop Form Fields
```jsx
<div className="grid md:grid-cols-3 gap-4">
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-2">
      <TranslatedText text="Nitrogen (N)" language={user?.language} />
    </label>
    <input
      type="number"
      className={inputClass}
      value={cropForm.N}
      onChange={(e) => setCropForm({...cropForm, N: e.target.value})}
      placeholder="0-140"
    />
  </div>
  {/* Similar fields for P, K, temperature, humidity, pH, rainfall */}
</div>
```

## 🎯 Results Display

### Success Results
```jsx
{result && !result.error && (
  <div>
    {result.crop && (
      <div className="bg-green-50 border border-green-200 rounded-xl p-6">
        <h4 className="text-lg font-semibold text-green-800 mb-3">
          <TranslatedText text="Recommended Crop" language={user?.language} />
        </h4>
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <div>
            <p className="text-xl font-bold text-green-800 capitalize">{result.crop}</p>
            {result.confidence && (
              <p className="text-green-600">
                <TranslatedText text={`Confidence: ${(result.confidence * 100).toFixed(1)}%`} language={user?.language} />
              </p>
            )}
          </div>
        </div>
      </div>
    )}
  </div>
)}
```

### Error Handling
```jsx
{result && result.error && (
  <div className="bg-red-50 border border-red-200 rounded-xl p-6">
    <h4 className="text-lg font-semibold text-red-800 mb-2">
      <TranslatedText text="Error" language={user?.language} />
    </h4>
    <p className="text-red-600">{result.error}</p>
  </div>
)}
```

## 🚀 Performance Optimizations

### Lazy Loading
```jsx
// Conditional rendering for different views
if (!user) {
  return <Login onLogin={handleLogin} languages={languages} translations={translations} />;
}

if (showComingSoon) {
  return <ComingSoon onBack={() => setShowComingSoon(false)} user={user} />;
}

if (showChatBot) {
  return <ChatBot onBack={() => setShowChatBot(false)} user={user} />;
}
```

### State Persistence
```jsx
// Save user data to localStorage
localStorage.setItem('user', JSON.stringify(userData));

// Save chat visibility preference
localStorage.setItem('krishisaathi_show_chat', showChatBot.toString());
```

## 🎨 Styling & Design System

### Tailwind CSS Classes
```jsx
// Gradient backgrounds
"bg-gradient-to-br from-green-50 to-blue-50"
"bg-gradient-to-r from-green-500 to-green-600"

// Shadows and borders
"shadow-xl border border-gray-100"
"rounded-2xl p-8"

// Responsive design
"max-w-7xl mx-auto px-4 sm:px-6 lg:px-8"
"grid lg:grid-cols-2 gap-8"
```

### Icon Integration
```jsx
import { Upload, Leaf, Droplets, Bug, ChevronRight, TrendingUp, Shield, LogOut, Menu, X, MessageCircle } from 'lucide-react';
```

## 📱 Mobile-First Design

### Responsive Breakpoints
- **Mobile**: Default styles
- **Small (sm)**: 640px and up
- **Large (lg)**: 1024px and up

### Mobile Optimizations
```jsx
// Mobile-specific classes
"w-12 h-12 sm:w-14 sm:h-14"  // Smaller on mobile
"text-sm sm:text-base"        // Smaller text on mobile
"p-2 sm:p-4"                  // Less padding on mobile
"hidden sm:block"             // Hide on mobile
"sm:hidden"                   // Show only on mobile
```

---

**File Location**: `/frontend/src/App.jsx`  
**Type**: React Component (JSX)  
**Dependencies**: React, Lucide React icons, Tailwind CSS  
**Features**: Multi-language, Responsive, AI Integration  
**State Management**: React Hooks, localStorage  
**API Integration**: RESTful backend communication