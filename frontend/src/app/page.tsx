"use client"
import Form from 'next/form'
import { useState } from 'react';
import { useSubmitGitUrl } from '@/hooks/useSubmitGitUrl';
export default function Home() {
  const [url,setUrl] = useState('');
  const {handleSubmit, error, isLoading} = useSubmitGitUrl();

  return (
    <>
      <div className='bg-black bg-full h-screen w-screen '>
        <div className='p-10 justify-center flex'>
          <Form className='tex-white' action={"/search"}>
            <input value={url} onChange={(e)=>setUrl(e.target.value)} className='mx-5 bg-gray-900' placeholder="type github url" name="query" />
            <button className='' type="submit" onClick={()=>handleSubmit(url)} disabled={isLoading}>Submit</button>
          </Form>
        </div>
        {error && <p className='text-red-500'>{error}</p>}
      </div>
    </>
  );
}
