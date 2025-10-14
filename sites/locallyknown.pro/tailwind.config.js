module.exports = {
  content: [
    './_layouts/**/*.html',
    './_includes/**/*.html',
    './_posts/**/*.md',
    './*.md',
    './*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        'kalam': ['Kalam', 'cursive'],
      },
      colors: {
        'orange': {
          600: '#ea580c',
        },
        'red': {
          600: '#dc2626',
        },
      },
    },
  },
  plugins: [],
}