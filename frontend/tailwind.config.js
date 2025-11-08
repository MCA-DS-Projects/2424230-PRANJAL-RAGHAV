module.exports = {
  content: [
    "./pages/*.{html,js}",
    "./index.html",
    "./src/**/*.{html,js,jsx,ts,tsx}",
    "./components/**/*.{html,js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Primary Colors
        primary: {
          DEFAULT: "#2D5A27", // deep-forest-green
          50: "#F0F7EF", // light-forest-green-50
          100: "#D9EDD6", // light-forest-green-100
          200: "#B8DDB2", // light-forest-green-200
          300: "#8FC885", // light-forest-green-300
          400: "#6BB05F", // light-forest-green-400
          500: "#4A8B3F", // forest-green-500
          600: "#3A6B31", // forest-green-600
          700: "#2D5A27", // deep-forest-green
          800: "#234520", // dark-forest-green-800
          900: "#1A3318", // dark-forest-green-900
        },
        // Secondary Colors
        secondary: {
          DEFAULT: "#8B4513", // earth-brown
          50: "#F7F1ED", // light-earth-brown-50
          100: "#EEDDD0", // light-earth-brown-100
          200: "#DCC4A8", // light-earth-brown-200
          300: "#C8A47D", // light-earth-brown-300
          400: "#B08456", // light-earth-brown-400
          500: "#9A6B3A", // earth-brown-500
          600: "#8B4513", // earth-brown
          700: "#6F3710", // dark-earth-brown-700
          800: "#552B0D", // dark-earth-brown-800
          900: "#3D1F09", // dark-earth-brown-900
        },
        // Accent Colors
        accent: {
          DEFAULT: "#E6A85C", // golden-amber
          50: "#FDF8F2", // light-golden-amber-50
          100: "#FAEED9", // light-golden-amber-100
          200: "#F4DCB3", // light-golden-amber-200
          300: "#EDC488", // light-golden-amber-300
          400: "#E6A85C", // golden-amber
          500: "#D9954A", // golden-amber-500
          600: "#C0803A", // golden-amber-600
          700: "#A06B2D", // golden-amber-700
          800: "#7F5622", // golden-amber-800
          900: "#5F4119", // golden-amber-900
        },
        // Background Colors
        background: "#FDFCF8", // warm-off-white
        surface: "#F7F5F0", // subtle-cream
        // Text Colors
        text: {
          primary: "#2C2C2C", // rich-charcoal
          secondary: "#6B6B6B", // medium-gray
        },
        // Status Colors
        success: {
          DEFAULT: "#4A7C59", // natural-green
          50: "#F1F7F3", // light-natural-green-50
          100: "#DDEEE2", // light-natural-green-100
          200: "#B8DCC5", // light-natural-green-200
          300: "#8FC8A1", // light-natural-green-300
          400: "#6BA27D", // light-natural-green-400
          500: "#4A7C59", // natural-green
          600: "#3D6548", // natural-green-600
          700: "#314E39", // natural-green-700
          800: "#253A2B", // natural-green-800
          900: "#1A281E", // natural-green-900
        },
        warning: {
          DEFAULT: "#D4A574", // muted-gold
          50: "#FBF7F2", // light-muted-gold-50
          100: "#F5EBDD", // light-muted-gold-100
          200: "#EDD7BB", // light-muted-gold-200
          300: "#E3C199", // light-muted-gold-300
          400: "#D4A574", // muted-gold
          500: "#C59660", // muted-gold-500
          600: "#B0844F", // muted-gold-600
          700: "#8F6B40", // muted-gold-700
          800: "#6E5231", // muted-gold-800
          900: "#4D3A23", // muted-gold-900
        },
        error: {
          DEFAULT: "#A0522D", // earthy-red-brown
          50: "#F6F1ED", // light-earthy-red-brown-50
          100: "#EBDDD2", // light-earthy-red-brown-100
          200: "#D7BBA5", // light-earthy-red-brown-200
          300: "#C19978", // light-earthy-red-brown-300
          400: "#AB774B", // light-earthy-red-brown-400
          500: "#A0522D", // earthy-red-brown
          600: "#8A4526", // earthy-red-brown-600
          700: "#73381F", // earthy-red-brown-700
          800: "#5C2B18", // earthy-red-brown-800
          900: "#451F11", // earthy-red-brown-900
        },
      },
      fontFamily: {
        // Headings
        inter: ['Inter', 'sans-serif'],
        // Body text
        'source-sans': ['Source Sans Pro', 'sans-serif'],
        // Captions
        'nunito-sans': ['Nunito Sans', 'sans-serif'],
        // Data/monospace
        'jetbrains-mono': ['JetBrains Mono', 'monospace'],
        // Default sans
        sans: ['Source Sans Pro', 'Inter', 'sans-serif'],
      },
      fontSize: {
        'fluid-sm': 'clamp(0.875rem, 0.8rem + 0.375vw, 1rem)',
        'fluid-base': 'clamp(1rem, 0.9rem + 0.5vw, 1.125rem)',
        'fluid-lg': 'clamp(1.125rem, 1rem + 0.625vw, 1.25rem)',
        'fluid-xl': 'clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)',
        'fluid-2xl': 'clamp(1.5rem, 1.3rem + 1vw, 2rem)',
        'fluid-3xl': 'clamp(1.875rem, 1.6rem + 1.375vw, 2.5rem)',
      },
      borderRadius: {
        'component': '8px',
        'card': '12px',
      },
      boxShadow: {
        'soft': '0 2px 8px rgba(45, 90, 39, 0.08), 0 1px 3px rgba(45, 90, 39, 0.12)',
        'medium': '0 4px 12px rgba(45, 90, 39, 0.08), 0 2px 6px rgba(45, 90, 39, 0.12)',
        'strong': '0 8px 24px rgba(45, 90, 39, 0.08), 0 4px 12px rgba(45, 90, 39, 0.16)',
      },
      animation: {
        'fade-in': 'fadeIn 300ms ease-in-out',
        'slide-up': 'slideUp 500ms ease-out',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
        '300': '300ms',
        '500': '500ms',
      },
      transitionTimingFunction: {
        'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      minHeight: {
        'touch': '44px',
      },
      minWidth: {
        'touch': '44px',
      },
    },
  },
  plugins: [],
}