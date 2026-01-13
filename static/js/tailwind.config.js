/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*/templates/**/*.html',
    './static/src/**/*.js',  // si tienes JS con clases tailwind
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
