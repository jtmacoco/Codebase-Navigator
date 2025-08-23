import { API_BASE_URL } from "@/constants/endpoints";
/*
* Centralized fetch wrapper 
*
* @typeParam T - The expected reponse type 
* 
* @param url - Request URL
* @param options - Feth options (method, headers, etc)
* 
* @returns A promise resolving to the parsed JSON
* 
*/
async function request<T>(url: string, options: RequestInit): Promise<T> {
    try {
        const is_Get = options.method?.toUpperCase() === 'GET';
        const is_Delete = options.method?.toUpperCase() === 'DELETE';
        const res = await fetch(url, {
            ...options,
            headers: {
                ...(is_Get || is_Delete ? {} : { 'Content-type': "application/json" }),
                ...(options.headers || {}),
            }
        });
        if(!res.ok){
            const body = (await res.json()) as {detail?:string};
            throw new Error(body.detail || "Something went wrong");
        }
        return (res.json() as Promise<T>);
    }
    catch (error) {
        if (error instanceof Error) {
            throw new Error(`Request Error Occured: ${error.message}`);
        }
        else {
            throw new Error("Uknown Error Occured");
        }
    }
}
const httpClient = {
    get: async <T>(url: string) => <T> request(url, { method: 'GET' }),
    post: async <T>(url: string, body: any) => <T>request(url, {
        method: 'POST',
        body: JSON.stringify(body)
    }),
    put: async <T>(url: string, body: any) => <T> request(url, {
        method: 'PUT',
        body: JSON.stringify(body)
    }),
    delete: async <T>(url: string) => <T> request(url, { method: 'DELETE' })
};
export default httpClient
