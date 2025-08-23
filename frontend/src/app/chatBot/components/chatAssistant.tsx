"use client"
import React from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export default function ChatAssistant({ content }: { content: string }) {
    return (
        <div className="prose prose-invert max-w-3xl">
            <ReactMarkdown remarkPlugins={[remarkGfm]}
            >
                {content}
            </ReactMarkdown>
        </div>
    )
}