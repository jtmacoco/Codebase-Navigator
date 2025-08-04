import httpClient from "../lib/httpClient";
import { GIT_URL } from "@/constants/endpoints";
import { API_BASE_URL } from "@/constants/endpoints";
export default async function sendGitUrl(body:{github_url:string}){
    return await httpClient.post(GIT_URL,body);
}