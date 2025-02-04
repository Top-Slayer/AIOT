import { ref, watchEffect } from "vue";
import { sendCameraData} from "~/service/UseCamera/cameraService";
import './style.css'

export const useCamera = () => {
  const cameraStream = ref<MediaStream | null>(null);
  const cameraImage = ref<Blob[]>([]);
  const isLoading = ref(false);
  const errorMessage = ref<string | null>(null);

  console.log("Camera start: ", cameraImage);

  // function open camera
  const startCamera = async () => {
    console.log("Start camera");
    
    try {
      isLoading.value = true;
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });
      cameraStream.value = stream;

      // create a new video
      const video = document.createElement("video");
      video.srcObject = stream;
      video.play();
      video.classList.add("camera-video");
      document.body.appendChild(video);
      
      const photInterval = setInterval(async() =>{
        await takePhoto();
      }, 3000);
      
      (window as any).photInterval = photInterval;
    } catch (error) {
      errorMessage.value = (error as Error).message;
    } finally {
      isLoading.value = false;
    }
  };

  // function stop camera
  const stopCamera = async () => {
    console.log("Stop camera");
    
    if (cameraStream.value) {
      cameraStream.value.getTracks().forEach((track) => track.stop);
      cameraStream.value = null;
    }

    const video = document.querySelector("video");
    if (video) {
      video.remove();
    }

    clearInterval((window as any).photInterval);
  };

  // function take photo
  const takePhoto = async () => {
    if (cameraStream.value) {
      const video = document.querySelector("video") as HTMLVideoElement;
      const canvas = document.createElement("canvas");

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(async (blob) => {
        if (blob) {
          cameraImage.value = [...cameraImage.value, blob];
          await sendCameraData([blob]);
        }
      }, "image/jpeg");
    }
  };

  watchEffect(() => {
    console.log("New Image Captured:", cameraImage.value);
  });
  return {
    cameraImage,
    isLoading,
    errorMessage,
    startCamera,
    stopCamera,
  };
};
