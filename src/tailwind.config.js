/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./home/templates/**/**.html",
    "./hanusovedni/templates/**/**.html"
  ],
  theme: {
    extend: {
      colors: {
        "raspberry": {
          DEFAULT: "#852049",
          500: "#9f2657",
          700: "#6c1a3b"
        },
        "bhd-orange": {
          DEFAULT: "#e2902e",
          600: "#c88029",
        }
      }
    },
  },
  plugins: [],
}
