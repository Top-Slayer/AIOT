import type { carType } from "~/types/carTable/carType";
const API_Car = "http://localhost:5000/getAllDatas";

// function fetch Data car 
export const fetchDataCar = async (): Promise<carType[]> => {
    try{
        const response = await fetch(API_Car);

        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: carType[] = await response.json();
        return data;
    }
    catch(error){
        console.error("Message error fetch API_car");
        throw new Error("Failed to fetch car data");
    };
};
