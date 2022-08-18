class Testcase_Component extends React.Component{
    constructor(props){
        super(props);
        this.state = {testcase: props.testcase, trigger_event_list: {}}
        this.componentClose = this.componentClose.bind(this)
    }
    componentClose(name){
        console.log("trigger")
        if(document.getElementById(name).classList.contains("h-0")){
            document.getElementById(name).classList.remove("h-0")
            document.getElementById(name).classList.add("h-[19vh]")
        }else{
            document.getElementById(name).classList.remove("h-[19vh]")
            document.getElementById(name).classList.add("h-0")
        }
    }
    componentDidUpdate(){
        let {testcase, trigger_event_list} = this.state;
        for(let i = 0; i < testcase.length; i++){
            document.getElementById("testcase-" + (i+1)).removeEventListener("click", trigger_event_list[i])
        }
        for(let i = 0; i < testcase.length; i++){
            let trigger = () => {this.componentClose("data-" + (i+1))}
            document.getElementById("testcase-" + (i+1)).addEventListener("click", trigger)
            trigger_event_list[i] = trigger
        }
    }
    render(){
        let {testcase} = this.state;
        if(testcase.length === 0){
            return (
                <div id="no_solution_current" class="my-5 p-5 border-2 rounded-lg">
                    <p class="text-center"> 目前還沒有測試資料，點擊下方「新增測試資料」按鈕來新增一個測試資料 </p>
                </div>
            )
        }else{
            testcase_component_list = []
            for(let i = 0; i < testcase.length; i++){
                let component = <div className="my-5 p-5 border-2 rounded-lg ">
                    <p id={"testcase-" + (i+1)} className="text-center text-lg hover:bg-slate-200 p-5 cursor-pointer"> 測試資料 {i+1} </p>
                    <div id={"data-" + (i+1)} className="w-full flex flex-row h-0 overflow-hidden transition-all duration-500">
                        <div className="w-[30%] p-5">
                            <textarea className="w-full h-[15vh] bg-slate-200 resize-none p-5 font-mono" value={testcase[i]["input"]} readOnly></textarea>
                        </div>
                        <div className="w-[30%] p-5">
                        <textarea className="w-full h-[15vh] bg-slate-200 resize-none p-5 font-mono" value={testcase[i]["output"]} readOnly></textarea>
                        </div>
                        <div className="w-[40%] p-5 flex flex-col gap-5 justify-center relative">
                            <button class="bg-orange-500 text-white transition-colors duration-200 hover:bg-orange-400 w-full p-3 text-lg rounded-lg"> 修改測試資料 </button>
                            <button class="bg-red-500 text-white transition-colors duration-200 hover:bg-red-400 w-full p-3 text-lg rounded-lg"> 刪除測試資料 </button>
                        </div>
                    </div>
                </div>
                testcase_component_list.push(component)
            }
            return testcase_component_list
        }
    }
}

class App extends React.Component {
    constructor(props){
        super(props);
        this.state = {testcase: []}
        this.add_test_case = this.add_test_case.bind(this);
        this.save_test_case = this.save_test_case.bind(this);
        this.upload_test_case = this.upload_test_case.bind(this);
    }
    add_test_case(){
        document.getElementById("add_testcase_platform").classList.remove("top-[100%]");
        document.getElementById("add_testcase_platform").classList.add("top-0");
    }
    save_test_case(){
        let {testcase} = this.state
        // Get Testcase
        let input = document.getElementById("testcase").value
        let output = document.getElementById("answer").value
        testcase.push({"input": input, "output": output})
        this.setState({testcase: testcase})
        // Clean Testcase
        document.getElementById("testcase").value = ""
        document.getElementById("answer").value = ""
        // Finish Save Testcase
        document.getElementById("add_testcase_platform").classList.add("top-[100%]");
        document.getElementById("add_testcase_platform").classList.remove("top-0");
    }
    upload_test_case(){
        let file_input = document.createElement("input")
        file_input.type = "file"
        file_input.accept = "application/json"
        file_input.onchange = e => {
            let file = file_input.files[0]
            Swal.fire({
                icon: "info",
                title: "接收到測試資料檔案",
                text: "大小：" + file.size + " KB",
                confirmButtonText: "上傳"
            }).then((result) => {
                if(result.isConfirmed) {
                    let start = 0;
                    let step = 1024 * 1024 * 2;
                    let count = 0;
                    Swal.fire({
                        title: "讀取資料中...",
                        didOpen: () => {
                            Swal.showLoading()
                            const promise = new Promise((resolve) => {
                                let reader = new FileReader()
                                reader.onload = () => {
                                    resolve(reader.result)
                                }
                                reader.readAsArrayBuffer(file)
                            })
                            promise.then((data) => {
                                for(let i = 0; i <= file.size / step; i++){
                                    let array_buffer = new Int8Array(data.slice(start, Math.min(start + step, file.size)))
                                    $.ajax({
                                        url: "/file_test/upload",
                                        type: "POST",
                                        data: JSON.stringify({"hash": SparkMD5.ArrayBuffer.hash(array_buffer), "data": Array.from(array_buffer)}),
                                        dataType: "json",
                                        contentType: "application/json",
                                        success: function(data){
                                            count += 1;
                                            Swal.getTitle().textContent = "上傳中（" + count + "/" + Math.ceil(file.size / step) + "）"
                                            if(count == Math.ceil(file.size / step)){
                                                Swal.fire({
                                                    icon: "success",
                                                    title: "上傳成功",
                                                    timer: 2000,
                                                    showConfirmButton: false
                                                })
                                            }
                                        },
                                        error: function(xhr, status, trown){
                                            Swal.fire({
                                                icon: "error",
                                                title: "上傳失敗，請再次重新上傳",
                                                timer: 2000,
                                                showConfirmButton: false
                                            })
                                        }
                                    })
                                    start += step;
                                }
                            })
                        }
                    });
                }
            })
        }
        file_input.click();
    }
    render(){
        let {testcase} = this.state
        return [
            <div class="z-20 flex flex-col">
                <AddProblemToolbar />
            </div>,
            <div id="main_platform" class="relativ mx-auto w-[70%] bg-white h-screen flex">
                <div class="w-screen p-10">
                    <p class="font-bold text-5xl mt-5 text-left"> 測資設定 </p>
                    <div id="testcase_area" className="max-h-[50vh] overflow-y-auto my-5 border-2 px-5">
                        <Testcase_Component testcase={testcase}/>
                    </div>
                    <div className="flex flex-col gap-5">
                        <div className="flex flex-row gap-5">
                            <button class="bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg" onClick={this.add_test_case}> 新增測試資料 </button>
                            <button class="bg-teal-500 text-white transition-colors duration-200 hover:bg-teal-400 w-full p-3 text-lg rounded-lg" onClick={this.add_test_case}> 上傳測試資料 </button>
                        </div>
                        <div className="flex flex-col gap-5">
                            <button class="bg-pink-500 transition-colors duration-200 w-full p-3 text-lg rounded-lg hover:bg-pink-400 text-white" onClick={this.upload_test_case}> 上傳測試資料壓縮檔 </button>
                            <button class="bg-gray-500 transition-colors duration-200 w-full p-3 text-lg rounded-lg text-gray-300" disabled> 利用測資產生器新增資料 </button>
                        </div>
                    </div>
                </div>
            </div>,
            <div id="add_testcase_platform" className="w-screen h-screen bg-black bg-opacity-50 absolute top-[100%] transition-all duration-500">
                <div className="absolute top-[50%] left-[50%] p-5 translate-x-[-50%] translate-y-[-50%] bg-white w-[50%] h-fit rounded-lg">
                    <p className="text-center text-2xl pb-5"> 新增測試資料 </p>
                    <div className="flex flex-row gap-5">
                        <div className="w-full h-fit border-2 rounded-xl p-5">
                            <p className="text-center text-xl pb-5"> 測試資料 </p>
                            <textarea id="testcase" className="bg-slate-200 h-[30vh] w-full resize-none font-mono text-lg p-5"></textarea>
                        </div>
                        <div className="w-full h-fit border-2 rounded-xl p-5">
                            <p className="text-center text-xl pb-5"> 解答 </p>
                            <textarea id="answer" className="bg-slate-200 h-[30vh] w-full resize-none font-mono text-lg p-5" placeholder="如果你想自動生成答案，請留空。"></textarea>
                        </div>
                    </div>
                    <button class="bg-amber-500 text-white transition-colors duration-200 hover:bg-amber-400 w-full p-3 text-lg rounded-lg mt-5" onClick={this.save_test_case}> 新增測試資料 </button>
                </div>
            </div>
        ]
    }
}

const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(<App />);