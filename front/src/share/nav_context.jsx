import { createContext, useEffect, useState } from "react";
// import cookie from "cookie"
import Cookies from 'js-cookie';
import { useContext } from "react";
import { useLocation, Navigate } from 'react-router-dom';

export const nav_context = createContext(null);

export const AuthProvider = ({children})=>{
    const [user, setUser] = useState(null);
    const [isInitial, setInitial] = useState(false);

    useEffect(()=>{
        getInfo();
    },[])

    const getInfo = async () =>{
        let jwt = Cookies.get("jwt");
        if ( jwt ) {
            let res = await fetch("/api/auth/verify_jwt",{
                method: "POST"
            });
            if(res.ok){
                let json = await res.json();
                setUser(json.data);
            }
        }
        setInitial(true);
    }

    const getUser = ()=>{
        if(isInitial){
            if(user) return {state: 1, ...user};
            else return {state: 0};
        }
        else{
            return {state: -1}
        }
    }

    const signin= async ({account, password}) => {
        let res;
        try {
            res = await fetch("/api/auth/login",{
                method: "POST",
                headers:{
                    "Content-Type": "application/json"
                },
                body : JSON.stringify({
                    account: account,
                    password: password
                })
            })   
        } catch (error) {
            console.log(error)
        }

        if(res.ok) {
            getInfo();
        }

        return res.status;
    }

    const signout= async () => {
        let res;
        try { res = await fetch("/api/auth/logout", {method: "POST"}); }
        catch (error) { console.log(error); }
        Cookies.remove("jwt")
        if (res.ok) {
            setUser(null);
        }
        return res.status;
        
    }

    let context = {getUser, signin, signout};
    return <auth_context.Provider value={context}>{children}</auth_context.Provider>;
}

export const RequireAuth = ({children, loadingElement = (<p>loading</p>)})=>{
    const auth = useContext(auth_context);
    const user= auth.getUser();
    const location = useLocation();
    
    console.log(user, location);
    if(user.state === 1){
        return children;
    }
    else if (user.state === -1 ){
        return loadingElement;
    }
    else{
        return <Navigate to={"/auth/login"} state={{from: location}} replace></Navigate>
    }

}