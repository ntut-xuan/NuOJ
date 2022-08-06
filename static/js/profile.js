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
var problemCount = 80


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
    data =""
    await fetch("/problem_list_setting").then(function(response){
        if(response.status == 400){
            document.location.href="/";
        }
        else{
            return response.json()
        }
    }).then(function(res){
        data = res
    })
    return data["count"]
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

async function toPage(i){
    var index=0
    const max = parseInt(problemCount/4)+1
    if(i>max) index = max
    else if(i<1) index =1
    else index =i

    if(getElement("InputPage").value == index) return

    getElement("InputPage").value=index
    numbers=[]
    for(var x =index-2;x<index+3;x++){
        if((x>0) && (x <= max)){
            numbers.push(x)
        }
        else{
            numbers.push("")    
        }
    }
    // console.log(numbers)
    getElement("left_number").innerHTML=
    `
        <div style="width: 27px;height: 27px;display: flex;justify-content: center;align-items: center;">
            ${numbers[0]}
        </div>
        <div style="width: 27px;height: 27px;display: flex;justify-content: center;align-items: center;">
            ${numbers[1]}
        </div>
    `
    getElement("right_number").innerHTML=
    `
        <div style="width: 27px;height: 27px;display: flex;justify-content: center;align-items: center;">
            ${numbers[3]}
        </div>
        <div style="width: 27px;height: 27px;display: flex;justify-content: center;align-items: center;">
            ${numbers[4]}
        </div>
    `
    getElement("problem_list").innerHTML = await getProblem(index-1) 
}

function bigjump(i){
    if(i==0){
        toPage(1)
    }
    else{
        toPage(100)
    }
}

function jump(i){
    var page =parseInt(getElement("InputPage").value)
    if(i==0){
        toPage(page-1)
    }
    else{
        toPage(page+1)
    }
}

function inputpage(){
    const i = getElement("InputPage")
    var value = i.value
    const max = parseInt(problemCount/4)+1
    if(value == ""){
        i.value = "1"
    }
    else if(parseInt(value) < 1){
        i.value ="1"
    }
    else if(parseInt(value) > max){
        i.value = max
    }
    toPage(i.value)
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

    toPage(1)
    problemCount = await getProblemSetting()
    console.log(problemCount)

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


init()