class User_info extends React.Component{
    constructor(props){
        super(props)
        this.state={
            isLogin : undefined,
            handle : ""
        }
        this.check_cookie = this.check_cookie.bind(this)
    }

    componentDidMount(){
        this.check_cookie()
    }

    check_cookie(){
        fetch("/api/auth/verify_jwt",{method : "POST"}).then((resp)=>{
            return resp.json()
        }).then((json)=>{
            this.setState({
                isLogin : true,
                handle : json.data.handle
            })
        })
    }

    render(){
        var main;
        if(this.state.isLogin){
            var herf = "/profile/"+this.state.handle
            main = (
                <div className="w-full h-fit my-auto text-center">
                    <p className="text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer"> 
                        <a href={herf}>{this.state.handle}</a> 
                    </p>
                </div>
            )
        }
        else if(this.state.isLogin === false){
            main=[
                <div className="w-full h-fit my-auto text-center">
                    <p className="text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer"> 
                        <a href="/login">登入</a> 
                    </p>
                </div>,
                <div className="w-full h-fit my-auto text-center">
                    <p className="text-base lg:text-2xl inline-block align-middle leading-normal my-0 font-['Noto_Sans_TC'] border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100 cursor-pointer"> 
                        <a href="/register">註冊</a> 
                    </p>
                </div>
            ]
        }
        return main
    }
}