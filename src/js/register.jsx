function getRandomInt(max) {
    return Math.floor(Math.random() * max);
}

class RegisterButton extends React.Component {
    constructor(props){
        super(props)
        this.state = {status: null, github_oauth_url: null, google_oauth_url: null, random_color: props.random_color}
    }
    componentDidMount() {
        $.ajax({
            url: "./oauth_info",
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
        let {status, github_oauth_url, google_oauth_url, color} = this.state
        let normal_submit = <button type="submit" id="viaAccount" className="w-full text-white text-lg p-2 rounded my-2 duration-150"> 註冊 </button>
        let github_submit = <a id="viaGithub" href={github_oauth_url} className="w-full bg-black text-white text-lg p-2 rounded my-2 duration-150 hover:bg-gray-800"> 使用 Github OAuth 進行註冊 </a>
        let google_submit = <a id="viaGoogle" href={google_oauth_url} className="w-full bg-gray-300 text-black text-lg p-2 rounded my-2 duration-150 hover:bg-gray-200"> 使用 Google OAuth 進行註冊 </a>
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

class RegisterForm extends React.Component {
    constructor(props){
        super(props)
        let color_array = ["blue", "orange", "purple", "red"]
        this.state = {handle: "", email: "", password: "", random_color: color_array[getRandomInt(4)]}
        this.handleAccountChange = this.handleAccountChange.bind(this);
        this.handleEmailChange = this.handleEmailChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }
    handleAccountChange(event){
        this.setState({handle: event.target.value})
    }
    handleEmailChange(event){
        this.setState({email: event.target.value})
    }
    handlePasswordChange(event){
        this.setState({password: event.target.value})
    }
    handleSubmit(event){
        let {handle, email, password} = this.state
        event.preventDefault();
        const shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
        shaObj.update(password)
        console.log(email)
        $.ajax({
            url: "./register",
            type: "POST",
            data: JSON.stringify({"handle": handle, "email": email, "password": shaObj.getHash("HEX")}),
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                let redirect = data["mail_verification_redirect"] ? "/mail_check" : "/"
                if(data["status"] == "OK"){
                    success_swal("註冊成功").then(() => {window.location.href = redirect})
                }else{
                    error_swal("註冊失敗", data["code"])
                }
            }
        })
    }
    componentDidMount(){
        let {random_color} = this.state
        /* Update Background and button color */
        document.getElementById("register_background").classList.add("bg-" + random_color + "-300")
        let input_field_array = document.getElementsByTagName("input")
        for(let i = 0; i < input_field_array.length; i++){
            input_field_array[i].classList.add("focus:border-" + random_color + "-500")
        }
    }
    render() {
        let {handle, email, password, random_color} = this.state
        let register_form = (
            <div className="w-full h-screen flex">
                <div className="bg-blue-500 bg-blue-300 bg-orange-500 bg-orange-300 bg-purple-500 bg-purple-300 bg-red-500 bg-red-300"></div>
                <div className="hover:bg-blue-300  hover:bg-orange-300 hover:bg-purple-300 hover:bg-red-300"></div>
                <div className="focus:border-blue-500 focus:border-orange-500 focus:border-purple-500 focus:border-red-500"></div>
                <div id="register_background" className="w-full h-screen bg-cover">
                    <form className="absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3" onSubmit={this.handleSubmit}>
                        <div className="pb-5">
                            <a href="/"><img className="w-[18%] mx-auto" src="/static/logo_min.png" /></a>
                        </div>
                        <p className="text-4xl text-center mb-10"> 註冊 </p>
                        <div className="mt-10 flex flex-col gap-5">
                            <div className="flex flex-col gap-1">
                                <input type="text" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white" placeholder="使用者名稱" onChange={this.handleAccountChange} />
                                <HandleValidNotice handle={handle}/>
                            </div>
                            <div className="flex flex-col gap-1">
                                <input type="text" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white" placeholder="信箱" onChange={this.handleEmailChange} />
                                <EmailValidNotice email={email} />
                            </div>
                            <div className="flex flex-col gap-1">
                                <input type="password" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:bg-white" placeholder="密碼" onChange={this.handlePasswordChange} />
                                <PasswordValidNotice password={password}/>
                            </div>
                        </div>
                        <div className="mt-10 flex flex-col text-center">
                            <RegisterButton random_color={random_color} />
                        </div>
                        <div>
                            <a className="w-full text-center" href="/login">  
                                <p className="text-gray-500 mt-10">已經有帳號了嗎？點此登入</p>
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        )
        return register_form
    }
}

const root = ReactDOM.createRoot(document.getElementById("register_form"))
root.render(<RegisterForm />)