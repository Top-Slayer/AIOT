<script setup lang="ts">
import { useCamera } from '~/composable/cameraComposable/useCamera';

const {
  isLoading,
  errorMessage,
  startCamera,
  stopCamera,
  cameraImage
} = useCamera();

</script>

<template>
  <div class="mx-auto">
    <h1 class="mt-8 font-bold text-lg text-gray-900 text-center">Camera-Control</h1>

    <div v-if="isLoading">Loading camera...</div>

    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-if="!isLoading && !errorMessage" class="mt-10 flex space-x-3 justify-center">

      <!-- button start -->
      <button @click="startCamera"
        class="px-2 py-3 border-4 border-blue-600 bg-blue-500 rounded-lg font-bold  text-white">Start Camera</button>

      <!-- Button stop camera -->
      <button @click="stopCamera"
        class="px-2 py-3 border-4 border-rose-600 bg-rose-500 rounded-lg font-bold text-white ">Stop camera</button>

      <!-- button status -->
      <button v-for="status  in cameraImage">
        
      </button>
     
    </div>
  </div>
</template>

<style scoped></style>


