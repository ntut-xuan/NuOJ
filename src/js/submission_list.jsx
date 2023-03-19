const Table = ({table_heads, table_cols})=>{
    console.log(table_heads)
    return(
        <div className="overflow-hidden">
            <table className="w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal">
                <thead>
                    <tr className="bg-orange-200">
                        {
                            table_heads.map(head=>
                                <th scope="col" className={`py-3 ${head.w?`w-[${head.w}%]`:''}`}>{head.lable}</th>
                            )
                        }
                    </tr>
                </thead>
                <tbody>
                    {table_cols.map(col=>{
                        <tr>
                            {
                                <td></td>
                            }
                        </tr>
                    })}
                </tbody>
            </table>
        </div>
    )
}

const Submission_list = ()=>{
    const [column,setCol] = React.useState([])
    
    // React.useEffect(
        
    // )
    const heads = [
        {lable: '提交ID'}, 
        {lable: '提交時間'}, 
        {lable: '題目'}, 
        {lable: '提交人'},
        {lable: '狀態'},
        {lable: '記憶體'},
        {lable: '時長'}
    ]
    
    return(
        <Table table_heads={heads} table_cols={column}></Table>
    )
}

ReactDOM.createRoot(document.getElementById("table")).render(<Submission_list></Submission_list>)