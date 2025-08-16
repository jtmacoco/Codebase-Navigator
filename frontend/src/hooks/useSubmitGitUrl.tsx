import { useState } from "react";
import sendGitUrl from "../../services/codebaseService";
import GitResponsse from "@/types/gitResponse";

/*
* A custom hook for submitting a Github repo URL
*
* @returns  An object containing
* - `handleSubmit`: Function to send the Github URL and return the parsed response
* - `error`: Error message if submission fails, otherwise `null`
* - `isLoading`: Boolean indicating whether a submission is in progress
* 
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