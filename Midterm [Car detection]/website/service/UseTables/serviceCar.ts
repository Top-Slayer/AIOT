import type { carType } from "~/types/carTable/carType";
import { useFetch } from "#app";
const API_Car = "http://localhost:5000/getAllDatas";
// const API_Car = "http://localhost:5000/getAllDatas?limit=10&offset=0";

// function fetch Data car 
export const fetchDataCar = async (): Promise<carType[]> => {
    const { data, error } = await useFetch(`${API_Car}`);

    if (error.value) {
        throw new Error(error.value.message);
    }
    if (data && data.value) {
        return data.value as carType[];
    }
    else {
        throw new Error("Invalid API Response key");
    }
}
