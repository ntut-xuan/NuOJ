function ToolbarButton(props){
    return (
        <div className="my-auto cursor-pointer">
            <a href={props.href} className="text-3xl my-auto hover:border-b-2 hover:border-b-black"> {props.text} </a>
        </div>
    )
}

class AddProblemToolbar extends React.Component {
    render(){
        PID = window.location.pathname.split("/")[2]
        return (
            <div id="icon" className="p-10 py-5 bg-gray-50 h-fit w-full z-10">
                <div className="flex w-full justify-start gap-16">
                    <div>
                        <a className="relative w-fit h-fit" href="/">
                            <img className="h-[60px] w-auto" src="/static/logo.svg" />
                        </a>
                    </div>
                    <ToolbarButton href={"/edit_problem/" + PID + "/basic"} text="基本設定"/>
                    <ToolbarButton href={"/edit_problem/" + PID + "/solution"} text="解答設定"/>
                    <ToolbarButton href={"/edit_problem/" + PID + "/testcase"} text="測資設定"/>
                    <ToolbarButton href={"/edit_problem/" + PID + "/program_test"} text="程式測試"/>
                </div>
            </div>
        )
    }
}