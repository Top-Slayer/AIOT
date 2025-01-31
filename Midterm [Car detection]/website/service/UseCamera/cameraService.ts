export const sendCameraData = async (cameraImage:Array<Blob>) => {
    try {
      const formData = new FormData();
      console.log("Form data: ", formData);

        cameraImage.forEach((blob, index) => {
            formData.append("image" + index, blob);
        });

    const response = await fetch(`http://localhost:5000/analyse-img`,{
      method: "POST",
      body: JSON.stringify(formData),
    });
    return response;
  } catch (errormessage) {
    throw new Error("Failed to add image!!!");
  }
};

//  function change Barrier Status
export const changeBarrierStatus = async () => {
  try {
    const response = await fetch(`http://localhost:5000/change-status`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    return response;
   
  } catch (error) {
    throw new Error("Failed to change barrier status");
  }
};
