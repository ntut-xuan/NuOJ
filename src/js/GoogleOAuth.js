function init() {
    gapi.load('auth2', function () {
        auth2 = gapi.auth2.init({
            client_id: "434328667842-4pqp3g8snef36jvf41g0ciu58rtek555.apps.googleusercontent.com",
            cookiepolicy: 'single_host_origin'
        });
        attachSignin(document.getElementById('viaGoogle'));
    });
}

init();