module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: '#0a0e27',
        glow: '#0ff0ff',
      },
      boxShadow: {
        glow: '0 0 20px rgba(0, 255, 255, 0.3)',
      },
    },
  },
  plugins: [],
}
