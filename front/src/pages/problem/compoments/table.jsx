import { Link } from "react-router-dom";

const Header = ({width, lable = ''})=>{
    return(
        <th 
            key={lable}
            scope="col"
            className={`px-6 py-3`}
            style={{width: `${width}\%`}} 
        >{lable}</th>
    )
}

const Data = ({conf, data}) =>{
    const type = conf.type;
    let content;
    if(type === "link"){
        content = (<Link to={data.href}>{data.lable}</Link>)
    }
    else{
        content = (<p>{data}</p>)
    }

    return(
        <td className={`px-6 py-4`} style={{width: `${conf.width}%`}}>
            {content}
        </td>
    )
} 

const Row = ({data, conf})=>(
    <tr className="hover:bg-slate-100 border bg-white">
        {
            data.map((col, index)=><Data conf={conf[index]} data={col} key={`${data[0]}:${index}`}/>)
        }
    </tr>
)

const normalizeCol = (cols)=>{
    let remain = 100;
    let len =  cols.length;
    cols.map((col)=>{
        if(col.width){
            remain = remain - col.width;
            len --;
        }
    });

    let remain_w = Math.round( remain / len);
    let new_cols= cols.map((col)=>{
        let new_col = {...col};
        new_col.width = col.width || remain_w;
        new_col.type = col.type || "text";
        return new_col
    })

    return new_cols;

}

export const Table = ({cols, datas})=>{
    let norma_cols = normalizeCol(cols);

    return(
        <div className="w-4/5 m-5">
            <table className="relative rounded-lg overflow-hidden w-full text-lg text-black text-center relative whitespace-nowrap leading-normal">
                <thead className="bg-orange-200">
                    <tr className="">
                        {
                            norma_cols.map((col)=>Header({...col}))
                        }   
                    </tr>
                </thead>
                <tbody className="">
                    {
                        datas.map(
                            (data, index)=><Row data={data} conf={norma_cols} key={`${data[0]}:${index}`}/>
                        )
                    }
                </tbody>
            </table>
        </div>
    )
}