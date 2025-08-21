"use client"
import { useChat } from "@/contexts/chatContext";
import ChatAssistant from "./chatAssistant";
import { useEffect, useRef } from "react";
export default function ChatHistory() {
    const { message } = useChat();
    const scrollRef = useRef<HTMLDivElement>(null);
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTo({
                top: scrollRef.current.scrollHeight,
                behavior: "smooth",
            })
        }
    }, [message])
    return (
        <div ref={scrollRef} className="flex flex-col gap-4 p-6 overflow-y-auto h-full">
            {message.map((m, i) => (
                <div key={i}>
                    <div key={i} className={`mx-auto max-w-3xl p-4 ${m.role === "user"
                        ? "bg-zinc-800"
                        : "bg-zinc-900/25"
                        }`}>
                        <div key={i}
                            className="flex items-start gap-2.5 justify-start"
                        >
                            <div
                                key={i}
                                className={` size-10 shrink-0 rounded-full border flex justify-center items-center ${m.role === "user"
                                    ? "bg-cyan-950 border-cyan-500 text-zinc-200"
                                    : "border-zinc-700 bg-zinc-900"
                                    }`}>
                                {m.role === "user" ? "Y" : "A"}
                            </div>

                            <div className="flex flex-col ml-6 w-full">

                                <div className="flex">
                                    <span className="text-m font-semibold text-gray-900 dark:text-white">
                                        {m.role === "user" ? "You" : "Assistant"}
                                    </span>
                                </div>

                                <div
                                    className={`text-m font-normal py-2.5 text-gray-900 dark:text-white`}
                                >
                                    {m.role === "user" ? m.content : <ChatAssistant content={m.content} />}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )
}