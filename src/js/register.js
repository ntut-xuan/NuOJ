function account(){
    let username = document.getElementsByTagName("input")[0].value
    let email = document.getElementsByTagName("input")[1].value
    let password = document.getElementsByTagName("input")[2].value
    
    const shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
    shaObj.update(password)
    dataJson = {}
    dataJson["handle"] = username
    dataJson["email"] = email
    dataJson["password"] = shaObj.getHash("HEX")
    dataJson["check"] = true
    $.ajax({
        url: "./register",
        type: "POST",
        data: JSON.stringify(dataJson),
        dataType: "json",
        contentType: "application/json",
        success(data, status, xhr){
            if(data["status"] == "OK"){
                success_dialog("註冊成功！", "", "")
            }else{
                Swal.fire({
                    icon: "error",
                    title: "註冊失敗",
                    text: getMessageFromCode(data["code"]),
                    timer: 1500,
                    showConfirmButton: false
                })
            }
        }
    })
}
document.addEventListener('keyup', (e) => {
    if(e.code=="Enter" || e.code =="NumpadEnter"){
        account()
    }
});