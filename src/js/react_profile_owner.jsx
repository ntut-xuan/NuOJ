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

// Profile 顯示範圍

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
        this.state={
            img : "",
            upload_img : false,
            img_type : null,
            img_data : null,
            sub : []
        }
        this.render_inputs = this.render_inputs.bind(this)
        this.setup_profile = this.setup_profile.bind(this)
        this.upload_profile = this.upload_profile.bind(this)
        this.trigger_image_upload = this.trigger_image_upload.bind(this)
    }

    componentDidMount(){
        const datas = this.props.datas
        this.setState({
            sub: {
                email : datas.email,
                school : datas.school,
                bio : datas.bio,
                
            },
            img : this.props.img
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

        // 先上傳圖片 

        if(this.state.upload_img){
            fetch("/upload_img",{
                method : "PUT",
                body : JSON.stringify({type : this.state.img_type,img : this.state.img}),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then((res)=>{ 
                if(res.status == 200){
                    return res.json() 
                }
                else{
                    error_swal("上傳圖片錯誤").then(()=>{ this.props.change(false) })
                }
            })
            .then((json)=>{
                const status = json.status
                if(status == "OK"){
                    this.setState({upload_img : false})
                }
                else{
                    error_swal("上傳圖片錯誤").then(()=>{ this.props.change(false) })
                    return
                }
            })
        }

        // 上傳個人資料 
        
        if(need_to_upload){
            fetch("#",{
                method : "PUT",
                body : JSON.stringify(this.state.sub),
                headers: new Headers({
                    'Content-Type': 'application/json'
                })
            }).then((res) => {
                return res.json()
            })
            .then((json)=>{
                const status = json.status;
                if(status == "OK"){
                    success_swal("上傳個人資料成功").then(()=>{ this.props.change(true) })
                }
                else{
                    error_swal("上傳個人資料錯誤").then(()=>{this.props.change(false)})
                }
            });
        }
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
                this.setState({
                    upload_img : true,
                    img : content,
                })
            }
        }
        file_input.click();
    }

    setup_profile(title,content){
        var temp = this.state.sub
        temp[title] = content
        this.setState({ sub : temp })
        // if(title=="email") this.setState({ email : content })
        // if(title=="school") this.setState({ school : content })
        // if(title=="bio") this.setState({ bio : content })
    }

    render_inputs(){
        resp =[]
        const sub_datas =  Object.entries(this.state.sub)
        sub_datas.forEach(element=>{
            resp.push(<Inputbox key={element[0]} title={element[0]} value={element[1]} update={(title,content)=>this.setup_profile(title,content)}></Inputbox>)  
        })
        return resp
    }

    render(){
        var main=(
            <div className="container gap-1 p-10 flex flex-col profile-area">
                <div className="m-auto">
                    <div className="profile-img-container" >
                        <button className="img-cover text-lg" onClick={this.trigger_image_upload}>修改圖片</button>
                        <img id="user_avater" className="profile-img" src={this.state.img}/>
                    </div>
                </div>
                <this.render_inputs></this.render_inputs>
                <div className="flex w-full">
                    <button className="bg-cyan-700/50 w-full" onClick={()=>{this.upload_profile()}}>確認修改</button>
                </div>
                <div className="flex w-full">
                    <button className="bg-neutral-400/50 w-full" onClick={()=>{this.props.change(false)}}>取消</button>
                </div>
            </div>
        )
        return main
    }
} 

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
                <div className="flex">
                    <button className="w-full bg-cyan-700/50" onClick={()=>this.props.change()}>修改個人資料</button>
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
            mode : false
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

        fetch("/get_profile/"+handle).then((res)=>{
            return res.json()
        }).then((json)=>{
            const status = json.status;
            if( status == "OK"){
                this.setState({profile_data : json.data})
            }
            else{
                error_swal("請先登入").then(() => {window.location.href = "/" })
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
        if(this.state.changing){
            return (<UpdateProfileInterface datas={subtitles} img = {maintitles.img} change={(i)=>this.change_mode(i)} update={(i)=>this.update_profile(i)}></UpdateProfileInterface>)
        }
        else{
            return (<Subtitle subtitles={subtitles} maintitles={maintitles} change={()=>this.change_mode()}></Subtitle>)
        }
    }
}

// 主要顯示範圍

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
        fetch("/get_user_problem_number").then((res)=>{
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

        fetch("/profile_problem_list?"+new URLSearchParams({mode:num_per_page,page:showing})).then((res)=>{
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
                <p className="problem-notification p-10"> You didn't released any problem yet</p>
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

// 概覽範圍
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
        fetch("/profile_problem_list?"+new URLSearchParams({mode:4,page:1})).then((res)=>{
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
                <p className="problem-notification p-10"> You didn't released any problem yet</p>
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

// 其他

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