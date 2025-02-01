// Convert Blob to Base64
export const convertBlobToBase64 = (blob: Blob): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(blob);
    reader.onloadend = () => {
      const base64String = reader.result?.toString().split(",")[1]; // ตัด "data:image/png;base64," ออก
      resolve(base64String || "");
    };
    reader.onerror = (error) => reject(error);
  });
};

// Send image data to API
export const sendCameraData = async (cameraImage: Blob[]) => {
  try {
    // Convert all images to Base64
    const base64Images = await Promise.all(
      cameraImage.map((blob) => convertBlobToBase64(blob))
    );

    // Send the first image (API รับเพียง 1 รูป)
    const response = await fetch("http://localhost:5000/analyse-img", {
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
    throw new Error("Failed to add image!!!");
  }
};

// Change barrier status
export const changeBarrierStatus = async () => {
  try {
    const response = await fetch("http://localhost:5000/change-status", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    return response;
  } catch (error) {
    throw new Error("Failed to change barrier status");
  }
};
