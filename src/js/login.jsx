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
        this.state = {status: null, github_oauth_url: null, google_oauth_url: null}
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
    render() {
        let {status, github_oauth_url, google_oauth_url} = this.state 
        let normal_submit = <button type="submit" id="viaAccount" className="w-full bg-orange-500 text-white text-lg p-2 rounded my-2 duration-150 hover:bg-orange-300"> 登入 </button>
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
        this.state = {account: "", password: ""}
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
        const shaObj = new jsSHA("SHA-512", "TEXT", { encoding: "UTF8" });
        shaObj.update(password)
        $.ajax({
            url: "./login",
            type: "POST",
            data: JSON.stringify({"account": account, "password": shaObj.getHash("HEX")}),
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                if(data["status"] == "OK"){
                    success_swal("登入成功").then(() => {window.location.href = "/"})
                }else{
                    if(data["code"] === 304){
                        window.location.href = "/mail_check"
                    }else{
                        error_swal("登入失敗", data["code"])
                    }
                }
            }
        })
    }
    render() {
        let {account, password} = this.state
        let login_form = (
            <form className="absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] w-[40%] bg-white bg-opacity-100 rounded p-10 pb-3" onSubmit={this.handleSubmit}>
                <p className="text-4xl text-center mb-10"> 登入 </p>
                <div className="mt-10 flex flex-col gap-5">
                    <div className="flex gap-1 flex-col">
                        <input type="text" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:border-orange-500 focus:bg-white" placeholder="帳號或電子信箱" onChange={this.handleAccountChange}/>
                        <AccountValidNotice account={account}/>
                    </div>
                    <div className="flex gap-1 flex-col">
                        <input type="password" className="w-full bg-slate-100 p-2 text-base px-4 border-2 border-gray-600 appearance-none resize-none overflow-y-hidden rounded focus:outline-none focus:border-orange-500 focus:bg-white" placeholder="密碼" onChange={this.handlePasswordChange} />
                        <PasswordValidNotice password={password}/>
                    </div>
                </div>
                <div className="mt-10 flex flex-col text-center">
                    <LoginButton />
                </div>
                <div>
                    <a className="w-full text-center" href="/register">  
                        <p className="text-gray-500 mt-10">沒有帳號嗎？點此註冊</p>
                    </a>
                </div>
            </form>
        )
        return login_form
    }
}

const root = ReactDOM.createRoot(document.getElementById("login_form"))
root.render(<LoginForm />)