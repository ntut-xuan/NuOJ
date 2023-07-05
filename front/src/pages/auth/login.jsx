import { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Form } from '@/share/form'
import { auth_context } from "@/share/auth";
import { useContext } from "react";
import { success_swal, error_swal } from "@/share/error";
import { show_mail_confirm_swal } from '@/share/email';

const Login = ()=>{
    const [color, setColor] = useState("");
    const auth = useContext(auth_context);
    const user = auth.getUser();
    const navigate = useNavigate();
    const location = useLocation();
    const redir_url = location.state?.from?.pathname || "/";

    useEffect(()=>{
        // ["bg-blue-300", "bg-orange-300", "bg-purple-300", "bg-red-300"];
        let colorArray = ["blue", "orange", "purple", "red"];
        setColor(colorArray[Math.floor(Math.random() * 4)]);
    }, [])

    useEffect(()=>{
        if(user.state === 1) 
            navigate(redir_url)
    }, []);

    const handleLogin = async (info) => {
        let StateCode = await auth.signin(info);
        console.log(StateCode);
        if(StateCode === 200) {
            success_swal("登入成功").then(()=>navigate(redir_url));
        }
        else{
            if ( StateCode === 403) {
                error_swal("登入失敗", "帳號或密碼錯誤");
            }
            else if (StateCode == 422) {
                error_swal("登入失敗", "錯誤的信箱格式")
            }
            else if (StateCode === 401 ){
                show_mail_confirm_swal(info.account)
            }
        }
    }

    return(
        <div className="w-full h-screen flex">
            <div className={`w-full h-screen bg-cover bg-${color}-300`}>
                <div className="w-full h-screen bg-cover">
                    <div className="w-full h-full">
                        <Form
                           title={"登入"}
                           inputs={[
                            {
                                key: "account",
                                type: "text",
                                placeholder: "帳號或電子信箱"
                            },
                            {
                                key: "password",
                                type: "password",
                                placeholder: "密碼"
                            }
                           ]}
                           color={color}
                           foots={[
                            {url: "/auth/registe", content: "沒有帳號嗎？點此註冊"}
                           ]}
                           callback={handleLogin}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login;