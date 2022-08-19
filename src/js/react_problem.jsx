class User_info extends React.Component{
    constructor(props){
        super(props)
        this.state={
            isLogin : false,
            handle : ""
        }
        this.check_cookie = this.check_cookie.bind(this)
    }

    componentDidMount(){
        this.check_cookie()
    }

    check_cookie(){
        fetch("/session_verification",{method : "POST"}).then((resp)=>{
            return resp.json()
        }).then((json)=>{
            if(json.status=="OK"){
                this.setState({
                    isLogin : true,
                    handle : json.handle
                })
            }
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
        else{
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

class Page_selecter extends React.Component{

}

class Problem_list extends React.Component{
    constructor(props){
        super(props)
        this.state={
            problems : [],
            total_problem_num : 0,
            page_now : 1
        }
    }

    componentDidMount(){
        this.getProblems(0,50)
    }

    getProblems(j,i){
        fetch("/all_problem_list?"+new URLSearchParams({numbers:i,from:j})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : this.state.problems.concat(list.data)
            })
        })
    }

    getTotalNum(){
        fetch("/profile_problem_setting").then((res)=>{
            return res.json()
        }).then((data)=>{
            this.setState({
                problem_number : data["count"]
            })
        })
    }

    render(){
        var main=[];
        this.state.problems.forEach(element=>{
            var col=(
            <tr className="hover:bg-slate-100 z-40 border">
                <td className="px-6 py-4 z-10"> {element.id} </td>
                <td className="px-6 py-4 z-10 text-blue-700"> <a href="/problem/{{item.problem_ID}}">{element.title}</a> </td>
                <td className="px-6 py-4 z-10 text-blue-700"> <a href="/profile/{{item.problem_author}}">{element.author}</a> </td>
                <td className="px-6 py-4 z-10 flex gap-5 justify-center text-base"> 
                    {/* <span class="p-1 bg-gray-200 rounded-lg hover:bg-orange-100 duration-300 cursor-pointer"> </span> */}
                </td>
            </tr>
            )
            main.push(col)
        })
        return main
    }
}

const userRoot = ReactDOM.createRoot(document.getElementById("user_title"))
userRoot.render(<User_info></User_info>)

const ProblemList = ReactDOM.createRoot(document.getElementById("table"))
ProblemList.render(<Problem_list></Problem_list>)