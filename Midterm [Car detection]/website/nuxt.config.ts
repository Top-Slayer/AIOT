export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  compatibilityDate: '2025-02-01',
  ssr: false,
  target: 'static',
  nitro:{
    preset: 'static'
  },
});




// modules: [
//   '@nuxtjs/tailwindcss'
// ],
// compatibilityDate: '2025-01-20',