"use client"
import { useState } from 'react';
import { useSubmitGitUrl } from '@/hooks/useSubmitGitUrl';
import { useRouter } from 'next/navigation';
import { IoMdSend } from "react-icons/io";
import ErrorMessages from './error';
export default function Home() {
  const [url, setUrl] = useState('');
  const { handleSubmit, error, isLoading, status } = useSubmitGitUrl();
  const router = useRouter();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await handleSubmit(url);
    const repo_name = res?.repo_name;
    if (res) {
      router.push(`chatBot/${repo_name}`);
    }
  };

  return (
    <>
      <div className='bg-zinc-900 bg-full h-screen w-screen '>
        <div className='pb-10 justify-center flex-col  flex items-center h-screen '>
          <h1 className='p-10 text-xl'>
            Enter A Github URL To Begin
          </h1>
          <form onSubmit={onSubmit} className='tex-white' action={"/search"}>
            <input value={url} onChange={(e) => setUrl(e.target.value)}
              className='rounded mx-5 bg-zinc-700 p-2 w-120'
              placeholder="type github url"
              name="query" />
            <button className='bg-zinc-700 p-2 rounded-xl hover:bg-zinc-600' type="submit" disabled={isLoading}>
              {isLoading ? 'Loading...' : (<IoMdSend />)}
            </button>
          </form>
        </div>
        {error && <ErrorMessages message={error}/>}
      </div>
    </>
  );
}
