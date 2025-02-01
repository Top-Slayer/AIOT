const API_Camera = "http://localhost:5000/analyse-img";

// Convert Blob to Base64
export const convertBlobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = () => {
      const base64String = reader.result?.toString().split(",")[1]; 
      resolve(base64String || "");
    };
    reader.onerror = (error) => reject(error);
  });
};

// Send image data to API
export const sendCameraData = async (cameraImage: Blob[]) => {
  console.log("Send camera");
  
  try {
    const base64Images = await Promise.all(
      cameraImage.map((blob) => convertBlobToBase64(blob))
    );

    console.log("Base 64", base64Images);
    
    // Send the first image 
    const response = await fetch(`${API_Camera}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: base64Images[0] }), 
      
    });

    const responseData = await response.json();
    console.log("Response Data: ", responseData);
    return responseData;

  } catch (error) {
    console.error("Message error Image: ", error);
    throw new Error("Failed to add image!!!");
  }
};

