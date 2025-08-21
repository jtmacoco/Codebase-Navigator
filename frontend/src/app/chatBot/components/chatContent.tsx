"use client"
import { useChat } from "@/contexts/chatContext";
import ChatHistory from "./chatHistory";
import ChatInput from "./chatInput";
export default function ChatContent({ repo_name }: { repo_name: string }) {
    const { message } = useChat();
    return (
        <>
            <div className="flex flex-col h-screen bg-zinc-800">
                {message.length === 0 ? (
                    <div className="flex flex-col items-center justify-center flex-grow">
                        <h2 className="font-semibold text-2xl text-white">Welcome!</h2>
                        <p className="text-zinc-500 text-sm">Ask your first question to get started.</p>
                    </div>
                ) :
                    <div className="flex-grow overflow-y-auto bg-zinc-800 p-4" >
                        <ChatHistory />
                    </div>
                }
                <div className="bg-zinc-900 p-4">
                    <ChatInput repo_name={repo_name} />
                </div>
            </div>
        </>
    )
}