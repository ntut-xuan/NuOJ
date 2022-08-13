class Subtitle extends React.Component{
    constructor(props){
        super(props)
    }
    render(){
        let main=(
            <div className="flex">
                <div className="w-full">
                    <p className="text-size-small text-little_gray">{this.props.content}</p>
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
            accountType : null,
            handle : null,
            sub_data: {},
            changing : false
        }
        this.render_subtitles = this.render_subtitles.bind(this)
    }

    componentDidMount(){
        fetch("/get_user").then((res)=>{
            return res.json()
        }).then((json)=>{
            this.setState({
                accountType : json.main.accountType,
                handle : json.main.handle,
                sub_data : json.sub
            })
        })
    }

    render_subtitles(){
        const sub_datas =  Object.entries(this.state.sub_data)
        resp =[]
        sub_datas.forEach(element=>{
            if(element[1]!="")
                resp.push(<Subtitle key={element[0]} title={element[0]} content={element[1]} mode={this.state.changing}></Subtitle>)  
        })
        return resp
    }
    render(){
        let pos = "container g-15 p-40 flex flex-col profile-page absolute"+this.props.position
        let context = (
            <div className={pos}>
                <div className="m-auto">
                    <div className="profile-picture-container" >
                        <img className="main-img" src="/static/logo-black.svg" alt=""/>
                    </div>
                </div>
                <div className="w-full flex flex-col">
                    <p className="text-size-small font-mono">{this.state.accountType}</p>
                    <p className="text-size-large font-mono ">{this.state.handle}</p>
                </div>
                <this.render_subtitles></this.render_subtitles>
                <div className="flex w-full">
                    <button className="large-btu-bg w-full">修改個人資料</button>
                </div>
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
    render(){
        var status;
        if(this.props.permission == true){
            status=<p>公開</p>
        }
        else{
            status=<p>未公開</p>
        }
        let url ="/edit/"+this.props.problem_pid
        let main=(
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
        re=[]
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
            re.push(info)
        }

        var main=(
            <div className="problem-list">
                {re}
            </div>
        )

        console.log(re.length)
        if(re.length==0){
            var None_problems=(
                <p className="problem-notification p-40"> You didn't released any problem yet</p>
            )
            return None_problems
        }
        else{
            return main
        }
    }

    topage(i){
        if(this.state.page_now == i) return
        this.setState({
            page_now : i
        })
    }

    render(){
        var max = Math.ceil(this.state.problem_number / this.state.number_per_page)
        if(max == 0){
            max =1
        }
        let pos = "container flex-col problem-list p-40 "+this.props.position
        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problrm list</p>
                </div>
                <div className="">
                    <this.getProblems></this.getProblems>
                </div>
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
                    <div className="h-50">
                        <a href="/"><img width={100}src="/static/logo-black.svg"/></a>
                    </div>
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
            now_showing: 0,
            changing : false
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
        let page = (
            <div className="p-40 main-page">
                <Introduce position={""}/>
                <div className="main-interface">
                    <div className="p-40 container flex flex-col">   
                        <Problem_list position={""}></Problem_list>
                    </div>
                </div>
            </div>
        )
        main.push(page)
        return main
    }
}


const root = ReactDOM.createRoot(document.getElementById("main"))
root.render(<Main></Main>)