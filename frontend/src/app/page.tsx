import Form from 'next/form'
export default function Home() {
  return (
    <>
      <div className='bg-black bg-full h-screen w-screen '>
        <div className='p-10 justify-center flex'>
          <Form className='tex-white' action={"/search"}>
            <input className='mx-5 bg-gray-900' placeholder="type github url" name="query" />
            <button className='' type="submit">Submit</button>
          </Form>
        </div>
      </div>
    </>
  );
}
