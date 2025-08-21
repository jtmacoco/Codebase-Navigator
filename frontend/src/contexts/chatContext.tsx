"use client"
import {createContext, useContext, useState, ReactNode} from "react"
import ChatMessage from "../types/chatMessage"
interface ChatContext{
    message: ChatMessage[];
    addMessage:(msg:ChatMessage)=>void;
}

const ChatContext = createContext<ChatContext|undefined>(undefined);

export default function ChatProvider({children}:{children: ReactNode}){
    const [message,setMessage] = useState<ChatMessage[]>([]);

    const addMessage = (msg:ChatMessage)=>{
        setMessage((prev)=>[...prev,msg]);
    };
    return(
        <ChatContext.Provider value={{message,addMessage}}>
            {children}
        </ChatContext.Provider>
    )
}
export function useChat(){
    const cont = useContext(ChatContext);
    if(!cont) throw new Error("useChat must be used inside ChatProvider");
    return cont;
}

