import httpClient from "../lib/httpClient";
import { CHATBOT_URL } from "@/constants/endpoints";
import { API_BASE_URL } from "@/constants/endpoints";
export default async function sendMessage(body:{message:string}){
    return await httpClient.post(CHATBOT_URL,body);
}