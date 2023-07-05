import { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { NavBar } from "@/share/navbar";
import { getImgSrc, getUserInfo } from '@/share/profile_api';

const UserInfo = ({handle}) =>{
    const [info, setInfo] = useState({school:'', email: "",role: 0, bio: "" });
    const [imgsrc, setSrc] = useState(null);

    useEffect(()=>{
        getUserInfo(handle, setInfo);
        getImgSrc(handle, setSrc);
    },[])

    const subtitles = [
        { key: "school", title: "學校" },
        { key: "email", title: "電子信箱" },
        { key: "bio", title: "個人介紹" }
    ];

    return(
        <div className="mx-auto max-w-5xl flex p-5 shadow-2xl rounded-lg bg-white my-5 border-2">
            <div className="mr-2 border-r-0 pr-2">
                <img className={`w-52 h-52 object-cover rounded-full border-2`} src={imgsrc}/>
            </div>
            <div className="grow">
                <div className="mb-2 border-b-2 pb-2">
                    <p className="text-base text-slate-400 ">{(info.role === 1)? "管理員" : "使用者"}</p>
                    <p className="text-5xl font-medium text-black-700">{handle}</p>
                </div>
                {
                    subtitles.map((subtitle)=>(
                        <div key={subtitle.key} className="pb-2">
                            <p className="text-sm text-slate-400 ">{subtitle.title}</p>
                            <p className="text-base text-slate-900 break-words">{info[subtitle.key]}</p>
                        </div>
                    ))
                }
            </div>
        </div>
    )
}

const Profile = () =>{
    let handle = useParams().handle;

    useEffect(()=>{
        document.title = `NuOJ-${handle}`;
    },[])

    return (
        <div className="w-full bg-gray-100 bg-opacity-80 min-h-screen">
            <NavBar 
                links={[
                    {title: '題目', href: "/problem"},
                    {title: '關於', href: "/about"},
                    {title: '狀態', href: '/status'}
                ]}
                style={'bg-black p-10 w-full flex justify-between'}
            />
            <UserInfo handle={handle}></UserInfo>
        </div>
    )
}

export default Profile;