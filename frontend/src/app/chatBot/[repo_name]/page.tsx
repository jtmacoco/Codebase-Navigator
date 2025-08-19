import ChatInput from "../components/chatInput"
interface PageProps{
    params: {repo_name:string}
}
export default async function chatBot({params}:PageProps) {
    const {repo_name} = await params;
    return (
        <>
            <div className='bg-zinc-800 bg-full h-screen w-screen '>
                <div className="flex flex-col items-center mx-auto justify-center py-10 gap-2">
                    <h2 className="font-semibold text-2xl text-white">Welcome!</h2>
                    <p className="text-zinc-500 text-sm">Ask your first question to get started.</p>
                </div>
                <div className="bg-zinc-900 fixed bottom-0 left-0 w-full  p-4">
                    <ChatInput repo_name={repo_name}/>
                </div>
            </div>
        </>
    )
}
