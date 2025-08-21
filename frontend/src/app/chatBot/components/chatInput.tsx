"use client"
import { useState } from 'react';
import { Textarea } from "@heroui/input";
import ChatResponse from '@/types/chatResponse';
import { IoMdSend } from "react-icons/io";
import sendMessage from '../../../../services/chatService';
import { useChat } from '@/contexts/chatContext';
interface InputProp {
    repo_name: string;
}
export default function ChatInput({ repo_name }: InputProp) {
    const [message, setMessage] = useState("");
    const {addMessage} = useChat();
    const handleSubmit = async (e: React.FormEvent, message: string) => {
        e.preventDefault();
        addMessage({role:"user",content:message});
        setMessage("");
        const res = await sendMessage({ message: message, repo_name: repo_name }) as ChatResponse;
        if(res?.response){
            addMessage({role:"assistant",content:res.response});
        }
    }
    return (
        <>
            <div className='relative flex flex-col w-full flex-grow p-4 '>
                <form action="/search" className="relative flex" onSubmit={(e) => { handleSubmit(e, message) }}>
                    <div className="relative mx-auto">
                        <Textarea
                            minRows={3}
                            value={message}
                            onChange={(e) => { setMessage(e.target.value) }}
                            classNames={{
                                base: "p-2 w-150",
                                input: "focus-none outline-none"
                            }}
                            className=" flex resize-none bg-zinc-800 rounded-xl text-base"
                            placeholder="Enter your questions..." />
                        <button type="submit" className="p-2 absolute z-10  bg-zinc-900 z-10 right-2 bottom-2 rounded-xl">
                            <IoMdSend />
                        </button>
                    </div>
                </form >
            </div >
        </>
    )
}