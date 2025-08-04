import httpClient from "../lib/httpClient"
import API_ENDPOINTS from "@/constants/endpoints";
export default function sendGitUrl(body:{github_url:string}){
    const res = httpClient.post();

}