import { NavBar } from "../share/navbar";
import ntut_logo from '/ntut_logo.png'
import bgUrl from '/index.jpg'
import '../assets/index.css'

const Index = () =>(
    <div className={`absolute h-full w-full bg-cover`} style={{ backgroundImage: `url(${bgUrl})`}}>
        <div className="absolute h-full w-full bg-gray-900 bg-opacity-80">
            <NavBar
                links={[
                    {title: '題目', href: "/problem"},
                    {title: '關於', href: "/about"},
                    {title: '狀態', href: '/status'}
                ]}
            />
            <div className="absolute left-[50%] top-[50%] -translate-x-[50%] -translate-y-[50%] text-center w-[80%]">
                <p className="text-white text-5xl m-5 hover:text-gray-400 font-medium "> Welcome to NuOJ! </p>
                <p className="text-white text-2xl m-5 hover:text-gray-400"> 一款來自 國立臺北科技大學 的線上程式評測系統 </p>
                <p className="text-white text-2xl m-5 hover:text-gray-400"> 系統正在進行開發中，你可以追蹤<a className="text-orange-500" href="/dev_progress">我們的開發進度</a></p>
            </div>
            <div className="absolute bottom-14 w-full" id="icon">
                <div className="w-full flex justify-center">
                    <div className="p-3 w-fit duration-500 bg-white hover:bg-slate-400">
                        <a href="https://ntut.edu.tw">
                            <img src={ntut_logo}/>
                        </a>
                    </div>
                </div>
                <div className="w-fit mx-auto m-5">
                    <p className="text-white"> 2022, NuOJ Team. </p>
                </div>
            </div>
        </div>
    </div>
)

export default Index
