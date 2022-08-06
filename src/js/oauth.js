if(document.getElementById("viaAccount") != undefined){
    document.getElementById("viaAccount").addEventListener("click", () => {
        Account()
    })
}
if(document.getElementById("viaGithub") != undefined){
    document.getElementById("viaGithub").addEventListener("click", () => {
        window.location.href = "https://github.com/login/oauth/authorize?client_id=a00b6ba16a262302ed3b&scope=repo";
    })
}
if(document.getElementById("viaGoogle") != undefined){
    document.getElementById("viaGoogle").addEventListener("click", () => {
        let client_id = "{{google_client_id}}"
        let redirect_url = "{{google_redirect_url}}"
        let response_type = "code"
        let scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        window.location.href = "https://accounts.google.com/o/oauth2/v2/auth?client_id=" + client_id + "&redirect_uri=" + redirect_url + "&response_type=" + response_type + "&scope=" + scope;
    })
}