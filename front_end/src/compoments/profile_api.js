export const getUserInfo = async (handle, setter) => {
  let res = await fetch(`/api/profile/${handle}`, {
    method: "GET",
  });
  if (res.ok) {
    let json = await res.json();
    setter(json);
  }
};

export const getImgSrc = async (handle, setter) => {
  let res = await fetch(`/api/profile/${handle}/avatar`, {
    method: "GET",
  });
  if (res.ok) {
    let blob = await res.blob();
    let reader = new FileReader();
    reader.onloadend = function () {
      let base64data = reader.result;
      setter(base64data);
    };
    reader.readAsDataURL(blob);
  }
};
