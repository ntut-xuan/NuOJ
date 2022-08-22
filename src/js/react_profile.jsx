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
    }

    onchange(event){
        this.setState({value : event.target.value})
    }

    update(){
        this.props.update(this.state.title,this.state.value)
    }

    render(){
        var type;
        if(this.state.title == "bio"){
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

class UpdateProfileInterface extends React.Component{
    constructor(props){
        super(props)
        this.state={}
        this.render_inputs = this.render_inputs.bind(this)
        this.setup_profile = this.setup_profile.bind(this)
        this.upload_profile = this.upload_profile.bind(this)
    }

    componentDidMount(){
        const datas = this.props.datas
        this.setState({
            email : datas.email,
            school : datas.school,
            bio : datas.bio
        })
    }

    upload_profile(){

        var need_to_upload = false;

        var keys = Object.keys(this.state)
        for(var i=0;i<keys.length;i++){
            if(this.state[keys[i]] != this.props.datas[keys[i]]){
                need_to_upload = true
                break;
            }
        }

        if(need_to_upload){
            fetch("#",{
                method : "PUT",
                body : JSON.stringify(this.state),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then(res => res.json())
            .then((respons)=>{
                if(respons.status == "OK"){
                }
            });
            this.props.change(1)
            this.props.update(this.state)
        }
        else{
            this.props.change(0)
        }
    }

    setup_profile(title,content){
        if(title=="email") this.setState({ email : content })
        if(title=="school") this.setState({ school : content })
        if(title=="bio") this.setState({ bio : content })
    }

    render_inputs(){
        resp =[]
        const sub_datas =  Object.entries(this.state)
        sub_datas.forEach(element=>{
            resp.push(<Inputbox title={element[0]} value={element[1]} update={(title,content)=>this.setup_profile(title,content)}></Inputbox>)  
        })
        return resp
    }

    render(){
        var main=[
            <this.render_inputs></this.render_inputs>,
            <div className="flex w-full">
                <button className="large-btu-bg w-full" onClick={()=>{this.upload_profile()}}>確認修改</button>
            </div>,
            <div className="flex w-full">
                <button className="large-btu-bg w-full" onClick={()=>{this.props.change(0)}}>取消</button>
            </div>
        ]
        return main
    }
} 

class Subtitle extends React.Component{
    get_titles(titles){
        const datas =  Object.values(titles)
        resp =[]
        datas.forEach(element=>{
            if(element!="")
                resp.push(
                    <div className="over-flow-text">
                        <p className="text-size-small text-little_gray break-words">{element}</p>
                    </div>
                ) 
        })
        return resp
    }
    render(){
        var maintitles = this.props.maintitles
        var main = [
            <div className="w-full flex flex-col">
                <p className="text-size-small font-mono">{maintitles.accountType}</p>
                <p className="text-size-large font-mono ">{maintitles.handle}</p>
            </div>,
            <div className="flex flex-col">
                {this.get_titles(this.props.subtitles)}
            </div>,
            <div className="flex">
                <button className="large-btu-bg w-full" onClick={()=>this.props.change(0)}>修改個人資料</button>
            </div>
        ]

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
            mode : false,
            upload_img : false,
            img_type : null,
            img_data : null
        }
        this.changing_mode = this.change_mode.bind(this)
        this.get_profile = this.get_profile.bind(this)
        this.upload_img = this.upload_img.bind(this)
        this.update_profile = this.update_profile.bind(this)
        this.trigger_image_upload = this.trigger_image_upload.bind(this)
    }

    componentDidMount(){
        this.get_profile()
    }

    get_profile(){
        fetch("/get_profile").then((res)=>{
            return res.json()
        }).then((json)=>{
            console.log(this.state.profile_data)
            console.log(json)
            this.setState({
                profile_data : json
            })
        })
        
    }
    
    update_profile(i){
        var temp = this.state.profile_data
        temp.sub = i
        this.setState({
            profile_data : temp
        })
    }

    upload_img(){
        if(this.state.upload_img){
            fetch("/upload_img",{
                method : "PUT",
                body : JSON.stringify({type : this.state.img_type,img : this.state.img_data}),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then(res => res.json())
            .then((respons)=>{
                if(respons.status == "OK"){

                }
            })
        }

        this.setState({upload_img : false})
    }

    trigger_image_upload(){
        let file_input = document.createElement("input")
        file_input.type = "file"
        file_input.accept = "image/*"
        file_input.onchange = e => {
            var image = e.target.files[0];
            var reader = new FileReader();
            reader.readAsDataURL(image)

            this.setState({img_type : image.type.slice(6)})

            reader.onload = readerEvent => {
                var content = readerEvent.target.result;
                // document.getElementById("user_avater").setAttribute("src", content)
                var temp = this.state.profile_data
                temp.main.img = content
                this.setState({
                    upload_img : true,
                    img_data : content,
                    profile_data : temp
                })
            }
        }
        file_input.click();
    }

    change_mode(i){
        if(i==1){
            this.upload_img()
        }
        this.setState({
            changing : !this.state.changing
        })
    }

    render(){
        var subtitles = this.state.profile_data.sub
        var maintitles = this.state.profile_data.main
        var main_showing;
        var img_area;
        if(this.state.changing){
            main_showing=(<UpdateProfileInterface datas={subtitles} change={(i)=>this.change_mode(i)} update={(i)=>this.update_profile(i)}></UpdateProfileInterface>)
            img_area = (<button className="img-cover text-size-normal" onClick={this.trigger_image_upload}>修改圖片</button>)
        }
        else
            main_showing = (<Subtitle subtitles={subtitles} maintitles={maintitles} change={(i)=>this.change_mode(i)}></Subtitle>)
    
        let context = (
            <div className="container g-15 p-40 flex flex-col profile-area absolute">
                <div className="m-auto">
                    <div className="profile-img-container" >
                        {img_area}
                        <img id="user_avater" className="profile-img" src={maintitles.img}/>
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
            problems : []
        }

        this.topage = this.topage.bind(this)
        this.get_problem_list = this.get_problem_list.bind(this)
    }

    getProblems(i,j){
        fetch("/profile_problem_list?"+new URLSearchParams({numbers:i,from:j})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : this.state.problems.concat(list.data)
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
        var real_page;
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
        if(this.props.num_of_problem==0){
            var None_problems=(
                <p className="problem-notification p-40"> You didn't released any problem yet</p>
            )
            return None_problems
        }
        re=[]
        const from = (this.state.showing - 1)*this.state.num_per_page
        const to = this.state.num_per_page + from
        const max = this.state.problems.length
        for(var i= from;i<to;i++){
            if(i>=max){
                break;
            }
            var element = this.state.problems[i]
            let info =
                <Problem_info key={element.problem_pid} problem_pid={element.problem_pid} title={element.title} permission={element.permission}  mode={false}></Problem_info>
            re.push(info)
        }

        return re
        
    }

    render(){
        let main=(
            <div>
                <div className="m-b-10">
                    <p>Problrm list</p>
                </div>
                <div className="flex flex-col">
                    <this.get_problem_list ></this.get_problem_list>
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
        fetch("/profile_problem_list?"+new URLSearchParams({numbers:4,from:0})).then((res)=>{
            return res.json()
        }).then((list)=>{
            this.setState({
                problems : list["data"]
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
                <Problem_info key={element.problem_pid} problem_pid={element.problem_pid} title={element.title} permission={element.permission} mode={true}></Problem_info>
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
                <button onClick={()=>this.props.onclick("Problem")}>...see more</button>
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

class ToolBar extends React.Component{
    constructor(prop){
        super(prop)
    }
    logout(){
        fetch("/logout").then((res)=>{ return res.json()}).then((resp)=>{if(resp.status == "OK"){ window.location.href = "/" }})
    }
    render(){
        let main = (
            <div className="items-center flex g-20 tool_bar">
                <div className="flex g-40 w-80 align-items-center">
                    <div className="h-50">
                        <a href="/"><img width={100} src="/static/logo-black.svg"/></a>
                    </div>
                    <a href="/problem" ><p className="text-size-normal">題目</p></a>
                    <a href="/about" ><p className="text-size-normal">關於</p></a>
                    <a href="/status" ><p className="text-size-normal">狀態</p></a>
                </div>
                <div className="w-20 flex justify-end">
                    <div>
                        <button className="text-size-normal" onClick={this.logout}>登出</button>
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
                <button className="page-info-btn" onClick={()=>this.props.onclick("OverView")}>
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
        this.get_maincontent = this.get_maincontent.bind(this)
        this.change_Info = this.change_Info.bind(this)
    }

    componentDidMount(){
        fetch("/profile_problem_setting").then((res)=>{
            return res.json()
        }).then((data)=>{
            this.setState({
                problem_number : data["count"]
            })
        })
    }

    get_maincontent(){
        if(this.state.showing=="OverView"){
            const html = [
                <OverView_problem position={""} num_of_problem={this.state.problem_number} onclick={(i)=>this.change_Info(i)}></OverView_problem>
            ]
            return html
        }
        else if(this.state.showing == "Problem"){
            const html = <Problem_List num_of_problem={this.state.problem_number} ></Problem_List>
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
        let page = [
            <ToolBar></ToolBar>,
            <div className="p-40 main-page">
                <Introduce position={""}/>
                <div className="main-content">
                    <Info_selecter onclick={(i)=>{this.change_Info(i)}} pos={translate_pos[this.state.showing]} ></Info_selecter>
                    <div className="p-40 container flex flex-col">   
                        <this.get_maincontent></this.get_maincontent>
                    </div>
                </div>
            </div>
        ]
        return page
    }
}


const root = ReactDOM.createRoot(document.getElementById("main"))
root.render(<Main></Main>)