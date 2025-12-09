'use client';
import { useState } from 'react';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faUpload } from "@fortawesome/free-solid-svg-icons"
import { uploadVideo } from "../lib/file";

export default function VideoUploader() {
    const [isDragging, setIsDragging] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [videoFile, setVideoFile] = useState<File | null>(null);

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

    async function handleSubmit() {
        if (videoFile) {
            setIsProcessing(true);
            setError(undefined);

            try {
                await uploadVideo(videoFile);
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

                <div
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
