document.getElementById("logout").addEventListener("click", function () {
    $.ajax({
        url: "/logout",
        type: "POST",
        success: function success(data, status, xhr) {
            Swal.fire({
                icon: 'success',
                title: '已登出',
                timer: 1500,
                showConfirmButton: false
            }).then(function () {
                window.location.href = "/";
            });
        }
    });
});

var state = 0;
var profileRunning,
    problemRunning = false;
function getElement(id) {
    return document.getElementById(id);
}

function allHidden() {
    var array = ["change_interface", "cover", "chose", "change_img"];
    for (var i = 0; i < array.length; i++) {
        var div = document.getElementById(array[i]);
        div.classList.add("hidden");
    }
    document.getElementById("input_file").value = "";
}

function init() {
    getElement("name_change").addEventListener("click", function () {
        old = document.getElementById("username").innerText;
        show_interface(old, "編輯使用者名稱", "請輸入新使用者名稱與密碼", "使用者名稱");
    });

    getElement("email_change").addEventListener("click", function () {
        old = document.getElementById("email").innerText;
        show_interface(old, "編輯電子郵件", "請輸入新電子郵件與密碼", "電子郵件");
    });

    getElement("school_change").addEventListener("click", function () {
        old = document.getElementById("school").innerText;
        show_interface(old, "編輯所屬學校", "請輸入新所屬學校與密碼", "所屬學校");
    });

    getElement("introduce_change").addEventListener("click", function () {
        old = document.getElementById("introduce").innerText;
        show_interface(old, "編輯個人簡介", "請輸入新個人簡介與密碼", "個人簡介");
    });

    getElement("main_change").addEventListener("click", function () {
        allHidden();
        document.getElementById("chose").classList.remove("hidden");
        document.getElementById("cover").classList.remove("hidden");
    });

    getElement("cover").addEventListener("click", function () {
        allHidden();
    });

    getElement("input_file").addEventListener("change", function (e) {
        var file = document.getElementById("input_file").files[0];
        var fr = new FileReader();
        fr.onload = function (e) {
            document.getElementById("img_show").setAttribute("src", e.target.result);
        };
        fr.readAsDataURL(file);
        allHidden();
        document.getElementById("change_img").classList.remove("hidden");
        document.getElementById("cover").classList.remove("hidden");
    });

    var pro = getElement("profile");
    pro.addEventListener("animationiteration", function () {
        pro.classList.remove("animationStart");
        pro.classList.add("animationStop");
        profileRunning = false;
    });

    var problem = getElement("problem");
    problem.addEventListener("animationiteration", function () {
        problem.classList.remove("animationStart");
        problem.classList.add("animationStop");
        problemRunning = false;
    });
}

function show_interface(old, main_title, subtitle, indecate) {
    document.getElementById("change_main_title").innerText = main_title;
    document.getElementById("change_subtitle").innerText = subtitle;
    document.getElementById("input_indecate").innerText = indecate;
    document.getElementById("new").value = old;
    document.getElementById("change_interface").classList.remove("hidden");
    document.getElementById("cover").classList.remove("hidden");
}

function contentchange(c) {
    if (profileRunning || problemRunning) return;
    if (state != c) {
        getElement("profile").classList.remove("animationStop");
        getElement("problem").classList.remove("animationStop");
        getElement("profile").classList.add("animationStart");
        getElement("problem").classList.add("animationStart");
        if (c == 1) {
            getElement("first_choice").className = "unselect";
            getElement("second_choice").className = "select";
        } else {
            getElement("first_choice").className = "select";
            getElement("second_choice").className = "unselect";
        }
        state = c;
        profileRunning = true;
        problemRunning = true;
    }
}

init();