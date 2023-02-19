class App extends React.Component{
    constructor(props){
        super(props)
        this.state = {status: "驗證中", message: "", error_code: ""}
    }
    componentDidMount(){
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString)

        const code = urlParams.get("code")

        if(code == null){
            this.setState({
                status: "驗證失敗",
                message: "驗證碼不存在",
                error_code: "ABSENT_VERIFICATION_CODE"
            })
        }

        $.ajax({
            url: "/api/auth/verify_mail?code=" + code,
            type: "POST",
            success: function(data, status, xhr){
                this.setState({
                    status: "驗證成功",
                    message: "信箱已驗證，約兩秒後轉址至首頁",
                })
                window.setTimeout(function(){
                    window.location.href = "/";
                }, 2000);
            }.bind(this),
            error: function(xhr, exception){
                if(xhr.status == 422){
                    this.setState({
                        status: "驗證失敗",
                        message: "驗證碼無效",
                        error_code: "INVALID_CODE"
                    })
                }
            }.bind(this)
        })
    }
    render(){
        const {status, message, error_code} = this.state
        return [
            <p class="w-fit mx-auto text-lg font-mono rounded-lg"> {status} </p>,
            <p class="w-fit mx-auto text-sm font-mono rounded-lg py-2"> {message} </p>,
            <p class="w-fit mx-auto text-sm font-mono rounded-lg pt-5 text-gray-500"> {error_code} </p>
        ]
    }
}

const root = ReactDOM.createRoot(document.getElementById("verify_mail_result"))
root.render(<App />)