/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Inclut tous les fichiers dans le dossier src
  ],
  theme: {
    extend: {
      colors:{
        primary: "#1a73e8", // Royal blue
        secondary: "#f4b400", // Deep gold
        surface: "#1e1e1e", // Dark surface
        background: "#121212", // Very dark gray
        error: "#d93025", // Crimson
        "on-surface": "#e8eaed",
      }
    },
  },
  plugins: [],
};
