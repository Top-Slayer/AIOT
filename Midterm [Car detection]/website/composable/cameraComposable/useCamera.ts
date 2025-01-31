import { ref } from "vue";
import { sendCameraData, changeBarrierStatus } from "~/service/UseCamera/cameraService";

export const useCamera = () => {
  const cameraStream = ref<MediaStream | null>(null);
  const cameraImage = ref<Array<Blob>>([]);
  const isLoading = ref(false);
  const errorMessage = ref<string | null>(null);
  const servoStatus = ref<boolean>(false);

  // function open camera
  const startCamera = async () => {
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
      document.body.appendChild(video);

      // Open Servo
      await changeBarrierStatus();
      servoStatus.value = true;

      takePhoto();

      setTimeout(async () => {
        if (cameraImage.value.length > 0) {
          await sendCameraData(cameraImage.value);
          cameraImage.value = [];
        }
      }, 1000);


    } catch (error) {
      errorMessage.value = (error as Error).message;
    } finally {
      isLoading.value = false;
    }
  };

  // function stop camera
  const stopCamera = async () => {
    if (cameraStream.value) {
      cameraStream.value.getTracks().forEach((track) => track.stop);
      cameraStream.value = null;
    }

    const video = document.querySelector("video");
    if (video) {
      video.remove();
    }
    try {
      await changeBarrierStatus();
      servoStatus.value = false;

    } catch (error) {
      errorMessage.value = (error as Error).message;
    }
  };

  // function post status sevo 
  const changeStatusServo = async () => {
    try {
      await changeBarrierStatus();
      servoStatus.value != servoStatus.value;
    }
    catch (error) {
      errorMessage.value = (error as Error).message;
    }
  }

  // function take photo
  const takePhoto = () => {
    if (cameraStream.value) {
      const video = document.querySelector("video") as HTMLVideoElement;
      const canvas = document.createElement("canvas");

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      const ctx = canvas.getContext("2d");
      ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob((blob) => {
        if (blob) {
          cameraImage.value.push(blob);
        }
      }, "image/jpeg");
    }
  };

  return {
    cameraImage,
    isLoading,
    errorMessage,
    startCamera,
    stopCamera,
    changeStatusServo,
    servoStatus
  };
};

// ມາເຮັດຕໍ່ໃນພາກສ່ວນຂອງກ້ອງ, ການຄວບຄຸມ servo ແລະ ການດຶງຂໍ້ມູນມາສະແດງໃນ Tables


