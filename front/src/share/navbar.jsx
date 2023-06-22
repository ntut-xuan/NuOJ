import { Link } from 'react-router-dom';
import logo from '/logo-white.svg';

const Links = ({
    links
}) =>{
    const LinkClass = "text-white text-2xl border-b-2 border-white border-opacity-0 duration-500 hover:border-white hover:border-opacity-100"
    return(
        <div className="flex gap-20 items-center min-h-[7vh] justify-start w-full">
            <div className="w-fit text-center">
                <Link to={"/"}>
                    <img className="w-32 h-auto mx-auto" src={logo}/>
                </Link>
            </div>
            {
                links.map((link)=>(
                    <div className="w-fit text-center" key={link.href}>
                        <Link className= {LinkClass} to={link.href}> {link.title} </Link>
                    </div>
                ))
            }
        </div>
    )
}

export const NavBar = ({
    links,
    sytle
}) =>{
    let bar_class = sytle ? sytle : "absolute p-10 w-full flex justify-between";
    return(
        <div className={bar_class}>
            <Links links={links}></Links>
        </div>
    )
}