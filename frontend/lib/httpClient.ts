/*
* Description:
    * Centralized fetch wrapper
* 
* Args:
    * url (string): Request URL
    * options (RequestInit): Fetch options (method, headers, etc.
*
* Returns:
    * Promise<T>: JSON response
*/
async function request<T>(url: string, options: RequestInit): Promise<T> {
    try {
        const is_Get = options.method?.toUpperCase() === 'GET';
        const is_Delete = options.method?.toUpperCase() === 'DELETE';
        const res = await fetch(url, {
            ...options,
            headers: {
                ...(is_Get || is_Delete ? {} : { 'Content-type': "application/json" }),
                ...(options.headers || {})
            }
        });
        return (res.json());
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
    get: <T>(url: string) => request(url, { method: 'GET' }),
    post: <T>(url: string, body: any) => request(url, {
        method: 'POST',
        body: JSON.stringify(body)
    }),
    put: <T>(url: string, body: any) => request(url, {
        method: 'PUT',
        body: JSON.stringify(body)
    }),
    delete: <T>(url: string) => request(url, { method: 'DELETE' })
};
export default httpClient
