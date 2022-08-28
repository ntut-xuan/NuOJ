function StatusRender(props){
    switch(props.value){
        case "AC":
            return <p className="border-2 p-3 w-full text-center text-xl font-mono text-bold text-green-600 border-green-600"> Accepted </p>
        case "WA":
            return <p className="border-2 p-3 w-full text-center text-xl font-mono text-bold text-red-600 border-red-600]"> Wrong Answer </p>
        case "TLE":
            return <p className="border-2 p-3 w-full text-center text-xl font-mono text-bold text-red-600 border-red-600"> Time Limit Exceeded </p>
        case "MLE":
            return <p className="border-2 p-3 w-full text-center text-xl font-mono text-bold text-red-600 border-red-600"> Memory Limit Exceeded </p>
    }
}

function CompileResultRender(props){
    switch(props.value){
        case "":
            return <p className="border-2 p-3 w-full text-center text-lg font-mono text-bold text-gray-600 border-gray-600"> Compile Status: Unknown </p>
        case "OK":
            return <p className="border-2 p-3 w-full text-center text-lg font-mono text-bold text-green-600 border-green-600"> Compile Status: OK </p>
        case "Failed":
            return <p className="border-2 p-3 w-full text-center text-lg font-mono text-bold text-red-600 border-red-600"> Compile Status: Failed </p>
    }
}

class SolutionArea extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            solution_data: props.solution_data,
            delete_data: props.delete_data
        }
        this.expend = this.expend.bind(this)
    }
    expend(ID){
        if($("#solution_area_" + ID).hasClass("h-0")){
            $("#solution_area_" + ID).removeClass("h-0");
            $("#solution_area_" + ID).addClass("h-[40vh]");
        }else{
            $("#solution_area_" + ID).removeClass("h-[40vh]");
            $("#solution_area_" + ID).addClass("h-0");
        }
    }
    render(){
        let {solution_data, delete_data} = this.state
        if(solution_data.length == 0){
            return (
                <div id="no_solution_current" class="p-5 border-2 rounded-lg">
                    <p class="text-center" > 目前還沒有解答，點擊下方「新增解答」按鈕來新增一個解答 </p>
                </div>
            )
        }else{
            let component_list = []
            for(let i = 0; i < solution_data.length; i++){
                let component = (
                    <div id="card" class="p-5 border-2 rounded-lg">
                        <p id={"card_" + (i+1)} value={(i+1)} class="text-center py-5 cursor-pointer hover:bg-gray-200" onClick={() => {this.expend(i+1)}}> 解答 {(i+1)} </p>
                        <div id={"solution_area_" + (i+1)} class="h-0 overflow-hidden transition-all duration-500 flex flex-row gap-5">
                            <div className="w-[80%]">
                                <textarea id={"code_area_" + (i+1)} class="resize-none w-full h-10" defaultValue={solution_data[i]["code"]} readonly></textarea>
                            </div>
                            <div className="w-[20%] flex flex-col gap-5">
                                <div className="flex flex-col justify-start h-full gap-3">
                                    <p className="border-2 p-3 w-full text-center text-xl font-mono text-bold">{solution_data[i]["uuid"].split("-")[4]}</p>
                                    <StatusRender value={solution_data[i]["status"]} />
                                    <CompileResultRender value={solution_data[i]["result"]} />
                                </div>
                                <div className="flex flex-col justify-end h-full">
                                    <button class="bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg" onClick={() => {delete_data(i)}}> 刪除 </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )
                component_list.push(component)
            }
            return component_list
        }
    }
}
class App extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            PID: window.location.pathname.split("/")[2],
            solution_editor: [],
            codearea_editor: null,
            solution_data: [],
        }
        this.cancel = this.cancel.bind(this)
        this.submit = this.submit.bind(this)
        this.add_problem = this.add_problem.bind(this)
        this.delete_data = this.delete_data.bind(this)
        this.compile_test = this.compile_test.bind(this)
    }
    cancel(){
        $("#dark").removeClass("h-screen")
        $("#dark").removeClass("bottom-0")
        $("#dark").addClass("h-0")
        $("#dark").addClass("bottom-[-100%]")
    }
    submit(){
        let {codearea_editor, solution_data} = this.state
        var code = codearea_editor.getValue();
        var status = document.getElementById("except_result").value
        solution_data.push({"code": code, "status": status, "uuid": uuid.v4(), "result": ""})
        this.cancel()
        codearea_editor.getDoc().setValue("")
        this.setState({solution_data: solution_data})
    }
    compile_test(){
        let {PID, solution_data} = this.state
        let data = {"problem_pid": PID, "save_uuid": uuid.v4(), "data": solution_data}
        $.ajax({
            url: "/edit_problem/" + PID + "/solution_pre_compile",
            data: JSON.stringify(data),
            type: "POST",
            dataType: "json",
            contentType: "application/json",
            success(data, status, xhr){
                Swal2.fire({
                    title: "Please wait",
                    timer: 2000,
                    timerProgressBar: true,
                    didOpen: () => {
                        Swal.showLoading()
                    },
                    willClose: () => {
                        window.location.reload();
                    }
                })
            }
        })
    }
    add_problem(){
        let {solution_data} = this.state
        $("#add_problem_title").text("解答設定 #" + (solution_data.length + 1))
        $("#dark").removeClass("h-0")
        $("#dark").removeClass("bottom-[-100%]")
        $("#dark").addClass("bottom-0")
        $("#dark").addClass("h-screen")
    }
    componentDidMount(){
        let {codearea_editor, PID, solution_data} = this.state
        let setting = {
            lineNumbers: true,
            matchBrackets: true,
            mode: "text/x-c++src",
            theme: "darcula"
        }
        codearea_editor = CodeMirror.fromTextArea(document.getElementById("code_area"), setting);
        codearea_editor.setSize("100%", "100%")

        $.ajax({
            url: "/fetch_solutions/" + PID,
            type: "GET",
            success: function(data, status, xhr){
                if(data["status"] == "OK"){
                    for(let i = 0; i < data["data"].length; i++){
                        solution_data_element = data["data"][i]
                        solution_data.push({"code": solution_data_element["code"], "status": "AC", "result": solution_data_element["result"], "uuid": solution_data_element["uuid"]})
                    }
                    this.setState({solution_data: solution_data})
                }
                console.log("fetch")
            }.bind(this)
        })

        this.setState({codearea_editor: codearea_editor})
    }

    componentDidUpdate(){
        let {solution_data} = this.state
        let read_only_setting = {
            lineNumbers: true,
            matchBrackets: true,
            mode: "text/x-c++src",
            theme: "darcula",
            readOnly: true,
        }
        console.log(solution_data)
        for(let i = 0; i < solution_data.length; i++){
            if(document.getElementById("code_area_" + (i+1)).hasAttribute("style")){
                continue;
            }
            codearea_editor = CodeMirror.fromTextArea(document.getElementById("code_area_" + (i+1)), read_only_setting);
            codearea_editor.setSize("100%", "100%")
        }
    }
    delete_data(index){
        let {solution_data} = this.state
        solution_data.splice(index, 1)
        this.setState({solution_data: solution_data})
    }
    render(){
        let {PID, solution_data} = this.state
        return [
            <div class="z-20 flex flex-col">
                <AddProblemToolbar />
                <div class="relative w-[70%] mx-auto bg-white min-h-full flex">
                    <div class="w-full p-10">
                        <p class="font-bold text-5xl m-5 text-left"> 解答設定 </p>
                        <div className="border-2 p-5">
                            <SolutionArea delete_data={this.delete_data} solution_data={solution_data} />
                        </div>
                        <button class="bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg my-3" onClick={this.add_problem}> 新增解答 </button>
                        <button id="compile_button" class="enabled:bg-blue-500 disabled:bg-slate-400 text-white transition-colors duration-200 enabled:hover:bg-blue-400 w-full p-3 text-lg rounded-lg my-3" onClick={this.compile_test}> 編譯測試並存檔 </button>
                    </div>
                </div>
                <div class="w-full text-center py-10">
                    <p id="PID" class="italic text-gray-400"> {PID} </p>
                </div>
            </div>,
            <div id="dark" class="h-0 overflow-y-hidden absolute left-0 bottom-[-100%] transition-all duration-500 ease-in-out bg-opacity-50 bg-black w-screen z-50">
                <div class="absolute bg-white p-5 rounded-lg w-[70%] h-[80vh] left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%] flex flex-col">
                    <div className="w-full relative">
                        <p id="add_problem_title" class="font-bold text-5xl m-5 text-center"> </p>
                    </div>
                    <div className="w-full relative h-full flex flex-row gap-5 overflow-hidden">
                        <div className="w-[80%]">
                            <textarea id="code_area" className="resize-none h-20"></textarea>
                        </div>
                        <div id="option" className="w-[20%] flex flex-col gap-3">
                            <select id="except_result" className="w-full p-3 text-center border-2 rounded-lg">
                                <option value="AC"> 通過測試（AC） </option>
                                <option value="WA"> 無法通過測試（WA） </option>
                                <option value="TLE"> 超時（TLE） </option>
                                <option value="MLE"> 超過記憶體限制（MLE） </option>
                            </select>
                            <button class="bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg" onClick={this.submit}> 存檔 </button>
                            <button class="bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg" onClick={this.cancel}> 取消 </button>
                        </div>
                    </div>
                </div>
            </div>
        ]
    }
}

const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(<App />);