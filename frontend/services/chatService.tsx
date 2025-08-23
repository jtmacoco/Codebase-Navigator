import httpClient from "../lib/httpClient";
import { CHATBOT_URL } from "@/constants/endpoints";
import { API_BASE_URL } from "@/constants/endpoints";
import ChatMessage from "@/types/chatMessage";
import ChatResponse from "@/types/chatResponse";
export default async function sendMessage(body:{message:string,repo_name:string}){
    return await httpClient.post<ChatResponse>(CHATBOT_URL,body);
}