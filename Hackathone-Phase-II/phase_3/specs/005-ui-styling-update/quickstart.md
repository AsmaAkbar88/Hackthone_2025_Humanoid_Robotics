# Quickstart Guide: UI/UX Styling Upgrade

## Overview
This guide provides the essential steps to implement the UI/UX styling upgrade with modern 2026 design aesthetics, dual theme support, and premium button experiences.

## Prerequisites
- Node.js 18+ and npm/yarn
- Next.js 16+ project with Tailwind CSS configured
- Understanding of Tailwind CSS utility classes
- Access to project source files

## Implementation Steps

### 1. Configure Tailwind for Themes
Update `tailwind.config.js` to include theme-specific color palettes:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        // Dark theme: black & white only
        dark: {
          primary: '#000000',
          secondary: '#FFFFFF',
          background: '#000000',
          text: '#FFFFFF',
        },
        // Light theme: pink & off-white (black text)
        light: {
          primary: '#FF69B4', // pink
          secondary: '#F8F8F8', // off-white
          background: '#F8F8F8',
          text: '#000000', // black text
        }
      }
    }
  }
}
```

### 2. Create Theme Context
Implement a theme provider to manage dark/light theme switching:

```jsx
// components/ThemeProvider.jsx
import { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => useContext(ThemeContext);

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

### 3. Implement Theme-Specific Styles
Create CSS files for each theme with the appropriate color schemes:

```css
/* styles/themes/dark.css */
[data-theme="dark"] {
  --bg-primary: #000000;
  --bg-secondary: #111111;
  --text-primary: #FFFFFF;
  --text-secondary: #CCCCCC;
  --border-color: #333333;
}

/* styles/themes/light.css */
[data-theme="light"] {
  --bg-primary: #F8F8F8;
  --bg-secondary: #FFFFFF;
  --text-primary: #000000;
  --text-secondary: #333333;
  --border-color: #DDDDDD;
}
```

### 4. Create Premium Button Components
Implement button components with the required hover behaviors:

```jsx
// components/buttons/PremiumButton.jsx
import React from 'react';

const PremiumButton = ({
  variant = 'primary',
  size = 'md',
  disabled = false,
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'rounded-md font-medium transition-all duration-200 ease-in-out';

  const variantClasses = {
    primary: 'bg-light-primary text-light-text hover:bg-opacity-90',
    delete: 'bg-red-600 text-white hover:bg-red-700 hover:scale-105', // danger styling
    edit: 'bg-light-secondary text-black hover:bg-gray-200 hover:shadow-md', // premium non-danger
    task: 'bg-light-primary text-white hover:bg-pink-600 hover:shadow-md' // premium non-danger
  };

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};

export default PremiumButton;
```

### 5. Update Global Styles
Modify `globals.css` to include new typography and base styles:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  font-family: 'Inter', system-ui, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  /* Base colors managed by theme */
  --text-color: var(--text-primary);
  --bg-color: var(--bg-primary);
}

body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s ease, color 0.3s ease;
}

/* Smooth transitions for interactive elements */
button, a {
  transition: all 0.2s ease-in-out;
}
```

### 6. Apply to All Pages
Ensure all existing pages/components are wrapped with the theme provider and implement the new styling patterns.

## Testing Checklist
- [ ] All pages display correctly in both themes
- [ ] Delete buttons have distinct danger hover styling
- [ ] Edit/Task buttons have premium non-danger hover styling
- [ ] Typography is updated across all components
- [ ] No unauthorized colors are used (verify color constraint compliance)
- [ ] Transitions and animations are smooth
- [ ] Responsive design maintained across breakpoints
- [ ] No JavaScript/TypeScript logic changed