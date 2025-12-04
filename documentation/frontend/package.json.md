# frontend/package.json

## 📋 Overview
Frontend package configuration file that defines dependencies, scripts, and build settings for the KrishiSaathi React application.

## 🎯 Purpose
- Manage React application dependencies
- Define build and development scripts
- Configure development tools and linting
- Set up proxy for API communication
- Manage browser compatibility settings

## 📦 Dependencies

### Core React Dependencies
```json
{
  "react": "^19.1.1",           // Latest React framework
  "react-dom": "^19.1.1",      // React DOM rendering
  "react-scripts": "5.0.1"     // Create React App build tools
}
```

### UI and Icons
```json
{
  "lucide-react": "^0.411.0"   // Modern icon library with 1000+ icons
}
```

### Testing Framework
```json
{
  "@testing-library/dom": "^10.4.1",
  "@testing-library/jest-dom": "^6.8.0",
  "@testing-library/react": "^16.3.0",
  "@testing-library/user-event": "^13.5.0"
}
```

### Performance Monitoring
```json
{
  "web-vitals": "^2.1.4"       // Core Web Vitals measurement
}
```

## 🛠️ Development Dependencies

### CSS Framework
```json
{
  "tailwindcss": "^3.4.1",     // Utility-first CSS framework
  "autoprefixer": "^10.4.19",  // CSS vendor prefixing
  "postcss": "^8.4.38"         // CSS transformation tool
}
```

## 🚀 Scripts Configuration

### Development Scripts
```json
{
  "start": "npm run dev",                                           // Alias for dev script
  "dev": "node node_modules/react-scripts/bin/react-scripts.js start"  // Development server
}
```

### Build Scripts
```json
{
  "build": "react-scripts build",  // Production build
  "test": "react-scripts test",    // Run test suite
  "eject": "react-scripts eject"   // Eject from Create React App
}
```

## 🌐 Proxy Configuration

### API Proxy Setup
```json
{
  "proxy": "http://127.0.0.1:8000"
}
```

**Purpose**: 
- Automatically proxy API requests to backend server
- Avoid CORS issues during development
- Simplify API calls (no need for full URLs)

**Usage Example**:
```javascript
// Instead of: fetch('http://127.0.0.1:8000/predict/crop')
fetch('/predict/crop')  // Automatically proxied
```

## 🔧 ESLint Configuration

### Linting Rules
```json
{
  "eslintConfig": {
    "extends": [
      "react-app",        // Standard React app rules
      "react-app/jest"    // Jest testing rules
    ]
  }
}
```

**Features**:
- React-specific linting rules
- Jest testing environment support
- Automatic code quality checks
- Integration with VS Code and other editors

## 🌍 Browser Support

### Production Browsers
```json
{
  "browserslist": {
    "production": [
      ">0.2%",           // Browsers with >0.2% market share
      "not dead",        // Still maintained browsers
      "not op_mini all"  // Exclude Opera Mini
    ]
  }
}
```

### Development Browsers
```json
{
  "development": [
    "last 1 chrome version",   // Latest Chrome
    "last 1 firefox version",  // Latest Firefox
    "last 1 safari version"    // Latest Safari
  ]
}
```

## 📊 Package Analysis

### Bundle Size Optimization
- **React 19**: Latest features with improved performance
- **Lucide React**: Tree-shakeable icons (only used icons bundled)
- **Tailwind CSS**: Purged CSS (unused styles removed)

### Security Considerations
- **Regular Updates**: All dependencies use latest stable versions
- **Vulnerability Scanning**: npm audit for security issues
- **Trusted Sources**: All packages from verified publishers

## 🎨 Styling Architecture

### Tailwind CSS Integration
```json
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### CSS Processing Pipeline
1. **Tailwind CSS**: Utility classes generation
2. **PostCSS**: CSS transformation and optimization
3. **Autoprefixer**: Vendor prefix addition
4. **PurgeCSS**: Unused CSS removal (production)

## 🚀 Development Workflow

### Local Development
```bash
npm install          # Install dependencies
npm run dev         # Start development server
npm test            # Run test suite
npm run build       # Create production build
```

### Development Server Features
- **Hot Reload**: Automatic page refresh on changes
- **Error Overlay**: In-browser error display
- **Source Maps**: Debug original source code
- **Proxy Support**: API requests forwarded to backend

## 📱 Mobile Development

### Responsive Design Support
- **Tailwind Breakpoints**: Mobile-first responsive utilities
- **Touch Optimization**: Touch-friendly UI components
- **Performance**: Optimized for mobile networks

### PWA Capabilities
- **Service Worker**: Offline functionality (configurable)
- **Web App Manifest**: Install as mobile app
- **Performance Metrics**: Core Web Vitals tracking

## 🔍 Testing Configuration

### Testing Libraries
- **React Testing Library**: Component testing utilities
- **Jest DOM**: Custom Jest matchers for DOM
- **User Event**: Simulate user interactions
- **DOM Testing**: DOM manipulation testing

### Test Environment
```json
{
  "scripts": {
    "test": "react-scripts test"  // Interactive test runner
  }
}
```

**Features**:
- Watch mode for continuous testing
- Coverage reporting
- Snapshot testing support
- Mocking capabilities

## 🌐 Deployment Configuration

### Build Optimization
```bash
npm run build
```

**Output**:
- Minified JavaScript bundles
- Optimized CSS files
- Compressed images and assets
- Service worker (if enabled)

### Static File Serving
- **Build Directory**: `build/`
- **Entry Point**: `build/index.html`
- **Asset Optimization**: Automatic compression and caching

## 📈 Performance Monitoring

### Web Vitals Integration
```javascript
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Measure Core Web Vitals
getCLS(console.log);  // Cumulative Layout Shift
getFID(console.log);  // First Input Delay
getFCP(console.log);  // First Contentful Paint
getLCP(console.log);  // Largest Contentful Paint
getTTFB(console.log); // Time to First Byte
```

### Bundle Analysis
```bash
npm run build
npx serve -s build    # Serve production build locally
```

## 🔧 Customization Options

### Ejecting (Advanced)
```bash
npm run eject  # Irreversible - exposes all configuration
```

**Provides Access To**:
- Webpack configuration
- Babel configuration
- ESLint configuration
- Jest configuration

### Alternative: CRACO
```bash
npm install @craco/craco
```
**Benefits**:
- Customize without ejecting
- Maintain upgrade path
- Override specific configurations

## 🚨 Common Issues & Solutions

### Dependency Conflicts
```bash
npm ls                    # Check dependency tree
npm audit                # Security vulnerability check
npm audit fix            # Auto-fix vulnerabilities
```

### Build Issues
```bash
rm -rf node_modules package-lock.json
npm install              # Clean reinstall
npm run build           # Retry build
```

### Proxy Issues
- Ensure backend server is running on port 8000
- Check firewall settings
- Verify API endpoints are accessible

---

**File Location**: `/frontend/package.json`  
**Type**: NPM Package Configuration  
**Framework**: React 19 with Create React App  
**Styling**: Tailwind CSS  
**Icons**: Lucide React  
**Testing**: React Testing Library + Jest  
**Development Server**: React Scripts with proxy to port 8000