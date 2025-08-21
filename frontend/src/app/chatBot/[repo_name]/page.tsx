import ChatProvider from "@/contexts/chatContext";
import ChatInput from "../components/chatInput"
import ChatHistory from "../components/chatHistory";
import ChatContent from "../components/chatContent";
import { useChat } from "@/contexts/chatContext";
interface PageProps {
    params: { repo_name: string } }


export default async function ChatBot({ params }: PageProps) {
    const { repo_name } = await params;
    return (
        <ChatProvider>
            <ChatContent repo_name={repo_name}/>
        </ChatProvider>
    )
}
