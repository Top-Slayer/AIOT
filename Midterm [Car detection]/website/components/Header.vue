<script setup lang="ts">
import { NuxtLink } from '#components';
</script>

<template>
    <div class="mt-16">
        <ul class="mx-auto mr-16 flex space-x-2 justify-end">
            <NuxtLink to="/">
                <li class="font-bold text-lg px-2 text-gray-900">Camera</li>
            </NuxtLink>

            <NuxtLink to="/camera/cameraView">
                <li class="font-bold text-lg px-2 text-gray-900">Tables</li>
            </NuxtLink>
        </ul>
    </div>

</template>

<style scoped>

</style>