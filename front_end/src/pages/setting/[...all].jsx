import { NavBar } from '../../compoments/navbar';
import { useNavigate, Routes, Route, Link } from 'react-router-dom';
import { auth_context, RequireAuth } from '../../compoments/auth';
import { useContext, useEffect, Suspense } from 'react';
import SetProfile from './compoments/profile';


const SettingNav = ({links}) =>{
    const link_class = `w-full border-b-2 border-black border-opacity-0 duration-500 hover:border-black hover:border-opacity-100`
    return(
        <div className='w-48 p-2'>
            <div className='shadow-2xl rounded-lg bg-white my-5 border-2 p-2 flex flex-col'>
                {
                    links.map((link)=>(
                        <Link to={"/setting" + link.href} className={link_class} key={link.href}>{link.title}</Link>        
                    ))
                }
            </div>
        </div>
    )
}

const SettingContent = ({links}) =>{
    return(
        <div className='grow p-2'>
            <Suspense fallback={<p>Loading...</p>}>
                <Routes>
                    {
                        links.map((link)=>(
                            <Route path={link.href} element={link.elememt} key={"page_"+link.href}></Route>
                        ))
                    }
                    <Route path='*' element={<p>404</p>}></Route>
                </Routes>
            </Suspense>
        </div>
    )
}

const Setting = () =>{
    const auth = useContext(auth_context);
    const user = auth.getUser();
    let navigate = useNavigate();

    const links = [
        {href: "/profile", title: '個人資訊', elememt: <SetProfile></SetProfile>}
    ]
    return(
        <RequireAuth>
            <div className="w-full bg-gray-100 bg-opacity-80 min-h-screen">
                <NavBar 
                    links={[
                        {title: '題目', href: "/problem"},
                        {title: '關於', href: "/about"},
                        {title: '狀態', href: '/status'}
                    ]}
                    style={'bg-black p-10 w-full flex justify-between'}
                />
                <div className='mx-auto max-w-5xl flex'>
                    <SettingNav links={links} />
                    <SettingContent links={links} />
                </div>
            </div>
        </RequireAuth>
    )
}

export default Setting;