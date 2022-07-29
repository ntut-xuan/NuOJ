function account(){
    let account = document.getElementsByTagName("input")[0].value
    let password = document.getElementsByTagName("input")[1].value
    let dataJson = {}
    const shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
    shaObj.update(password)
    dataJson["account"] = account
    dataJson["password"] = shaObj.getHash("HEX")
    $.ajax({
        url: "./login",
        type: "POST",
        data: JSON.stringify(dataJson),
        dataType: "json",
        contentType: "application/json",
        success(data, status, xhr){
            if(data["status"] == "OK"){
                Swal.fire({
                    icon: "success",
                    title: "登入成功",
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    window.location.href = "/"
                })
            }else{
                if(data["code"] === 304){
                    window.location.href = "/mail_check"
                }else{
                    Swal.fire({
                        icon: "error",
                        title: "登入失敗",
                        text: getMessageFromCode(data["code"]),
                        timer: 1500,
                        showConfirmButton: false
                    })
                }
            }
        }
    })
}

document.addEventListener('keyup', (e) => {
    if(e.code=="Enter" || e.code =="NumpadEnter"){
        account()
    }
});