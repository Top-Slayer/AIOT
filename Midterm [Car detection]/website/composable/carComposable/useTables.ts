import { fetchDataCar } from "~/service/UseTables/serviceCar";
import type { carType } from "~/types/carTable/carType";
import { ref , watchEffect} from "vue";

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
  
      // Effect Data
  watchEffect(() =>{
    if(data.value){
      infoCar.value = data.value;
    }
    isLoading.value = pending.value;
    errorMessage.value = error.value?.message || null;
  })      

  return {
    infoCar,
    isLoading,
    errorMessage,
  };
};
export default carService;

