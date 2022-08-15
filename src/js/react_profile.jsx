class Inputbox extends React.Component{
    constructor(pro){
        super(pro)
        this.state={
            key : "",
            value : ""
        }
        this.onchange = this.onchange.bind(this)
        this.update = this.update.bind(this)
    }

    componentDidMount(){
        this.setState({
            title : this.props.title,
            value : this.props.value
        })
        this.props.new(this.props.title,this.props.value)
    }

    onchange(event){
        this.setState({
            value : event.target.value
        })
    }

    update(){
        this.props.new(this.state.title,this.state.value)
    }
    render(){
        var type;
        if(this.state.title == "about_me"){
            type = <textarea cols="30" rows="5" value={this.state.value} onChange={this.onchange} onBlur={this.update}></textarea>
        }
        else{
            type = <input type="text" value={this.state.value} onChange={this.onchange} onBlur={this.update}/>
        }
        var main=[
            <div>
                <p>{this.state.title}</p>
            </div>,
            <div className="w-full">
                {type}
            </div>
        ]
        return main
    }
} 

class Subtitle extends React.Component{
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
            changing : false,
            input_tmp : {}
        }
        this.render_subtitles = this.render_subtitles.bind(this)
        this.changing = this.changing.bind(this)
        this.render_input = this.render_input.bind(this)
        this.update = this.update.bind(this)
    }

    get_user_data(){
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

    componentDidMount(){
        this.get_user_data()
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

    render_input(){
        resp =[<Inputbox title={"handel"} value={this.state.handle} new={(i,j)=>this.new_input(i,j)}></Inputbox>]
        const sub_datas =  Object.entries(this.state.sub_data)
        sub_datas.forEach(element=>{
            resp.push(<Inputbox title={element[0]} value={element[1]} new={(i,j)=>this.new_input(i,j)}></Inputbox>)  
        })
        return resp
    }

    new_input(i,j){
        var temp =this.state.input_tmp
        temp[i] = j
        this.setState({
            input_tmp : temp
        })
    }

    changing(){
        this.setState({
            changing : !this.state.changing
        })
    }

    update(){
        fetch("#",
            {method : "PUT",
            body : JSON.stringify(this.state.input_tmp),
            headers: new Headers({
                'Content-Type': 'application/json'
              })}
              ).then(res => res.json())
        .then((respons)=>{
            if(respons.status == "OK"){
                this.get_user_data()
            }
        });
        this.changing()
    }

    render(){
        let pos = "container g-15 p-40 flex flex-col profile-area absolute"
        var main_showing;
        if(this.state.changing){
            main_showing=[
                <this.render_input></this.render_input>,
                <div className="flex w-full">
                    <button className="large-btu-bg w-full" onClick={()=>{this.update()}}>確認修改</button>
                </div>,
                <div className="flex w-full">
                    <button className="large-btu-bg w-full" onClick={()=>this.changing()}>取消</button>
                </div>
            ]
        }
        else{
            main_showing=[
                <div className="w-full flex flex-col">
                    <p className="text-size-small font-mono">{this.state.accountType}</p>
                    <p className="text-size-large font-mono ">{this.state.handle}</p>
                </div>,
                <this.render_subtitles></this.render_subtitles>,
                <div className="flex w-full">
                    <button className="large-btu-bg w-full" onClick={()=>this.changing()}>修改個人資料</button>
                </div>
            ]
        }
        let context = (
            <div className={pos}>
                <div className="m-auto">
                    <div className="profile-picture-container" >
                        <img className="main-img" src="/static/logo-black.svg" alt=""/>
                    </div>
                </div>
                {main_showing}
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

        if(this.props.mode = true){
            return main
        }
        else{

        }
    }
}

class Problem_List extends React.Component{
    constructor(prop){
        super(prop)
        this.state={
            num_per_page : 10,
            showing : 1,
            problems : [],
            num_of_problem : 0
        }

        this.topage = this.topage.bind(this)
        this.get_problem_list = this.get_problem_list.bind(this)
    }

    getProblems(i,j){
        fetch("/problem_list?"+new URLSearchParams({numbers:i,from:j})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : this.state.problems.concat(list)
            })
        })
    }

    getMoerProblems(i){
        const from = this.state.problems.length
        this.getProblems(i,from)
    }

    componentDidMount(){
        this.getProblems(20,0)
    }

    topage(i){
        if(i==this.state.showing) return
        var real_page=0
        var max = Math.ceil(this.props.num_of_problem / this.state.num_per_page)
        
        if(i>max){
            real_page = max
        }
        else if(i<1){
            real_page = 1
        }
        else{
            real_page = i
        }

        num_should_be = this.state.showing *this.state.num_per_page
        if(this.state.problems.length<num_should_be){
            const needed = num_should_be - this.state.problems.length +20
            this.getMoerProblems(needed)
        }
    }



    get_problem_list(){
        re=[]
        const from = (this.state.showing - 1)*this.state.num_of_problem
        const to = this.state.num_of_problem + from
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
            <div className="problem-overview-list">
                {re}
            </div>
        )
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

    render(){
        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problrm list</p>
                </div>
                <div className="">
                    <this.get_problem_list></this.get_problem_list>
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

        this.getProblems = this.getProblems.bind(this)
    }

    componentDidMount(){
        fetch("/problem_list?"+new URLSearchParams({numbers:4,from:0})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : list["data"]
            })
        })

        fetch("/problem_list_setting").then((res)=>{
            return res.json()
        }).then((data)=>{
            this.setState({
                problem_number : data["count"]
            })
        })
    }

    getProblems(){
        re=[]
        const max = this.state.problems.length
        for(var i= 0;i<4;i++){
            if(i>=max){
                break;
            }
            var element = this.state.problems[i]
            let info =
                <Problem_info key={element.problem_pid} problem_pid={element.problem_pid} title={element.title} permission={element.permission}></Problem_info>
            re.push(info)
        }

        var main=(
            <div className="problem-overview-list">
                {re}
            </div>
        )
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

    render(){
        var overflow_tag;
        if(this.props.num_of_problem>4){
            overflow_tag=(
                <a href="" className="text-align-end">...see more</a>
            )
        }
        else{
            overflow_tag = ""
        }

        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problrm list</p>
                </div>
                <div className="">
                    <this.getProblems></this.getProblems>
                </div>
                <div className="flex justify-content-end">
                    {overflow_tag}
                </div>
            </div>  
        )
        return main
    }
}

class Tool_bar extends React.Component{
    render(){
        let main = (
            <div className="items-center container g-20 tool_bar">
                <div className="flex g-20 w-80 align-items-center">
                    <div className="h-50">
                        <a href="/"><img width={100} src="/static/logo-black.svg"/></a>
                    </div>
                    <a href="/problem" ><p className="text-size-normal">題目</p></a>
                    <a href="/about" ><p className="text-size-normal">關於</p></a>
                    <a href="/status" ><p className="text-size-normal">狀態</p></a>
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

class Info_selecter extends React.Component{
    render(){

        var indecater_class = "page-info flex page-info-indecater "+this.props.pos
        var main = [
            <div className="flex g-10 m-b-10 page-info-title">
                <button className="page-info-btn">
                    <img src="/static/house.svg" alt="" />
                </button>
                <div className="page-info">
                    <button onClick={()=>this.props.onclick("OverView")} className="page-info-btn">OverView</button>
                </div>
                <div className="page-info">
                    <button onClick={()=>this.props.onclick("Problem")} className="page-info-btn">Problems</button>
                </div>
                <div className={indecater_class}>
                    <p>&lt;</p>
                    <p>&gt;</p>
                </div>
            </div>,
            <hr/>
        ]
        return main
    }
}

class Main extends React.Component{
    constructor(props){
        super(props)
        this.state={
            changing : false,
            showing : "OverView",
            problem_number : 0
        }

        this.MainContent = this.MainContent.bind(this)
    }

    componentDidMount(){
        fetch("/problem_list_setting").then((res)=>{
            return res.json()
        }).then((data)=>{
            this.setState({
                problem_number : data["count"]
            })
        })
        this.MainContent = this.MainContent.bind(this)
        this.change_Info = this.change_Info.bind(this)
    }

    MainContent(){
        if(this.state.showing=="OverView"){
            const html = [
                <OverView_problem position={""} num_of_problem={this.state.problem_number}></OverView_problem>
            ]
            return html
        }
        else if(this.state.showing == "Problem"){
            const html = <Problem_List></Problem_List>
            return html
        
        }
    }

    change_Info(i){
        this.setState({
            showing : i
        })
    }
    
    render(){

        var translate_pos ={
            "OverView" :  "info-first",
            "Problem" :  "info-second"
        }

        var main=[<Tool_bar></Tool_bar>]
        let page = (
            <div className="p-40 main-page">
                <Introduce position={""}/>
                <div className="main-content">
                    <Info_selecter onclick={(i)=>{this.change_Info(i)}} pos={translate_pos[this.state.showing]} ></Info_selecter>
                    <div className="p-40 container flex flex-col">   
                        <this.MainContent></this.MainContent>
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