import { fetchDataCar } from "~/service/UseTables/serviceCar";
import type { carType } from "~/types/carTable/carType";
import { ref } from "vue";

const carService = () => {
  const infoCar = ref<carType[]>([]);
  const isLoading = ref<boolean>(false);
  const errorMessage = ref<string | null>(null);

  // function fetch APT SSR
  const { data, pending, error } = useAsyncData<carType[]>(
    "carData",
    async () => {
      return await fetchDataCar();
    }
  );
  if (data.value) {
    infoCar.value = data.value;
  }
  if (pending.value) {
    isLoading.value = pending.value;
  }
  if (error.value) {
    errorMessage.value = error.value.message;
  }

  return {
    infoCar,
    isLoading,
    errorMessage,
  };
};
export default carService;

