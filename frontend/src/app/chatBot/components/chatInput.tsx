"use client"
import { Textarea } from "@heroui/input";
import { Button, ButtonGroup } from "@heroui/button";
import Form from "next/form";
import { IoMdSend } from "react-icons/io";
export default function ChatInput() {
    return (
        <>
            <div className='relative flex flex-col w-full flex-grow p-4 '>
                <Form action="/search" className="relative flex">

                    <div className="relative mx-auto">
                        <Textarea
                            minRows={3}
                            classNames={{
                                base: "p-2 w-150",
                                input: "focus-none outline-none"
                            }}
                            className=" flex resize-none bg-zinc-800 rounded-xl text-base"
                            placeholder="Enter your questions..." />
                        <Button size="sm" className="p-2 absolute z-10  bg-zinc-900 z-10 right-2 bottom-2 rounded-xl">
                            <IoMdSend/>
                        </Button>

                    </div>
                </Form >
            </div >
        </>
    )
}