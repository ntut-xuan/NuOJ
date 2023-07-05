import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { NavBar } from '../../share/navbar';

const ProblemDetail = ()=>{
    let id = useParams().id;
    const [data, setData] = useState(null);
    useEffect(()=>{
        getInfo()
    },[]);

    const getInfo = async () => {
        let res = await fetch(`/api/problem/${id}`);

        if(res.ok){
            let json = await res.json();
            let info = {
                "description": json.data.content.description,
                "input_description": json.data.content.input_description,
                "output_description": json.data.content.output_description,
                "note": json.data.content.note,
                "title": json.data.content.title,
                "tl": json.data.setting.time_limit,
                "ml": json.data.setting.memory_limit
            }
            setData(info);
        }
    }


    const lines = [
        {key: "description", lable: '題目敘述'},
        {key: "input_description", lable: '輸入說明'},
        {key: "output_description", lable: '輸出說明'},
        {key: "note", lable: '備註'}
    ]

    return(
        <div className='bg-gray-100'>
            <NavBar
                style = {"bg-black p-10 w-full flex justify-between"}
                links = {[
                    {title: '題目', href: "/problem"},
                    {title: '關於', href: "/about"},
                    {title: '狀態', href: '/status'}
                ]}
            />
            <div className="py-5">
                <div className="w-3/4 mx-auto h-fit rounded border-2 shadow flex flex-col p-10 gap-10 bg-white mb-5">
                    <div className="text-center">
                        <p id="title" className="text-4xl font-medium my-2"> {data?.title} </p>
                        <p id="TL-text" className="text-lg font-medium my-2"> 程式運行時間限制（TL）：{data?.tl} 秒</p>
                        <p id="ML-text" className="text-lg font-medium my-2"> 程式運行時間限制（ML）：{data?.ml} MB</p>
                    </div>
                    {
                        lines.map((line)=>{
                            return(
                                <div key={`${line.key}`}>
                                    <p className="text-xl font-semibold my-5">{line.lable}</p>
                                    {
                                        data?.[line.key].split("\n").map((l,index)=>(
                                            <p key={`${line.key}:${index}`} class="py-1"> {l} </p>
                                        ))
                                    }
                                </div>
                            )
                        })
                    }
                </div>
                <div className="w-3/4 mx-auto border-2 text-lg flex flex-col gap-10 p-10 shadow bg-white">
                    <textarea id="code_area" className="resize-none w-full h-20"></textarea>
                    <button className="bg-blue-700 w-full delay-50 p-2 hover:bg-blue-500 rounded text-white text-2xl"> 提交 </button>
                </div>
            </div>
        </div>
    )
}

export default ProblemDetail;