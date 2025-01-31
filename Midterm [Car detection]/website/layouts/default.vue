<script setup lang="ts">
import Header from '~/components/Header.vue';
import Footer from '~/components/Footer.vue';
</script>

<template>
    <div class="mx-5">

        <h1 class="mt-10 text-center font-bold text-blue-900 text-2xl">CAR DETECTION</h1>

        <header>
            <Header />
        </header>

        <NuxtPage />

        <footer>
            <Footer />
        </footer>
    </div>
</template>

<style scoped>

</style>