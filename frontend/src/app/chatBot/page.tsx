"use client"
import { useRef } from "react";
import Form from 'next/form'
import ChatInput from "./components/chatInput";
export default function chatBot() {
    return (
        <>
            <div className='bg-zinc-800 bg-full h-screen w-screen '>
                <div className="flex flex-col items-center mx-auto justify-center py-10 gap-2">
                    <h2 className="font-semibold text-2xl text-white">Welcome!</h2>
                    <p className="text-zinc-500 text-sm">Ask your first question to get started.</p>
                </div>
                <div className="bg-zinc-900 fixed bottom-0 left-0 w-full  p-4">
                    <ChatInput />
                </div>
            </div>
        </>
    )
}
