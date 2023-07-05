import { useEffect, useState } from "react";
import { success_swal, error_swal } from "@/share/error";
import { Form } from "@/share/form"



const Registe = () =>{
    const [color, setColor] = useState("");

    useEffect(()=>{
        // ["bg-blue-300", "bg-orange-300", "bg-purple-300", "bg-red-300"];
        let colorArray = ["blue", "orange", "purple", "red"];
        setColor(colorArray[Math.floor(Math.random() * 4)]);
    },[])

    const handleRegister = async (info) => {
        let res = await fetch("/api/auth/register", {
            "method": "POST",
            headers: {
                "Content-Type": "Application/json"
            },
            body: JSON.stringify(info)
        });

        if(res.ok){
            success_swal("註冊成功")
        }
        else{
            let resCode = res.status;
            if(resCode === 422){
                error_swal("註冊失敗", "錯誤的信箱、密碼或 handle 格式。");
            }
            if(resCode === 403){
                error_swal("註冊失敗", "信箱或 handle 重複。")
            }
        }
    }

    return(
        <div className="w-full h-screen flex">
            <div className={`w-full h-screen bg-cover bg-${color}-300`}>
                <Form
                    title={"註冊"}
                    inputs={[
                     {
                        key: "handle",
                        type: "text",
                        placeholder: "使用者名稱"
                     },
                     {
                        key: "email",
                        type: "text",
                        placeholder: "信箱"
                     },
                     {
                        key: "password",
                        type: "password",
                        placeholder: "密碼"
                     }
                    ]}
                    color={color}
                    foots={[
                     {url: "/auth/login", content: "已經有帳號了嗎？點此登入"}
                    ]}
                    callback={handleRegister}
                />
            </div>
        </div>
    )
}

export default Registe;