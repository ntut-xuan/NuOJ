import { getImgSrc, getUserInfo } from '@/compoments/profile_api';
import { useContext, useEffect, useState, useRef } from 'react';
import { auth_context, RequireAuth } from '@/compoments/auth';
import { success_swal } from '@/compoments/error';
import img_x from '/x.svg'

const Input = ({val, title, callback})=>{
    return(
        <div className='flex py-5'>
            <p className='w-32 text-base text-slate-400 '>{title}</p>
            <textarea 
                className='w-full p-2 border-2 rounded-lg' 
                value={val}
                onChange={(e)=>{ callback(e.target.value) }}
            />
        </div>
    );
}

const ProfileForm = ({infos, callback}) => {
    const auth = useContext(auth_context);
    const user = auth.getUser();
    const [vals, setVal] = useState({});
    const [isChange, setChange] = useState(false);

     const cols = [
        {key: "school", title: "學校", type: "text"},
        {key: "bio", title: "自我介紹", type: ""}
    ]

    useEffect(()=>{setVal({...infos})},[infos]);

    const handleChange = (key, val)=>{
        let new_vals = {...infos};
        new_vals[key] = val;

        setVal(new_vals);

        let change = cols.reduce((a, v)=>{
            if(infos[v.key] !== new_vals[v.key]) return a+1;
            else return a;
        }, 0);
        setChange(change > 0);
    }

    const restoreBackup = ()=>{
        setVal({...infos});
        setChange(false);
    }

    const handleProfileUpdate = async ({bio, school}) => {
        let res = await fetch(`/api/profile/${user.handle}`,{
            method: "POST",
            body: JSON.stringify({
                "bio": bio,
                "school": school
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })

        // if success
        success_swal("更新成功").then(()=>{
            callback({...vals});
            setChange(false);
        })


    }

    return(
        <div className='flex flex-col py-2'>
            {
                cols.map((col)=>(
                    <Input 
                        key={col.title}
                        val={vals[col.key]} 
                        title={col.title}
                        callback={(val)=>handleChange(col.key, val)}
                    />
                ))
            }
            {
                isChange && (
                    <div className='mx-auto'>
                        <button 
                            className='bg-orange-500 text-white p-2 rounded-lg mx-3'
                            onClick={()=>handleProfileUpdate(vals)}
                        >確認更改</button>
                        <button 
                            className='bg-gray-400 text-white p-2 rounded-lg mx-3' 
                            onClick={restoreBackup}
                        >取消</button>
                    </div>
                )
            }
        </div>
    )
}

const ImgForm = ({imgSrc, callback}) => {
    const [newImg, setNew] = useState(null);

    useEffect(()=>{
        setNew(imgSrc);
    },[imgSrc])

    const handleUpdate = async () =>{
        if(newImg == imgSrc)
            success_swal("大頭照並未更改").then(()=>callback(false));
    }

    const updateImg = () =>{
        console.log("qwe")
        let file_input = document.createElement("input")
        file_input.type = "file"
        file_input.accept = "image/*"
        file_input.onchange = e => {
            let image = e.target.files[0];
            let reader = new FileReader();
            reader.readAsDataURL(image)
            reader.onload = readerEvent => {
                let content = readerEvent.target.result;
                setNew(content);
            }
        }
        file_input.click();
    }

    return(
        <div className='w-full h-full fixed bg-black/[.3] top-0 left-0 flex justify-center'>
            <div className='max-w-xl w-1/2 my-auto shadow-2xl rounded-lg bg-white border-2 p-5 '>
                <div className='w-full'>
                    <button className='ml-auto w-5 h-5 block'>
                        <img src={img_x} className='w-5 h-5' onClick={()=>callback(false)}/>
                    </button>
                </div>
                <div className='border-b-2 pb-2 mb-2'>
                    <p className='text-2xl font-medium text-center'>請上傳新圖片</p>
                </div>
                <div className='my-10'>
                    <img className={'w-52 h-52 object-cover mx-auto rounded-full border-2'} src={newImg}/>
                </div>
                <div className='w-fit mx-auto'>
                    <button className='bg-orange-500 text-white p-2 rounded-lg mx-3' onClick={handleUpdate}>確認更改</button>
                    <button className='bg-gray-400 text-white p-2 rounded-lg mx-3' onClick={updateImg}>上傳圖片</button>
                </div>
            </div>
        </div>    
    )
}

const SetProfile = () =>{
    const auth = useContext(auth_context);
    const user = auth.getUser();
    const [info, setInfo] = useState({school:'', email: "",role: 0, bio: "" });
    const [imgpop, setPop] = useState(false);
    const [imgSrc, setSrc] = useState(null);

    useEffect(()=>{
        const handle = user.handle;
        getUserInfo(handle, setInfo);
        getImgSrc(handle, setSrc);
    },[])

    return(
        <div className='shadow-2xl rounded-lg bg-white my-5 border-2 p-5'>
            <div className='border-b-2 pb-2 mb-2'>
                <p className='pl-2 text-2xl font-medium'>設定個人資料</p>
            </div>
            <div className='flex'>
                <div className='mr-4'>
                    <img className='w-52 h-52 object-cover rounded-full border-2' src={imgSrc}/>
                </div>
                <div className="grow flex flex-col justify-between py-5">
                    <div>
                        <p className="text-base text-slate-400 ">{(info.role === 1)? "管理員" : "使用者"}</p>
                        <p className="w-full text-center text-5xl font-medium text-black-700">{ user.handle }</p>
                    </div>
                    <div>
                        <button className='bg-orange-500 text-white p-2 rounded-lg' onClick={()=>setPop(true)}>上傳新大頭貼</button>
                    </div>
                </div>
            </div>
            {
                imgpop && <ImgForm callback={setPop} imgSrc={imgSrc}></ImgForm>
            }
            <ProfileForm infos={info} callback={setInfo}/>
        </div>
    )
}

export default SetProfile;