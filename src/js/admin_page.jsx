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

class Main extends React.Component{
    constructor(props){
        super(props)
        this.state={
            changing : false,
            showing : "OverView",
            problem_number : 0
        }
    }
    
    render(){
        var translate_pos ={
            "OverView" :  "info-first",
            "Problem" :  "info-second"
        }
        let page = [
            <ToolBar></ToolBar>
        ]
        return page
    }
}

const root = ReactDOM.createRoot(document.getElementById("main"))
root.render(<Main></Main>)