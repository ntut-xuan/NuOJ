class Subtitle extends React.Component{
    constructor(props){
        super(props)
        this.state={
            title : "",
            content : ""
        }
    }

    componentDidMount(){
        this.setState({
            title : this.props.data.title,
            content : this.props.data.content
        })
    }

    render(){
        let main=(
            <div className="w-full flex flex-col">
                <p className="subtitle text-size-normal">{this.state.title}</p>
                <div className="flex">
                    <div className="w-80">
                        <p>{this.state.content}</p>
                    </div>
                    <div className="flex justify-end w-20" >
                        <button className="little-btu-bg" >修改</button>
                    </div>
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
            accountType:"使用者",
            handle:"0000",
            email : "pony076152340@gmail.com",
            about_me : ""
        }
    }
    render(){
        let {accountType,handle,email,about_me} = this.state
        let pos = "container g-40 flex flex-col middel main-interface "+this.props.position
        let context = (
            <div className={pos}>
                <div className="w-full flex">
                    <div className="w-33 flex flex-col g-10">
                        <div className="profile-picture-container" >
                            <img  className="main-img" src="/static/logo-black.svg" alt=""/>
                        </div>
                        <div>
                            <div className="flex justify-center w-full">
                                <button className="large-btu-bg">修改個人資料</button>
                            </div>
                        </div>
                    </div>
                    <div className="w-full flex justify-center flex-col items-center">
                        <p className="text-size-q font-mono"> {accountType} </p>
                        <p className="text-size-large font-mono ">{handle}</p>
                    </div>
                </div>
                <Subtitle data={{title:"電子信箱", content : email}}></Subtitle>
            </div>
        )
        return context
    }
}

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
    constructor(props){
        super(props)
        this.state={
            problem_pid : "",
            title : "",
            permission : 0
        }
    }

    componentDidMount(){
        this.setState({
            problem_pid : this.props.problem_pid,
            title : this.props.title,
            permission : this.props.permission
        })
    }

    Status(permission) {
        let T=[
            <div className="problem-status bg-green"> </div>
            ,<p>公開</p>
        ]

        let F=[
            <div className="problem-status bg-red"> </div>,
            <p>未公開</p> 
        ]
        if(permission.value==1){
            return T
        }
        else{
            return F
        }
    }

    render(){
        let url ="/edit/"+this.state.problem_pid
        let main=(
            <a href={url}>
                <div className="problem-container">
                    <div className="flex g-10 align-items-center">
                        <this.Status value={this.state.permission}></this.Status>
                    </div>
                    <hr/>
                    <p className="text-size-normal">{this.state.title}</p>
                </div>
            </a>
        )
        return main
    }
}

class Problem_list extends React.Component {
    constructor(props){
        super(props)
        this.state={
            problem_number : 0,
            number_per_page : 4,
            page_now : 1,
            problems : []
        }

        this.getProblems = this.getProblems.bind(this)
        this.topage = this.topage.bind(this)
    }

    componentDidMount(){
        fetch("/problem_list?"+new URLSearchParams({numbers:50,from:0})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : list["data"]
            })
        })

        fetch("/problem_list_setting").then((res)=>{
            return res.json()
        }).then((data)=>{
            console.log(data["count"])
            this.setState({
                problem_number : data["count"]
            })
        })
    }

    getProblems(){
        result=[]
        const from = this.state.number_per_page * (this.state.page_now -1)
        const to = this.state.number_per_page + from
        const max = this.state.problems.length
        for(var i= from;i<to;i++){
            if(i>=max){
                break;
            }
            var element = this.state.problems[i]
            let info =
                <Problem_info key={element.problem_pid} problem_pid={element.problem_pid} title={element.title} permission={element.permission}></Problem_info>
            result.push(info)
        }
        return result
    }

    topage(i){
        if(this.state.page_now == i) return
        this.setState({
            page_now : i
        })
    }

    render(){
        const max = Math.ceil(this.state.problem_number / this.state.number_per_page)

        let pos = "container flex-col middel main-interface problem-list "+this.props.position
        let main=(
            <div className={pos} >
                <div className="flex g-15 flex-col">
                    <this.getProblems value={this.state.problems}></this.getProblems>
                </div>
                <PageSlecter topage={(i)=>{this.topage(i)}}  Lastpage={max}></PageSlecter>
            </div>
        )
        return main
    }
}

class Interface_slecter extends React.Component{
    render(){
        let main = (
            <div className="items-center container g-20 interface-selecter">
                <div className="flex g-20 w-80">
                    <a  href="/"><img  src="/static/logo-black.svg"/></a>
                    <button className="text-size-normal" onClick={()=>this.props.onclick(0)}>個人資料</button>
                    <button className="text-size-normal" onClick={()=>this.props.onclick(1)}>題目</button>
                </div>
                <div className="w-20 flex justify-end">
                    <div>
                        <button className="text-size-normal">登出</button>
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
            now_showing: 0
        }
    }

    componentDidMount(){
        
    }
    
    changePage(selected){
        this.setState({
            now_showing : selected
        })
    }

    render(){
        var main=[<Interface_slecter onclick={(i)=>this.changePage(i)}/>]
        if(this.state.now_showing==0){
            main.push(<Introduce position={""}/>)
            main.push(<Problem_list position={"l-150"}/>)
        }
        else{
            main.push(<Introduce position={"l-150"}/>)
            main.push(<Problem_list position={""}/>)
        }
        return main
    }
}


const root = ReactDOM.createRoot(document.getElementById("main"))
root.render(<Main></Main>)