document.getElementById("logout").addEventListener("click", () => {
    $.ajax({
        url: "/logout",
        type: "POST",
        success(data, status, xhr){
            Swal.fire({
                icon: 'success',
                title: '已登出',
                timer: 1500,
                showConfirmButton: false,
            }).then(() => {
                window.location.href = "/"
            })
        }
    });
})

var state = 0;
var profileRunning,problemRunning = false
var problemCount = 0


async function getProblem(index){
    data=""
    state = ""
    await fetch('/problem_list/'+index).then(function(response){
        state = response.status    
        return response.text()
    }).then(function(text){
        data = text
    })

    if(state == 400){
        document.location.href="/";
    }
    // console.log(state)
    return data
}

async function getProblemSetting(){
    fetch("/problem_list_setting").then(function(response){
        if(response.status == 400){
            document.location.href="/";
        }
        else{
            return response.json()
        }
    }).then(function(res){
        console.log(res)
    })
}

function getElement(id){
    return document.getElementById(id)
}    

function allHidden(){
    let array = ["change_interface", "cover","chose","change_img"]
    for(let i = 0; i < array.length; i++){
        let div = document.getElementById(array[i]);
        div.classList.add("hidden");
    }
    document.getElementById("input_file").value=""
}

async function init(){
    getElement("name_change").addEventListener("click", () => { show_interface(0) })

    getElement("email_change").addEventListener("click", () => { show_interface(1)})

    getElement("school_change").addEventListener("click", () => { show_interface(2)})

    getElement("introduce_change").addEventListener("click", () => { show_interface(3)})

    getElement("main_change").addEventListener("click", () => {
        allHidden()
        document.getElementById("chose").classList.remove("hidden")
        document.getElementById("cover").classList.remove("hidden")
    })

    getElement("cover").addEventListener("click", () => {
        allHidden()
    })

    getElement("input_file").addEventListener("change", function(e){
        const file = document.getElementById("input_file").files[0];
        const fr = new FileReader();
        fr.onload = function (e) {
            document.getElementById("img_show").setAttribute("src",e.target.result)
        };
        fr.readAsDataURL(file);
        allHidden()
        document.getElementById("change_img").classList.remove("hidden")
        document.getElementById("cover").classList.remove("hidden")
    })

    getElement("problem_list").innerHTML = await getProblem(0) 
    problemCount = getProblemSetting()

    const pro = getElement("profile");
    pro.addEventListener("animationiteration",function(){
        pro.classList.remove("animationStart")
        pro.classList.add("animationStop")
        profileRunning = false
    })

    const problem =getElement("problem")
    problem.addEventListener("animationiteration",function(){
        problem.classList.remove("animationStart")
        problem.classList.add("animationStop")
        problemRunning = false
    })
}

function show_interface(index){
    const text=[
        ["編輯使用者名稱","請輸入新使用者名稱與密碼","使用者名稱","username"],
        ["編輯電子郵件","請輸入新電子郵件與密碼","電子郵件","email"],
        ["編輯所屬學校","請輸入新所屬學校與密碼","所屬學校","school"],
        ["編輯個人簡介","請輸入新個人簡介與密碼","個人簡介","introduce"],
    ]
    document.getElementById("change_main_title").innerText=text[index][0]
    document.getElementById("change_subtitle").innerText=text[index][1]
    document.getElementById("input_indecate").innerText=text[index][2]
    document.getElementById("new").value=getElement(text[index][3]).innerText
    document.getElementById("change_interface").classList.remove("hidden")
    document.getElementById("cover").classList.remove("hidden")
}

function inputpage(){
    const i = getElement("InputPage")
    var value = i.value
    if(value == ""){

    }
    else if
}

function contentchange(c){
    if(profileRunning ||  problemRunning) return
    if(state!=c){
        getElement("profile").classList.remove("animationStop")
        getElement("problem").classList.remove("animationStop")
        getElement("profile").classList.add("animationStart")
        getElement("problem").classList.add("animationStart")
        if(c==1){
            getElement("first_choice").className="unselect"
            getElement("second_choice").className="select"
        }
        else{
            getElement("first_choice").className="select"
            getElement("second_choice").className="unselect"
        }
        state = c
        profileRunning = true
        problemRunning = true
    }
}

init()