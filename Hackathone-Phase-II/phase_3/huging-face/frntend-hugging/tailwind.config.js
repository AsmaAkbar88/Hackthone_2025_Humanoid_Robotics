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
    },
  },
  plugins: [],
}