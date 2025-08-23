"use client"
import ErrorMessage from "@/types/ErrorMessage"
import { SegmentViewStateNode } from "next/dist/next-devtools/userspace/app/segment-explorer-node"
import { useState, useEffect } from "react"
export default function ErrorMessages({ message }: ErrorMessage) {
    const [visible, setVisible] = useState(true);
    useEffect(() => {
        const timer = setTimeout(() => {
            setVisible(false);
        }, 5000);
        console.log(visible)
        
        return () => clearTimeout(timer)
    }, [message])
    if (!visible) return null;
    return (
        <>
            <div className="absolute z-50 top-0 w-screen h-screen">
                <div className="p-10 flex items-center justify-center">
                    <div className="p-4 bg-red-100 border border-red-400 rounded text-red-800">
                        <p>An Error occured</p>
                        {message && <p>{message}</p>}
                    </div>
                </div>
            </div>
        </>

    )
}