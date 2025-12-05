'use client';
import { useState } from 'react';

export default function VideoUploader() {
    const [isDragging, setIsDragging] = useState(false);

    return (
        <div className="text-white flex flex-col items-center justify-center p-6">
            <div className="w-full max-w-2xl">
                <div className="text-center mb-8">
                    <h1 className="text-2xl font-bold mb-2">Upload New Video & Start Your Project.</h1>
                </div>

                <div
                    className={`
              aspect-video rounded-2xl border-2 border-dashed transition-all duration-300 flex flex-col items-center justify-center gap-4 cursor-pointer
              ${isDragging ? 'border-purple-500 bg-purple-500/10 scale-[1.02]' : 'border-zinc-700 hover:border-zinc-500 hover:bg-zinc-900'}
            `}
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    onDrop={(e) => { e.preventDefault(); setIsDragging(false); }}
                >
                    <div className="w-16 h-16 rounded-full bg-zinc-800 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-zinc-400"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" x2="12" y1="3" y2="15" /></svg>
                    </div>
                    <div className="text-center">
                        <p className="font-medium text-lg">Click to upload or drag and drop</p>
                        <p className="text-sm text-zinc-500 mt-1">MP4, MOV, or WebM</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
