import GitResponsse from "@/types/gitResponse";
import httpClient from "../lib/httpClient";
import { GIT_URL } from "@/constants/endpoints";
export default async function sendGitUrl(body:{github_url:string}){
    return await httpClient.post<GitResponsse>(GIT_URL,body); 
}