import { useState } from "react";
import sendGitUrl from "../../services/codebaseService";
import GitResponsse from "@/types/gitResponse";

/*
* Description: Github URL submission hook
*
* 
* Returns :
    * handleSubmit: Submission Function
    * error (String): Error Messages
    * isLoading (Boolean): Inidcates Loading State
*/
export function useSubmitGitUrl() {
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const handleSubmit = async (url: string) => {
        setError(null);
        setIsLoading(true);
        try {
            const res = await sendGitUrl({ github_url: url })as GitResponsse;
            return res
        }
        catch (error) {
            if (error instanceof Error) {
                setError(error.message);
            }
        } finally {
            setIsLoading(false);
        }
    };
    return { handleSubmit, error, isLoading };
}