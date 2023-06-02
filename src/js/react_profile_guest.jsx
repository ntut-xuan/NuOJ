function success_swal(title){
    return Swal.fire({
        icon: "success",
        title: title,
        timer: 1500,
        showConfirmButton: false
    })
}

function error_swal(title){
    return Swal.fire({
        icon: "error",
        title: title,
        timer: 1500,
        showConfirmButton: false
    })
}

// ============================個人介紹部分============================

class Subtitle extends React.Component{ 
    render_titles(titles){
        const lines = Object.entries(titles)
        resp =[]
        lines.forEach(element=>{
            if(element[1]!="")
                resp.push(
                    <div key={element[0]} className="">
                        <p className="text-base text-slate-400 break-words">{element[1]}</p>
                    </div>
                ) 
        })
        return resp
    }
    render(){
        var maintitles = this.props.maintitles
        var main = (
            <div className="container gap-5 p-10 flex flex-col profile-area">
                <div className="m-auto">
                    <div className="profile-img-container" >
                        <img id="user_avater" className="profile-img" src={maintitles.img}/>
                    </div>
                </div>
                <div className="w-full flex flex-col">
                    <p className="text-base font-mono">{maintitles.accountType}</p>
                    <p className="text-6xl font-mono ">{maintitles.handle}</p>
                </div>
                <div className="flex flex-col">
                    {this.render_titles(this.props.subtitles)}
                </div>
            </div>
        )
        return main
    }
}

class Introduce extends React.Component {
    constructor(pro){
        super(pro)
        this.state={
            profile_data : {
                main:{
                    img : "",
                    handle : "",
                    accountType : ""
                },
                sub:{
                    email : "",	
                    school : "",
                    bio : ""
                }
            },
        }
        this.changing_mode = this.change_mode.bind(this)
        this.get_profile = this.get_profile.bind(this)
        this.update_profile = this.update_profile.bind(this)
    }

    componentDidMount(){
        this.get_profile()
    }

    get_profile(){
    var location = window.location.href.split("/")
    const handle = location[location.length-1] 

    fetch("/api/profile/" + handle).then((response) => {
        if(response.ok){
            response.json().then((json) => {
                console.log(json)
                let profile_data = {
                    main: {
                        img: "/api/profile/" + handle + "/avatar",
                        handle: handle,
                        accountType: json.role
                    },
                    sub: {
                        email: json.email,
                        school: json.school,
                        bio: json.bio
                    }
                }
                this.setState({profile_data: profile_data, mode: false})
            })  
        }
    })
    }
    
    update_profile(i){
        var temp = this.state.profile_data
        temp.sub = i
        this.setState({
            profile_data : temp
        })
    }

    change_mode(i){
        if(i){
            this.get_profile()
        }
        this.setState({ changing : !this.state.changing })
    }

    render(){
        const subtitles = this.state.profile_data.sub
        const maintitles = this.state.profile_data.main
        return (<Subtitle subtitles={subtitles} maintitles={maintitles} change={()=>this.change_mode()}></Subtitle>)
        
    }
}

// ============================主要部分============================

class PageSlecter extends React.Component{
    constructor(props){
        super(props)
        this.state={
            inputbox : "1"
        }
        this.change = this.change.bind(this)
        this.limit = this.limit.bind(this)
    }

    change(event){
        this.setState({ inputbox : event.target.value.replace(/[^\d]/g,'') })
    }

    limit(){
        const showing = this.state.inputbox
        var real_page;
        if(showing == "")    real_page = 1
        else if(parseInt(showing) < 1) real_page = 1
        else if(parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage
        else real_page = parseInt(showing)

        this.setState({ inputbox : real_page })

        this.props.topage(real_page)
    }

    bigjump(i){
        var real_page;
        if(i){
            this.props.topage(1)
            real_page =1;
        }
        else{
            this.props.topage(this.props.Lastpage)
            real_page =this.props.Lastpage;
        }
        this.setState({
            inputbox : real_page
        })

    }

    littlejump(i){
        var showing;
        if(i) showing = this.state.inputbox -1;
        else showing = this.state.inputbox +1
        if(parseInt(showing) < 1) real_page = 1
        else if(parseInt(showing) > this.props.Lastpage) real_page = this.props.Lastpage
        else real_page = parseInt(showing)

        this.setState({ inputbox : real_page })
        this.props.topage(real_page)
    }

    render(){
        let main= (
            <div className="page_container" >
                <button onClick={()=>this.bigjump(1)}>&lt;&lt;</button>
                <button onClick={()=>this.littlejump(1)}>&lt;</button>
                <div  className="page_showing"></div>
                <div  className="page_showing"></div>
                <input type="text" 
                    value={this.state.inputbox}
                    className="page_showing page_now_showing"
                    onChange  = {this.change} 
                    onBlur = {this.limit}
                    maxLength={2}/>
                <div  className="page_showing"></div>
                <div  className="page_showing"></div>
                <button onClick={()=>this.littlejump(0)}>&gt;</button>
                <button onClick={()=>this.bigjump(0)}>&gt;&gt;</button>
            </div>
        )
        return main
    }
}


class Problem_info extends React.Component{
    render(){
        var status;
        if(this.props.permission == true){
            status=<p>公開</p>
        }
        else{
            status=<p>未公開</p>
        }
        let url ="/edit_problem/" + this.props.problem_pid + "/basic"

        var main=(
            <div className="w-50">
                <div className="problem-container">
                    <div className="border-sd p-10 flex flex-col">
                        <div className="flex g-10 align-items-center problem-title">
                            <a href={url}  className="text-size-small problem-info-col text-bule">
                                {this.props.title}
                            </a>
                        
                            {status}
                        </div>
                        <div className="problem-info-col">

                        </div>
                    </div>
                </div>
            </div>
        )

        var all=(
            <div className="p-10 flex flex-col">
                <div className="flex g-10 align-items-center problem-title">
                    <a href={url}  className="text-size-small problem-info-col text-bule">
                        {this.props.title}
                    </a>
                    {status}
                </div>
                <div className="problem-info-col"></div>
                <hr />
            </div>
        )
        

        if(this.props.mode == true){
            return main
        }
        else{
            return all
        }
    }
}

class Problem_List extends React.Component{
    constructor(prop){
        super(prop)
        this.state={
            num_per_page : 10,
            showing : 1,
            problems : {},
            total_number : 0
        }

        this.topage = this.topage.bind(this)
        this.render_problem_list = this.render_problem_list.bind(this)
    }

    componentDidMount(){
        this.getNumbers()
        this.getProblems()
    }


    getNumbers(){
        var location = window.location.href.split("/")
        const handle = location[location.length-1] 
        fetch("/get_user_problem_number?"+new URLSearchParams({handle:handle})).then((res)=>{
            return res.json()
        }).then((json)=>{
            const status = json.status;
            if(status == "OK"){
                this.setState({ total_number : json.data })
            }
        })
    }

    getProblems(){
        const num_per_page = this.state.num_per_page
        const showing = this.state.showing
        const problems = this.state.problems

        if(problems[showing] != undefined){
            return
        }
        var location = window.location.href.split("/")
        const handle = location[location.length-1] 
        fetch("/profile_problem_list?"+new URLSearchParams({mode:num_per_page,page:showing,handle:handle})).then((res)=>{
            return res.json()
        }).then((json)=>{
            const status = json.status;
            if(status == "OK"){
                var temp = this.state.problems
                temp[showing]=json.data
                this.setState({ problems : temp })
            }
        })
    }

    topage(i){
        if(i==this.state.showing) return
        var real_page;
        var max = Math.ceil(this.state.total_number / this.state.num_per_page)
        
        if(i>max) real_page = max
        else if(i<1) real_page = 1
        else real_page = i
        this.setState({showing : real_page})
        this.getProblems()
    }

    render_problem_list(){
        const None_problems=(
            <div className="h-full w-hull flex items-center">
                <p className="problem-notification p-10"> He/She didn't released any problem yet</p>
            </div>
        )
        if(this.state.total_number == 0){
            
            return None_problems
        }

        re=[]
        const showing = this.state.showing
        const lists = this.state.problems[showing]
        if(lists == undefined) return None_problems

        lists.forEach(function(element){
            var status;
            if(element.permission == true){
                status=<p>公開</p>
            }
            else{
                status=<p>未公開</p>
            }
            const url ="/edit_problem/" + element.problem_pid + "/basic"

            const info =(
                <div className="p-5 flex flex-col">
                    <div className="gap-5 problem-title">
                        <a href={url}  className="text-xl problem-info-col text-blue-700/70">
                            {element.title}
                        </a>
                        {status}
                    </div>
                    <div className="problem-info-col w-ful"></div>
                    <hr/>
                </div>
            )

            re.push(info)
        })
        return re
    }

    render(){
        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problem list</p>
                </div>
                <div className="problem-list-container">
                    {this.render_problem_list()}
                </div>
            </div>  
        )

        return main
    }
}
class OverView_problem extends React.Component {
    constructor(props){
        super(props)
        this.state={
            problem_number : 0,
            problems : []
        }

        this.render_poroblems = this.render_poroblems.bind(this)
    }

    componentDidMount(){
        var location = window.location.href.split("/")
        const handle = location[location.length-1] 
        fetch("/profile_problem_list?"+new URLSearchParams({mode:4,page:1,handle:handle})).then((res)=>{
            return res.json()
        }).then((json)=>{
            const status = json.status;
            if(status == "OK"){
                this.setState({ problems : json.data })
            }
            else{
                this.setState({ problems : [] })
            }
        })
    }

    render_poroblems(){
        re=[]
        const max = this.state.problems.length
        for(var i= 0;i<4;i++){
            if(i>=max){
                break;
            }
            var element = this.state.problems[i]
            let url ="/edit_problem/" + element.problem_pid + "/basic"
            if(element.permission == true){
                problem_status=<p>公開</p>
            }
            else{
                problem_status=<p>未公開</p>
            }
            const info_card = (
                <div className="w-1/2 " key={element.problem_pid}>
                    <div className="problem-container">
                        <div className="problem-overview-container">
                            <div className="gap-5 problem-title">
                                <a href={url}  className="text-xl problem-info-col text-blue-700/80">
                                    {element.title}
                                </a>
                            {problem_status}
                            </div>
                            <div className="problem-info-col w-full"></div>
                        </div>
                    </div>
                </div>
            )
            re.push(info_card)
        }

        var main=(
            <div className="problem-overview-list">
                {re}
            </div>
        )
        if(re.length==0){
            var None_problems=(
                <p className="problem-notification p-10"> He/She didn't released any problem yet</p>
            )
            return None_problems
        }
        else{
            return main
        }
    }

    render(){
        var overflow_tag;
        if(this.props.num_of_problem>4){
            overflow_tag=(
                <button onClick={()=>this.props.onclick("Problem")}>...see more</button>
            )
        }
        else{
            overflow_tag = ""
        }

        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problem list</p>
                </div>
                <div className="">
                    {this.render_poroblems()}
                </div>
                <div className="flex justify-content-end">
                    {overflow_tag}
                </div>
            </div>  
        )
        return main
    }
}


class Info_selecter extends React.Component{
    render(){
        var main = [
            <div className="flex gap-5 m-b-10 ">
                <button className="page-info-btn" onClick={()=>this.props.onclick("OverView")}>
                    <img src="/static/house.svg" alt="" />
                </button>
                <div className="page-info-container">
                    <div className="page-info">
                        <button onClick={()=>this.props.onclick("OverView")} className="page-info-btn">OverView</button>
                    </div>
                    <div className="page-info">
                        <button onClick={()=>this.props.onclick("Problem")} className="page-info-btn">Problems</button>
                    </div>
                    <div className="page-info flex page-info-indecater" style={{ transform : `translateX(${this.props.pos})`}}>
                        <p>&lt;</p>
                        <p>&gt;</p>
                    </div>
                </div>
            </div>,
            <hr/>
        ]
        return main
    }
}

// ============================工具欄部分============================

class ToolBar extends React.Component{
    constructor(prop){
        super(prop)
    }

    logout(){
        fetch("/logout").then((res)=>{ return res.json()}).then((json)=>{
            if(json.status == "OK"){ 
                success_swal("登出成功").then(() => {window.location.href = "/" })
            }
            else{
                error_swal("登出失敗")
            }
        })
    }
    render(){
        let main = (
            <div className="items-center flex tool_bar">
                <div className="flex gap-10 w-4/5 items-center">
                    <div className="h-50">
                        <a href="/"><img width={100} src="/static/logo-black.svg"/></a>
                    </div>
                    <a href="/problem" ><p className="text-lg">題目</p></a>
                    <a href="/about" ><p className="text-lg">關於</p></a>
                    <a href="/status" ><p className="text-lg">狀態</p></a>
                </div>
                <div className="w-1/5 flex justify-end">
                    <div>
                        <button className="text-lg" onClick={this.logout}>登出</button>
                    </div>
                </div>
            </div>
        )
        return main
    }
}

class Main extends React.Component{
    constructor(props){
        super(props)
        this.state={
            changing : false,
            showing : "0px"
        }
        this.get_maincontent = this.get_maincontent.bind(this)
        this.change_Info = this.change_Info.bind(this)
    }

    get_maincontent(){
        if(this.state.showing=="0px"){
            const html = [<OverView_problem position={""} num_of_problem={this.state.problem_number} onclick={(i)=>this.change_Info(i)}></OverView_problem> ]
            return html
        }
        else if(this.state.showing == "110px"){
            const html = <Problem_List num_of_problem={this.state.problem_number} ></Problem_List>
            return html
        }
    }

    change_Info(i){
        const translate_pos ={
            "OverView" :  "0px",
            "Problem" :   "110px"
        }
        this.setState({
            showing : translate_pos[i]
        })
    }
    
    render(){
        let page = [
            <ToolBar></ToolBar>,
            <div className="p-10 main-page">
                <Introduce/>
                <div className="ml-96">
                    <Info_selecter onclick={(i)=>{this.change_Info(i)}} pos={this.state.showing} ></Info_selecter>
                    <div className="p-10 container flex flex-col">   
                        {this.get_maincontent()}
                    </div>
                </div>
            </div>
        ]
        return page
    }
}



const root = ReactDOM.createRoot(document.getElementById("main"))
root.render(<Main></Main>)