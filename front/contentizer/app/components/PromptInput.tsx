"use client";

import { useState } from "react";
import { generatePrompt } from "../lib/prompt";

export default function PromptInput({ vidId, time }: { vidId: string, time: number }) {
    const [prompt, setPrompt] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);

    const handleGenerate = async () => {
        setIsProcessing(true);
        try {
            await generatePrompt(vidId, time, prompt);
        } catch (err) {
            console.error(err);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
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
    );
}
