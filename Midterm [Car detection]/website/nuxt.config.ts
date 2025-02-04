export default defineNuxtConfig({
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  compatibilityDate: '2025-02-01',
  ssr: true,
  nitro:{
    preset: 'static'
  }
});




// modules: [
//   '@nuxtjs/tailwindcss'
// ],
// compatibilityDate: '2025-01-20',