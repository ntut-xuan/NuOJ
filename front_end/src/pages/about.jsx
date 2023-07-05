import "../assets/about.css"
import logo_min from "/logo_min.png"
import { Link } from 'react-router-dom'
const About = () =>{
    const profiles =[
        {
            name: "黃漢軒",
            edu: "國立臺北科技大學 109 級資訊工程系",
            img_url: "https://ntut-xuan.github.io/src/image/uriah2.jpg",
            dutys:[ "System Design", "Backend Design", "Database Design", "Research and Development" ]
        },
        {
            name: "吳秉宸",
            edu: "國立臺北科技大學 109 級資訊工程系",
            img_url: "https://cdn.discordapp.com/attachments/982659073017278527/996374011548274758/233D9288-77FC-43D9-B0D4-1ED24AB5A4C3.JPG",
            dutys:[ "Cyber Security", "Linux Engineer", "Research and Development" ]
        },
        {
            name: "溫紹傑",
            edu: "國立臺北科技大學 109 級資訊工程系",
            img_url: "https://cdn.discordapp.com/attachments/982659073017278527/996384235315277885/IMG_8469.JPG",
            dutys:[ "Frontend Design" ]
        }
    ]

    return(
        <div className={"bg-cover flex items-center bg-orange-200"}>
            <div className="text-center p-5 bg-white rounded-xl mx-auto">
                <div className="py-8">
                    <Link to="/">
                        <img className="w-[8rem] mx-auto" src={logo_min}/>
                    </Link>
                    <p className="text-4xl underline font-thin font-serif p-5"> Nu Online Judge Staff </p>
                </div>
                <div className="flex font-['Noto_Serif_TC']">
                    {profiles.map((profile, profile_i)=>(
                        <div className="profile-container" key={profile_i}>
                            <div className="text-center">
                                <img className="object-contain h-48 w-48 mx-auto" src={profile.img_url}/>
                            </div>
                            <div className="py-5">
                                <p className="text-2xl"> {profile.name} </p>
                                <p className="text-base"> {profile.edu} </p>
                                <div className="py-5">
                                    { profile.dutys.map((duty, duty_i)=>(<p className="text-base" key={profile_i.toString() + duty_i.toString()}> {duty} </p>))}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div> 
    )
}

export default About;