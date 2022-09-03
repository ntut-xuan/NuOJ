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
    constructor(props){
        super(props)
        this.state={

        }
        this.render_btu = this.render_btu.bind(this)
    }

    render_btu(){
        const showing = this.props.showing 
        const max = this.props.max
        var main=[]
        if(showing >=5){
            main.push(<button>1</button>)
            main.push(<button>2</button>)
            if((showing-5)>0){
                main.push(<div>...</div>)
            }
        }


        for(var i=-2;i<3;i++){
            var index = showing+i
            if((index > 0) && (index<=max)){
                main.push(<button>{index}</button>)
            }
        }

        if(showing <= (max-3)){
            if((showing+4) < max ){
                main.push(<div>...</div>)
            }
            for(var i=-1;i<1;i++){
                if((max+i)>(showing + 2)){
                    main.push(<button>{max+i}</button>)
                }
            }
        }
        return main
    }

    render(){
        let main= (
            <div className="flex justify-center gap-10" >
                <button>&lt;&lt;</button>
                <button>&lt;</button>
                <this.render_btu></this.render_btu>
                <button>&gt;</button>
                <button>&gt;&gt;</button>
            </div>
        )
        return main
    }
}

class Problem_list extends React.Component{
    constructor(props){
        super(props)
        this.state={
            problems : [],
            total_problem_num : 0,
            page_now : 1,
            max : 1
        }
        this.render_col = this.render_col.bind(this)
    }

    componentDidMount(){
        this.getProblems(0,50)
    }

    getProblems(j,i){
        fetch("/all_problem_list?"+new URLSearchParams({numbers:i,from:j})).then((res)=>{
            return res.json()
        }).then((json)=>{
            
            var index = Math.ceil(json.data.length/9)
            if(index == 0) index =1
            
            this.setState({
                problems : this.state.problems.concat(json.data),
                max : index
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

    render_col(){
        var main=[];
        const problems = this.state.problems
        for(var i=0;i<9;i++){
            if(i>=(problems.length)){
                break
            }
            var col=(
                <tr className="hover:bg-slate-100 z-40 border">
                    <td className="px-6 py-4 z-10"> {problems[i].id} </td>
                    <td className="px-6 py-4 z-10 text-blue-700"> <a href={`/profile/${problems[i].id}`}>{problems[i].title}</a> </td>
                    <td className="px-6 py-4 z-10 text-blue-700"> <a href={`/profile/${problems[i].author}`}>{problems[i].author}</a> </td>
                    <td className="px-6 py-4 z-10 flex gap-5 justify-center text-base"> 
                        {/* <span class="p-1 bg-gray-200 rounded-lg hover:bg-orange-100 duration-300 cursor-pointer"> </span> */}
                    </td>
                </tr>
            )
            main.push(col)
        }
        return main
    }

    render(){
        var main=[
            <table className="w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal">
                <thead>
                    <tr>
                        <th scope="col" className="sticky top-0 bg-orange-200 px-6 py-3 w-[10%]">題目 ID</th>
                        <th scope="col" className="sticky top-0 bg-orange-200 px-6 py-3 w-[40%]">題目名稱</th>
                        <th scope="col" className="sticky top-0 bg-orange-200 px-6 py-3 w-[10%]">題目作者</th>
                        <th scope="col" className="sticky top-0 bg-orange-200 px-6 py-3 w-[40%]">題目標籤</th>
                    </tr>
                </thead>
                <tbody>
                    <this.render_col></this.render_col>
                </tbody>
            </table>,
            <Page_selecter showing={this.state.page_now} max={this.state.max}></Page_selecter>
        ]
        return main
    }
}

const userRoot = ReactDOM.createRoot(document.getElementById("user_title"))
userRoot.render(<User_info></User_info>)

const ProblemList = ReactDOM.createRoot(document.getElementById("table"))
ProblemList.render(<Problem_list></Problem_list>)