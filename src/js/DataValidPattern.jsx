function HandleValidNotice(prop){
    let invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500 ease-in-out"
    let valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500 ease-in-out"
    let handle = prop.handle;
    let regex_pattern = '[a-zA-Z\\d](?:[a-zA-Z\\d]|[_-](?=[a-zA-Z\\d])){3,38}$'
    let re = new RegExp(regex_pattern)
    let matches = handle.match(re)
    let test = ((matches && matches[0].length == handle.length) || (handle.length == 0))
    let render = (
        <div id="account_valid_notice" className={test ? valid_classname : invalid_classname}>
            <p> Handle 不合法 </p>
            <p> ．Handle 僅能使用大小寫英文、數字與特殊符號（底線與連接號）　</p>
            <p> ．最長長度 39 個字，最短長度 4 個字。 </p>
            <p> ．特殊符號不能當做 handle 字首或字尾，特殊符號不能連續。 </p>
        </div>
    )
    return render;
}

function EmailValidNotice(prop){
    let invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500 ease-in-out"
    let valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500 ease-in-out"
    let email = prop.email;
    let regex_pattern = "^\\w+([\\.-]?\\w+)*@\\w+([\\.-]?\\w+)*(\\.\\w{2,3})+$"
    let re = new RegExp(regex_pattern)
    let matches = email.match(re)
    let test = ((matches && matches[0].length == email.length) || (email.length == 0))
    let render = (
        <div id="account_valid_notice" className={test ? valid_classname : invalid_classname}>
            <p> 信箱不合法 </p>
        </div>
    )
    return render;
}

function PasswordValidNotice(prop){
    let invalid_classname = "w-full h-fit rounded-lg p-2 px-5 bg-red-500 text-white transition-all duration-500";
    let valid_classname = "w-full rounded-lg bg-red-500 text-white h-0 overflow-y-hidden transition-all duration-500"
    let password = prop.password;
    let regex_pattern = "(?=.*?[a-zA-Z])(?=.*?[0-9]).{8,32}$"
    let re = new RegExp(regex_pattern)
    let matches = password.match(re)
    let test = ((matches && matches[0].length == password.length) || (password.length == 0))
    let render = (
        <div id="password_valid_notice" className={test ? valid_classname : invalid_classname}>
            <p> 密碼不合法 </p>
            <p> ．密碼需要長達 8 個字，最多 32 個字 </p>
            <p> ．密碼需要包含至少一個英文字母 </p>
        </div>
    )
    return render;
}