/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // New premium color palette for 2026 ultra-modern style
        'peachpuff': '#FFDAB9',
        'turquoise': '#40E0D0',
        'near-black': '#1A1A1A',
        'soft-white': '#F8F8F8',
        // Extended color scales
        'premium': {
          50: '#FFFAF7',
          100: '#FFF5EE',
          200: '#FFECE4',
          300: '#FFE4DB',
          400: '#FFD7C9',
          500: '#FFDAB9',
          600: '#FCCCB6',
          700: '#F9BB9E',
          800: '#F6A880',
          900: '#F39260',
        },
        'turquoise': {
          50: '#F0FDFC',
          100: '#E0FBF9',
          200: '#C8F7F4',
          300: '#A0F0EC',
          400: '#67E3DE',
          500: '#40E0D0',
          600: '#34C2B2',
          700: '#2B9D91',
          800: '#257C74',
          900: '#20635D',
        },
        'near-black': {
          DEFAULT: '#1A1A1A',
          50: '#E6E6E6',
          100: '#CCCCCC',
          200: '#B3B3B3',
          300: '#999999',
          400: '#808080',
          500: '#666666',
          600: '#4D4D4D',
          700: '#333333',
          800: '#1A1A1A',
          900: '#0D0D0D',
        },
        // Glassmorphism and background colors
        'glass': {
          primary: 'rgba(255, 255, 255, 0.85)',
          secondary: 'rgba(255, 253, 253, 0.65)',
          input: 'rgba(255, 250, 248, 0.9)',
        },
        // Dark theme: updated to near-black
        dark: {
          primary: '#1A1A1A',
          secondary: '#FFFFFF',
          background: '#F8F8F8',
          text: '#1A1A1A',
        },
        // Light theme: updated to premium palette
        light: {
          primary: '#40E0D0', // turquoise
          secondary: '#FFDAB9', // peachpuff
          background: '#F8F8F8',
          text: '#1A1A1A', // near-black text
        }
      },
      borderRadius: {
        'xl': '16px',
        '2xl': '20px',
      },
      boxShadow: {
        'glass': 'rgba(255, 77, 155, 0.15) 0px 8px 36px 0px, rgba(47, 96, 97, 0.1) 0px 6.08815px 20.6997px 0px, rgba(79, 143, 145, 0.08) 0px 3.40662px 11.5825px 0px, rgba(92, 126, 127, 0.05) 0px 1.71482px 5.83078px 0px',
        'premium': '0 8px 32px rgba(0, 0, 0, 0.1)',
      },
      backdropBlur: {
        'xs': '4px',
      },
      fontFamily: {
        'display': ['system-ui', 'sans-serif'],
        'body': ['system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}