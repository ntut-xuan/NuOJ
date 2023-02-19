const ERROR_CODE = Object.freeze({
    "HANDLE_INVALID": {"code": 201, "message": "Handle 不合法"},
    "HANDLE_NOT_FOUND": {"code": 202, "message": "Handle 不存在"},
    "HANDLE_EXIST": {"code": 203, "message": "Handle 已存在"},
    "HANDLE_REPEAT": {"code": 204, "message": "Handle 已重複"},
    "EMAIL_INVALID": {"code": 302, "message": "信箱不合法"},
    "EMAIL_NOT_FOUND": {"code": 303, "message": "信箱不存在"},
    "EMAIL_NOT_VERIFICATION": {"code": 304, "message": "信箱未驗證"},
    "EMAIL_VERIFICATION_FAILED": {"code": 305, "message": "信箱驗證失敗"},
    "EMAIL_EXIST": {"code": 306, "message": "信箱已存在"},
    "PASSWORD_NOT_MATCH": {"code": 401, "message": "密碼不符合"},
    "PASSWORD_INVALID": {"code": 402, "message": "密碼不符合規定"},
    "REQUIRE_PAPRMETER": {"code": 501, "message": "缺少參數"},
    "REQUIRE_AUTHORIZATION": {"code": 502, "message": "需要驗證"},
    "INVALID_DATA": {"code": 601, "message": "資料無效"},
    "ACCOUNT_INVALID": {"code": 701, "message": "Handle 或信箱無效"},
    "UNEXCEPT_ERROR": {"code": 999, "message": "未預期的錯誤發生"},
})

function getMessageFromCode(code){
    let keys = Object.keys(ERROR_CODE)
    for(let i = 0; i < keys.length; i++){
        let key = keys[i];
        if(ERROR_CODE[key]["code"] === code){
            return ERROR_CODE[key]["message"]
        }
    }
}

function success_swal(title){
    return Swal.fire({
        icon: "success",
        title: title,
        timer: 1500,
        showConfirmButton: false
    })
}

function error_swal(title, text){
    Swal.fire({
        icon: "error",
        title: title,
        text: text,
        timer: 1500,
        showConfirmButton: false
    })
}