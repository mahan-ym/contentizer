"use client";
import { useState, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay, faPause, faCompress, faScissors, faMousePointer } from "@fortawesome/free-solid-svg-icons";

export default function VideoEditor({ vidId }: { vidId: string }) {
    const videoRef = useRef<HTMLVideoElement>(null);
    const timelineRef = useRef<HTMLDivElement>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [isDraggingPlayhead, setIsDraggingPlayhead] = useState(false);

    // Trim state (visual only for now)
    const [trimStart, setTrimStart] = useState(0); // 0%
    const [trimEnd, setTrimEnd] = useState(100); // 100%

    // Construct the video URL assuming it's in public/assets
    const [prompt, setPrompt] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);

    // Backend API URL
    const API_BASE = "http://localhost:8000/api";
    const videoSrc = `${API_BASE}/stream/${vidId}`;

    const togglePlay = () => {
        if (videoRef.current) {
            if (isPlaying) {
                videoRef.current.pause();
            } else {
                videoRef.current.play();
            }
            setIsPlaying(!isPlaying);
        }
    };

    const handleTimeUpdate = () => {
        if (videoRef.current && !isDraggingPlayhead) {
            setCurrentTime(videoRef.current.currentTime);
        }
    };

    const handleLoadedMetadata = () => {
        if (videoRef.current) {
            setDuration(videoRef.current.duration);
        }
    };

    const handleTimelineClick = (e: React.MouseEvent<HTMLDivElement>) => {
        if (timelineRef.current && videoRef.current) {
            const rect = timelineRef.current.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const percentage = Math.max(0, Math.min(1, x / rect.width));
            const time = percentage * duration;

            videoRef.current.currentTime = time;
            setCurrentTime(time);
        }
    };

    const formatTime = (seconds: number) => {
        const h = Math.floor(seconds / 3600);
        const m = Math.floor((seconds % 3600) / 60);
        const s = Math.floor(seconds % 60);
        return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    };

    const handleGenerate = async () => {
        if (!prompt) return;
        setIsProcessing(true);
        try {
            await fetch(`${API_BASE}/agent/prompt`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ filename: vidId, prompt }),
            });
            // Clear prompt or show success
            setPrompt("");
        } catch (err) {
            console.error(err);
        } finally {
            setIsProcessing(false);
        }
    };

    const handleTrim = async () => {
        setIsProcessing(true);
        try {
            // Convert percentage to seconds
            const startStr = duration * (trimStart / 100);
            const endStr = duration * (trimEnd / 100);

            const res = await fetch(`${API_BASE}/trim`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    filename: vidId,
                    start_time: startStr,
                    end_time: endStr
                }),
            });
            if (res.ok) {
                const data = await res.json();
                // Optionally redirect to new video or update src
                // window.location.href = `/${data.filename}`;
                alert(`Trimmed video created: ${data.filename}`);
            }
        } catch (err) {
            console.error(err);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <div className="h-screen flex flex-col bg-black text-white overflow-hidden">
            {/* Header */}
            <header className="h-14 border-b border-zinc-800 flex items-center justify-between px-4 bg-zinc-900/50">
                <div className="flex items-center gap-4">
                    <a href="/" className="p-2 hover:bg-zinc-800 rounded-md transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m15 18-6-6 6-6" /></svg>
                    </a>
                    <h1 className="font-semibold text-sm">Project: {vidId}</h1>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => handleTrim()}
                        disabled={isProcessing}
                        className="px-4 py-1.5 text-xs font-medium bg-purple-600 hover:bg-purple-500 disabled:bg-purple-800 rounded-md transition-colors"
                    >
                        {isProcessing ? "Processing..." : "Export / Trim"}
                    </button>
                </div>
            </header>

            {/* Main Content */}
            <div className="flex-1 flex overflow-hidden">
                {/* Left Sidebar - Assets/Tools */}
                <div className="w-16 border-r border-zinc-800 flex flex-col items-center py-4 gap-4 bg-zinc-900/30">
                    <button className="w-10 h-10 bg-zinc-800 hover:bg-zinc-700 rounded-md flex items-center justify-center transition-colors" title="Select">
                        <FontAwesomeIcon icon={faMousePointer} className="text-zinc-400" />
                    </button>
                    <button className="w-10 h-10 bg-zinc-800 hover:bg-zinc-700 rounded-md flex items-center justify-center transition-colors" title="Trim">
                        <FontAwesomeIcon icon={faScissors} className="text-zinc-400" />
                    </button>
                </div>

                {/* Center - Player & Prompt */}
                <div className="flex-1 flex flex-col min-w-0">
                    <div className="flex-1 p-4 flex items-center justify-center bg-zinc-950 relative">
                        {/* Player */}
                        <div className="aspect-video w-full max-w-4xl bg-zinc-900 rounded-lg border border-zinc-800 flex items-center justify-center shadow-2xl overflow-hidden relative group">
                            <video
                                ref={videoRef}
                                src={videoSrc}
                                className="w-full h-full object-contain"
                                onTimeUpdate={handleTimeUpdate}
                                onLoadedMetadata={handleLoadedMetadata}
                                onClick={togglePlay}
                            />
                            {/* Overlay Play Button */}
                            {!isPlaying && (
                                <div className="absolute inset-0 flex items-center justify-center bg-black/30 cursor-pointer" onClick={togglePlay}>
                                    <div className="w-16 h-16 rounded-full bg-purple-600/90 flex items-center justify-center backdrop-blur-sm transition-transform hover:scale-105">
                                        <FontAwesomeIcon icon={faPlay} className="text-2xl ml-1" />
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Prompt Area */}
                    <div className="h-32 border-t border-zinc-800 bg-zinc-900/50 p-4">
                        <div className="max-w-3xl mx-auto w-full h-full flex gap-2">
                            <input
                                value={prompt}
                                onChange={(e) => setPrompt(e.target.value)}
                                onKeyDown={(e) => e.key === "Enter" && handleGenerate()}
                                type="text"
                                placeholder="Describe edits to apply..."
                                className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-4 focus:outline-none focus:border-purple-500 transition-colors"
                            />
                            <button
                                onClick={handleGenerate}
                                disabled={isProcessing}
                                className="px-6 bg-white text-black font-medium rounded-lg hover:bg-zinc-200 disabled:bg-zinc-400 transition-colors"
                            >
                                {isProcessing ? "..." : "Generate"}
                            </button>
                        </div>
                    </div>
                </div>

                {/* Right Sidebar - Properties */}
                <div className="w-64 border-l border-zinc-800 bg-zinc-900/30 p-4">
                    <h3 className="text-xs font-bold text-zinc-500 uppercase mb-4">Properties</h3>
                    <div className="space-y-4">
                        <div className="p-3 bg-zinc-800/50 rounded-lg border border-zinc-800">
                            <p className="text-xs text-zinc-400 mb-1">Duration</p>
                            <p className="font-mono text-sm">{formatTime(duration)}</p>
                        </div>
                        <div className="p-3 bg-zinc-800/50 rounded-lg border border-zinc-800">
                            <p className="text-xs text-zinc-400 mb-1">Resolution</p>
                            <p className="font-mono text-sm">1920x1080</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom - Timeline */}
            <div className="h-64 border-t border-zinc-800 bg-zinc-900/80 p-2 flex flex-col">
                <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800/50 mb-2">
                    <div className="flex items-center gap-4">
                        <button onClick={togglePlay} className="w-8 h-8 rounded-full bg-white text-black flex items-center justify-center hover:bg-zinc-200 transition-colors">
                            <FontAwesomeIcon icon={isPlaying ? faPause : faPlay} className="text-xs" />
                        </button>
                        <span className="font-mono text-sm text-zinc-400">
                            <span className="text-white">{formatTime(currentTime)}</span> / {formatTime(duration)}
                        </span>
                    </div>
                    <div className="flex gap-2">
                        <div className="w-32 h-1 bg-zinc-800 rounded-full overflow-hidden">
                            <div className="h-full bg-purple-500" style={{ width: '100%' }}></div>
                        </div>
                    </div>
                </div>

                <div className="flex-1 relative overflow-hidden mx-4 my-2" ref={timelineRef} onClick={handleTimelineClick}>
                    {/* Time Ruler */}
                    <div className="h-6 border-b border-zinc-800 flex justify-between text-[10px] text-zinc-600 font-mono select-none">
                        <span>00:00</span>
                        <span>{formatTime(duration / 2)}</span>
                        <span>{formatTime(duration)}</span>
                    </div>

                    {/* Tracks Container */}
                    <div className="relative mt-2 h-full">
                        {/* Trim visual indicator (background dim) */}
                        <div className="absolute inset-0 bg-black/60 pointer-events-none z-10" style={{
                            clipPath: `polygon(${trimStart}% 0, ${trimEnd}% 0, ${trimEnd}% 100%, ${trimStart}% 100%)`
                        }}></div>

                        {/* Track 1 */}
                        <div className="h-16 bg-zinc-800/50 rounded-lg border border-zinc-700/50 mb-2 relative group overflow-hidden">
                            {/* Video Strip Simulation */}
                            <div className="absolute inset-0 opacity-20 flex" style={{ backgroundImage: 'linear-gradient(90deg, #333 1px, transparent 1px)', backgroundSize: '20px 100%' }}></div>
                            <div className="absolute inset-y-0 left-0 bg-purple-600/30 border-r border-purple-500/50 px-2 flex items-center overflow-hidden whitespace-nowrap" style={{ width: '100%' }}>
                                <span className="text-xs text-purple-200 font-medium truncate">{vidId}</span>
                            </div>

                            {/* Trim Handles (Visual) */}
                            <div className="absolute left-0 top-0 bottom-0 w-1 bg-yellow-500 cursor-ew-resize opacity-0 group-hover:opacity-100 transition-opacity"></div>
                            <div className="absolute right-0 top-0 bottom-0 w-1 bg-yellow-500 cursor-ew-resize opacity-0 group-hover:opacity-100 transition-opacity"></div>
                        </div>

                        {/* Playhead */}
                        {duration > 0 && (
                            <div
                                className="absolute top-0 bottom-0 w-px bg-red-500 z-20 pointer-events-none transition-all duration-75"
                                style={{ left: `${(currentTime / duration) * 100}%` }}
                            >
                                <div className="absolute -top-1 -left-1.5 w-3 h-3 bg-red-500 transform rotate-45 shadow-sm" />
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
