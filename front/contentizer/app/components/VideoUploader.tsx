'use client';
import { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUpload } from "@fortawesome/free-solid-svg-icons"
import { uploadVideo } from "../lib/file";

export default function VideoUploader() {
    const router = useRouter();
    const [isDragging, setIsDragging] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [videoFile, setVideoFile] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleBoxClick = () => {
        fileInputRef.current?.click();
    }

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setVideoFile(e.target.files[0]);
            handleSubmit(e.target.files[0]);
        }
    }

    const handleOnDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }
    const handleOnDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }
    const handleOnDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        setVideoFile(e.dataTransfer.files[0]);
        handleSubmit();
    }

    async function handleSubmit(file?: File) {
        const fileToUpload = file || videoFile;
        if (fileToUpload) {
            setIsProcessing(true);
            setError(undefined);

            try {
                const result = await uploadVideo(fileToUpload);
                if (result.filename) {
                    console.log(result);
                    router.push(`/${result.project}`);
                }
            } catch (error: any) {
                setError(error.message);
            } finally {
                setIsProcessing(false);
                setVideoFile(null); // Clear selected video
            }
        }
    }

    return (
        <div className="text-white flex flex-col items-center justify-center p-6">

            <div className="w-full max-w-2xl">
                <div className="text-center mb-8">
                    <h1 className="md:text-2xl text-xl font-bold mb-2">Upload New Video & Start Your Project.</h1>
                </div>

                {isProcessing && <p>Processing...</p>}
                {error && <p className="text-red-500">{error}</p>}

                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="hidden"
                    accept="video/mp4,video/quicktime,video/webm"
                />

                <div
                    onClick={handleBoxClick}
                    className={`
              aspect-video rounded-2xl border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center gap-4 cursor-pointer
              ${isDragging ? 'border-purple-500 bg-purple-500/10 scale-[1.02]' : 'border-zinc-700 hover:border-zinc-500 hover:bg-zinc-900'}
            `}
                    onDragOver={handleOnDragOver}
                    onDragLeave={handleOnDragLeave}
                    onDrop={handleOnDrop}
                >
                    <div className="w-16 h-16 rounded-full bg-zinc-800 flex items-center justify-center">
                        <FontAwesomeIcon className='text-lg md:text-2xl' icon={faUpload} />
                    </div>
                    <div className="text-center">
                        <p className="font-medium md:text-lg text-base">Click to upload or drag and drop</p>
                        <p className="md:text-sm text-xs text-zinc-500 mt-1">MP4, MOV, or WebM</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
