function LineBreakDescription(props){
    let description = props.description
    let descriptions = description.split("\n");
    let descriptionObject = []
    for(let i = 0; i < descriptions.length; i++){
        let descriptionLine = <p id="description" class="py-1"> {descriptions[i]} </p>
        descriptionObject.push(descriptionLine)
    }
    return descriptionObject
}

class App extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            basic_setting: undefined,
            problem_content: undefined,
            complete_third_party_render: false
        }
        this.fecthProblemID = this.fecthProblemID.bind(this)
    }

    fecthProblemID(){
        let pathname = window.location.pathname;
        let problemID = pathname.split("/")[2];

        return problemID;
    }

    componentDidMount(){
        let problemID = this.fecthProblemID()
        $.ajax({
            url: "/api/problem/" + problemID,
            type: "GET",
            success: function(data, status, xhr){
                document.title = `NuOJ - ${data["content"]["title"]}`
                this.setState({
                    basic_setting: data["setting"],
                    problem_content: data["content"],
                })
            }.bind(this)
        })
    }

    componentDidUpdate(){
        if(this.state.complete_third_party_render === false){
            MathJax.typesetPromise();
            let textarea = document.getElementById("code_area");
            editor = CodeMirror.fromTextArea(textarea, {
                lineNumbers: true,
                matchBrackets: true,
                mode: "text/x-c++src",
                theme: "darcula"
            });
            this.setState({editor: editor, complete_third_party_render: true})
        }
    }

    render(){
        let {problem_content, basic_setting} = this.state;
        if(problem_content != undefined){
            return (
                <div>
                    <div class="flex gap-10">
                        <div class="w-3/4 mx-auto h-fit rounded border-2 shadow flex flex-col p-10 gap-10 bg-white">
                            <div class="text-center">
                                <p id="title" class="text-4xl font-medium my-2"> {problem_content["title"]} </p>
                                <p id="TL-text" class="text-lg font-medium my-2"> 程式運行時間限制（TL）：{basic_setting["time_limit"]} 秒</p>
                                <p id="ML-text" class="text-lg font-medium my-2"> 程式運行時間限制（ML）：{basic_setting["memory_limit"]} MB</p>
                            </div>
                            <div>
                                <p class="text-xl font-semibold my-5">題目敘述</p>
                                <LineBreakDescription description={problem_content["description"]}></LineBreakDescription>
                            </div>
                            <div>
                                <p class="text-xl font-semibold my-5">輸入說明</p>
                                <LineBreakDescription description={problem_content["input_description"]}></LineBreakDescription>
                            </div>
                            <div>
                                <p class="text-xl font-semibold my-5">輸出說明</p>
                                <LineBreakDescription description={problem_content["output_description"]}></LineBreakDescription>
                            </div>
                            <div>
                            </div>
                            <div>
                                <p class="text-xl font-semibold my-5">備註</p>
                                <LineBreakDescription description={problem_content["note"]}></LineBreakDescription>
                            </div>
                        </div>
                    </div>,
                    <div class="w-3/4 mx-auto border-2 text-lg flex flex-col gap-10 p-10 shadow bg-white">
                        <textarea id="code_area" class="resize-none w-full h-20"></textarea>
                        <button class="bg-blue-700 w-full delay-50 p-2 hover:bg-blue-500 rounded text-white text-2xl" onclick="submit_code()"> 提交 </button>
                    </div>
                </div>
            )
        }
    }
}

const app = ReactDOM.createRoot(document.getElementById("app"))
app.render(<App></App>)
