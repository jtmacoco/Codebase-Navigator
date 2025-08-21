"use client"
import { useState } from 'react';
import { useSubmitGitUrl } from '@/hooks/useSubmitGitUrl';
import { useRouter } from 'next/navigation';
export default function Home() {
  const [url, setUrl] = useState('');
  const { handleSubmit, error, isLoading } = useSubmitGitUrl();
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
      <div className='bg-black bg-full h-screen w-screen '>
        <div className='p-10 justify-center flex'>
          <form onSubmit={onSubmit} className='tex-white' action={"/search"}>
            <input value={url} onChange={(e) => setUrl(e.target.value)} className='mx-5 bg-gray-900' placeholder="type github url" name="query" />
            <button className='' type="submit"  disabled={isLoading}>
              {isLoading ? 'Loading...' : 'Submit'}
            </button>
          </form>
        </div>
        {error && <p className='text-red-500'>{error}</p>}
      </div>
    </>
  );
}
