<script setup lang="ts">
import { useCamera } from '~/composable/cameraComposable/useCamera';
import { ref, onMounted } from 'vue';

const {
  isLoading,
  errorMessage,
  servoStatus,
  startCamera,
  stopCamera,
  changeStatusServo,
} = useCamera();

// video stream
const video = ref<HTMLVideoElement | null>(null);

onMounted(() => {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      if (video.value) video.value.srcObject = stream;
    })
    .catch((err) => console.error("Error accessing camera:", err));
});

</script>

<template>
  <div class="mx-auto">
    <h1 class="mt-10 font-bold text-2xl text-gray-900 text-center">Camera-contor</h1>

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
      <button @click="changeStatusServo" class="px-2 py-2 border-4 rounded-lg font-bold text-white"
        :class="servoStatus ? 'border-green-600 bg-green-500' : 'border-blue-900 bg-blue-800'">
        {{ servoStatus ? "OPEN" : "CLOSE" }}
      </button>
    </div>

    <!-- <div>
      <video ref="video" autoplay></video>
    </div> -->
  </div>
</template>

<style scoped></style>


<!-- ມາເຮັດຕໍ່ໃນສ່ວນຂອງຕາຕະລາງ -->