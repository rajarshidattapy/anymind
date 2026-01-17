/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      fontWeight: {
        'normal': '700',
        'bold': '700',
        'semibold': '700',
        'medium': '700',
      },
      letterSpacing: {
        'tight': '-0.02em',
        'normal': '-0.02em',
      },
      colors: {
        // Mantle-inspired color palette
        mantle: {
          50: '#f0fdfa',   // Very light teal
          100: '#ccfbf1',  // Light teal
          200: '#99f6e4',  // Soft teal
          300: '#5eead4',  // Medium teal
          400: '#2dd4bf',  // Teal accent
          500: '#14b8a6',  // Primary teal
          600: '#0d9488',  // Darker teal
          700: '#0f766e',  // Deep teal
          800: '#115e59',  // Very deep teal
          900: '#134e4a',  // Darkest teal
        },
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',
        },
        accent: {
          50: '#ecfdf5',   // Light green
          100: '#d1fae5',  // Soft green
          200: '#a7f3d0',  // Medium green
          300: '#6ee7b7',  // Bright green
          400: '#34d399',  // Green accent
          500: '#10b981',  // Primary green
          600: '#059669',  // Darker green
          700: '#047857',  // Deep green
          800: '#065f46',  // Very deep green
          900: '#064e3b',  // Darkest green
        }
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      boxShadow: {
        'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        'soft-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      transitionDuration: {
        '250': '250ms',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
};
