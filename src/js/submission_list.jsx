const ConfigPayload = ({lable = '', type = 'text', width = undefined, className = '', href_pattern = undefined, replacement =[]}) => 
    ({lable: lable,type: type, width: width, className: className,href_pattern:href_pattern ,replacement:replacement})

const construct_conf = (conf) => {
    var Conf = {}
    var ids = []
    conf.forEach(e => {
        Conf[e.id] = ConfigPayload(e)
        ids.push(e.id);
    });
    return [Conf, ids]
}

const Text = ({id, data, config}) => (<span>{data[id]}</span>)
const Link = ({id, data, config}) => {
    if (config.href_pattern === undefined) return(
        <a href={''}>{data[id]}</a>
    )
    const args = config.replacement
    const href = config.href_pattern.replace(/{(\d+)}/g, function(match, number) { 
        return args[number] != 'undefined' ? data[args[number]] : match;
    })
    return(
        <a href={href}>{data[id]}</a>
    )
}

const Containers = ({id, data, config})=>{
    console.log(config)
    const containers = {
        text: (<Text id={id} data={data} config={config}></Text>),
        link: (<Link id={id} data={data} config={config}></Link>)
    }
    return containers[config.type]
}

const Column = ({ids, config, data}) =>{
    return(
        <tr>
            {ids.map(id=>{
                const element_config = config[id]
                return(<td className={element_config.className}>
                    <Containers id={id} data={data} config={element_config}></Containers>
                </td>)})}
        </tr>
    )
}

const Table = ({raw_conf, data})=>{
    const [config, ids] = construct_conf(raw_conf)
    return(
        <div className="overflow-hidden">
            <table className="w-full text-lg text-black dark:text-gray-400 text-center relative table-auto whitespace-nowrap leading-normal">
                <thead>
                    <tr className="bg-orange-200">
                    {
                        ids.map(id=>{
                            const col_conf = config[id]
                            return(<th className={`px-6 py-3`} style={col_conf.width === undefined?{}:{width: col_conf.width}}>{col_conf.lable}</th>)
                        })
                    }
                    </tr>
                </thead>
                <tbody>
                    {data.map(row=>Column({ids: ids,config: config,data: row}))}
                </tbody>
            </table>
        </div>
    )
}

PROBLEMAPIURL = ''

const Submission_list = ()=>{
    const [column,setCol] = React.useState([])
    
    React.useEffect(()=>{
        /* $.ajax({
            url: PROBLEMAPIURL,
            method: 'GET',
            dataType: 'json',
            success: (data, status, xml)=>{
                setCol(data.list)
            }
        }) */
    },[])

    return(
        <Table raw_conf={[
            {lable: '提交ID', id: 'id', width: '6rem'},
            {lable: '提交時間', id: 'submit_t', width: '18rem'},
            {lable: '題目', width: '18rem', id: 'problem',type: 'link', href_pattern:'/problem/{0}', replacement: ['problem_id'] },
            {lable: '提交人', id: 'submitter',type: 'link', href_pattern: '/profile/{0}', replacement: ['submitter']},
            {lable: '狀態', id: 'status'},
            {lable: '記憶體', id: 'memory'},
            {lable: '時長', id: 'consume_time'}
        ]} data={[
            {id: 1, submit_t: "YYYY-MM-DDThh:mm:ss", problem_id: 1, problem:'test', submitter: 'qwe', status: 'AC', memory: '123M', consume_time: '00:00'}
        ]}></Table>
    )
}

ReactDOM.createRoot(document.getElementById("table")).render(<Submission_list></Submission_list>)