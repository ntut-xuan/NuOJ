class LoginComponent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            handle: null,
            isLogin: null
        };
    }
    componentDidMount() {
        $.ajax({
            url: "/session_verification",
            type: "POST",
            success: function(data, status, xhr){
                if(data["status"] == "OK"){
                    this.setState({isLogin: true, handle: data["handle"]})
                }else{
                    this.setState({isLogin: false})
                }
            }.bind(this),
            error: function(status, xhr){
                this.setState({isLogin: false})
            }.bind(this)
        })
    }
    render(){
        const {handle, isLogin} = this.state
        // redirect_url = "https://nuoj.ntut-xuan.net/profile/" + handle
        redirect_url = "/profile/" + handle
        element_class = "text-white text-2xl border-b-2 border-white border-opacity-0 duration-500 hover:border-white hover:border-opacity-100"
        login_div = [
            <div>
                <a className={element_class} href="/login"> 登入 </a>
            </div>,
            <div>
                <a className={element_class} href="/register"> 註冊 </a>
            </div>
        ]
        profile_div = (
            <div>
                <a className={element_class} href={redirect_url}> {this.state.handle} </a>
            </div>
        )
        if(isLogin === null){
            return null;
        }else{
            return isLogin ? profile_div : login_div;
        }
    }
}

const root = ReactDOM.createRoot(document.getElementById('login_div'));
root.render(<LoginComponent />);