import { useState } from 'react';
import { Table } from './compoments/table';
import { NavBar } from '@/compoments/navbar';
import logo_min from '/logo_min.png';
import { useEffect } from 'react';

const ProblemList = () =>{
    const [datas, setData] = useState([]);

    useEffect(()=>{getList()},[])

    const getList = async ()=>{
        let res = await fetch("/api/problem",{
            method: "GET"
        })

        if(res.ok){
            let json = await res.json();
            let datas = json.map((problem)=>([
                problem.id, 
                { lable: problem.data.content.title, href: `/problem/${problem.id}`},
                { lable: problem.data.author.handle, href: `/profile/${problem.data.author.handle}`},
                ""
            ]))
            setData(datas)
        }   
    }

    return(
        <div className="w-full bg-gray-100 bg-opacity-80 min-h-screen">
            <NavBar
                links={[
                    {title: "題目列表", href: "/problem/list"},
                    {title: "提交狀況", href: "/problem/submition"},
                ]}
                style={'bg-black p-10 w-full flex justify-between'}
            />
            <div className='p-5 flex'>
                <Table
                    cols={[
                        {lable: "題目 ID", width: 10},
                        {lable: "題目名稱", type: "link"},
                        {lable: "題目作者", type: "link", width: 10},
                        {lable: "題目標籤"}
                    ]}
                    datas={datas}
                />
                <div className="w-[20%] m-5  p-5 h-full bg-white rounded-xl">
                    <img className="w-[50%] mx-auto" src={logo_min}/>
                    <p className="text-2xl text-center p-5"> NuOJ Lab </p>
                </div>
            </div>
            
        </div>
    )
}

export default ProblemList;