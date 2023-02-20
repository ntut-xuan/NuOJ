
function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

function AccountValidNotice(prop){
    let account = prop.account
    if (account.includes("@")){
        return <EmailValidNotice email={account} />
    }else{
        return <HandleValidNotice handle={account} />
    }
}

class LoginButton extends React.Component {
    constructor(props){
        super(props)
        this.state = {status: null, github_oauth_url: null, google_oauth_url: null, random_color: props.color}
    }
    componentDidMount() {
        let {random_color} = this.state
        $.ajax({
            url: "/api/auth/oauth_info",
            type: "GET",
            success: function(data, status, xhr){
                if(data["status"] == "OK"){
                    this.setState({status: data["status"]})
                    if(data.hasOwnProperty("github_oauth_url")){
                        this.setState({github_oauth_url: data["github_oauth_url"]})
                    }
                    if(data.hasOwnProperty("google_oauth_url")){
                        this.setState({google_oauth_url: data["google_oauth_url"]})
                    }
                }
            }.bind(this)
        })
    }
    componentDidUpdate(){
        let {status, random_color} = this.state
        if(status != null){
            document.getElementById("viaAccount").classList.add("bg-" + random_color + "-500")
            document.getElementById("viaAccount").classList.add("hover:bg-" + random_color + "-300")
        }
    }
    render() {
        let {status, github_oauth_url, google_oauth_url} = this.state
        let normal_submit = <button type="submit" id="viaAccount" className="w-full text-white text-lg p-2 rounded my-2 duration-150"> 登入 </button>
        let github_submit = <a id="viaGithub" href={github_oauth_url} className="w-full bg-black text-white text-lg p-2 rounded my-2 duration-150 hover:bg-gray-800"> 使用 Github OAuth 進行登入 </a>
        let google_submit = <a id="viaGoogle" href={google_oauth_url} className="w-full bg-gray-300 text-black text-lg p-2 rounded my-2 duration-150 hover:bg-gray-200"> 使用 Google OAuth 進行登入 </a>
        let render_component = [normal_submit]
        if(github_oauth_url != null){
            render_component.push(github_submit)
        }
        if(google_submit != null){
            render_component.push(google_submit)
        }
        if(status == null){
            return null;
        }else{
            return render_component;
        }
    }
}

class LoginForm extends React.Component {
    constructor(props){
        super(props)
        color_array = ["blue", "orange", "purple", "red"]
        this.state = {account: "", password: "", random_color: color_array[getRandomInt(4)]}
        this.handleAccountChange = this.handleAccountChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleAccountChange(event){
        this.setState({account: event.target.value})
    }
    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }
    handleSubmit(event){
        let {account, password} = this.state
        event.preventDefault();
        $.ajax({
            url: "/api/auth/login",
            type: "POST",
            data: JSON.stringify({"account": account, "password": password}),
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                success_swal("登入成功").then(() => {window.location.href = "/"})
            },
            error(xhr, exception){
                if(xhr.status == 403){
                    error_swal("登入失敗", "帳號或密碼錯誤")
                }else if(xhr.status == 422){
                    error_swal("登入失敗", "錯誤的信箱格式")
                }else if(xhr.status == 401){
                    show_mail_confirm_swal(account)
                }
            }
        })
    }
    componentDidMount(){
        let {random_color} = this.state
        let use_bg = "bg-blue-500 bg-blue-300 bg-orange-500 bg-orange-300 bg-purple-500 bg-purple-300 bg-red-500 bg-red-300"
        let use_hover_bg = "hover:bg-blue-300  hover:bg-orange-300 hover:bg-purple-300 hover:bg-red-300"
        let use_focus_bg = "focus:border-blue-500 focus:border-orange-500 focus:border-purple-500 focus:border-red-500"
        /* Update Background and button color */
        document.getElementById("login_background").classList.add("bg-" + random_color + "-300")
        let input_field_array = document.getElementsByTagName("input")
        for(let i = 0; i < input_field_array.length; i++){
            input_field_array[i].classList.add("focus:border-" + random_color + "-500")
        }
    }
    render() {
        let {account, password, random_color} = this.state
        let login_form = (
            <div className="w-full h-screen flex">
                <div id="login_background" className="w-full h-screen bg-cover">
                    <div className="w-full h-screen bg-cover">
                        <div className="w-full h-full">
                            <form className="absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3 h-fit" onSubmit={this.handleSubmit}>
                                <div className="pb-5">
                                    <a href="/">
                                        <img className="w-[18%] mx-auto hover:bg-slate-200 rounded-lg p-3 transition-all duration-500" data-tooltip="hello world" src="/static/logo_min.png" />
                                    </a>
                                </div>
                                <p className="text-4xl text-center mb-10"> 登入 </p>
                                <div className="mt-10 flex flex-col gap-5">
                                    <div className="flex gap-1 flex-col">
                                        <input type="text" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white" placeholder="帳號或電子信箱" onChange={this.handleAccountChange}/>
                                        <AccountValidNotice account={account}/>
                                    </div>
                                    <div className="flex gap-1 flex-col">
                                        <input type="password" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white" placeholder="密碼" onChange={this.handlePasswordChange} />
                                        <PasswordValidNotice password={password}/>
                                    </div>
                                </div>
                                <div className="mt-10 flex flex-col text-center">
                                    <LoginButton color={random_color}/>
                                </div>
                                <div>
                                    <a className="w-full text-center" href="/register">
                                        <p className="text-gray-500 mt-10">沒有帳號嗎？點此註冊</p>
                                    </a>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        )
        return login_form
    }
}

function show_mail_confirm_swal(handle){
    Swal.fire({
        icon: "warning",
        title: "信箱驗證",
        text: "驗證信應已寄至您的信箱，請確認並驗證郵件！",
        showDenyButton: true,
        confirmButtonText: "OK",
        denyButtonText: "沒有收到信，重寄一封"
    }).then((result) => {
        if(result.isDenied){
            run_resend_email(handle)
        }
    })
}

function run_resend_email(account){
    $.ajax({
        url: "/api/auth/resend_email?account=" + account,
        type: "POST",
        success: function(data, status, xhr){
            success_swal("信件已寄送")
        },
        error: function(xhr, exception){
            if(xhr.status == 422){
                error_swal("寄送失敗", "登入使用的 Handle 或信箱尚未註冊")
            }else if(xhr.status == 403){
                error_swal("寄送失敗", "信箱驗證設置尚未開啟")
            }
        }
    })
}

const root = ReactDOM.createRoot(document.getElementById("login_form"))
root.render(<LoginForm />)