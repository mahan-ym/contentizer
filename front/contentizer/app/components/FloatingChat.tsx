"use client";

import { useState } from "react";
import { generatePrompt } from "../lib/prompt";
import { faMessage, faClose, faRocket, faRobot } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface Message {
    role: "user" | "assistant";
    content: string;
    timestamp: Date;
}

export default function FloatingChat({ project_id, time }: { project_id: string; time: number }) {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState("");
    const [isProcessing, setIsProcessing] = useState(false);

    const handleSendMessage = async () => {
        if (!inputValue.trim() || isProcessing) return;

        const userMessage: Message = {
            role: "user",
            content: inputValue,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputValue("");
        setIsProcessing(true);

        try {
            const response = await generatePrompt(String(project_id), String(time), inputValue);

            const assistantMessage: Message = {
                role: "assistant",
                content: response.message || "Task completed successfully!",
                timestamp: new Date()
            };

            setMessages(prev => [...prev, assistantMessage]);
        } catch (err) {
            console.error(err);
            const errorMessage: Message = {
                role: "assistant",
                content: "Sorry, there was an error processing your request.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <>
            {/* Floating Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={`fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-br from-purple-600 to-purple-700 hover:from-purple-500 hover:to-purple-600 shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center ${isOpen ? "scale-0" : "scale-100"
                    }`}
                aria-label="Toggle chat"
            >
                <FontAwesomeIcon icon={faRobot} className="text-white text-2xl" />
            </button>

            {/* Floating Chat Panel */}
            <div
                className={`fixed bottom-6 right-6 z-50 w-96 h-[600px] bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl flex flex-col transition-all duration-300 ${isOpen ? "scale-100 opacity-100" : "scale-95 opacity-0 pointer-events-none"
                    }`}
            >
                {/* Header */}
                <div className="flex items-center justify-between p-4 border-b border-zinc-800 bg-gradient-to-r from-purple-900/20 to-purple-800/20">
                    <div className="flex items-center gap-3">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                        <h3 className="font-semibold">Contentizer AI</h3>
                    </div>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="w-8 h-8 rounded-lg hover:bg-zinc-800 flex items-center justify-center transition-colors"
                        aria-label="Close chat"
                    >
                        <FontAwesomeIcon icon={faClose} className="text-zinc-400 hover:text-zinc-200" />
                    </button>
                </div>

                {/* Messages Container */}
                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {messages.length === 0 ? (
                        <div className="h-full flex flex-col items-center justify-center text-center text-zinc-500 px-4">
                            <div className="w-16 h-16 rounded-full bg-purple-900/30 flex items-center justify-center mb-4">
                                <FontAwesomeIcon icon={faMessage} className="text-purple-500 text-3xl" />
                            </div>
                            <p className="text-sm">Ask me to help edit your video!</p>
                            <p className="text-xs mt-2">
                                Try: "Create a dancing banana" or "Create a "
                            </p>
                        </div>
                    ) : (
                        messages.map((message, index) => (
                            <div
                                key={index}
                                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"
                                    }`}
                            >
                                <div
                                    className={`max-w-[80%] rounded-2xl px-4 py-2.5 ${message.role === "user"
                                        ? "bg-purple-600 text-white"
                                        : "bg-zinc-800 text-zinc-100"
                                        }`}
                                >
                                    <p className="text-sm whitespace-pre-wrap break-words">
                                        {message.content}
                                    </p>
                                    <p
                                        className={`text-[10px] mt-1 ${message.role === "user"
                                            ? "text-purple-200"
                                            : "text-zinc-500"
                                            }`}
                                    >
                                        {message.timestamp.toLocaleTimeString([], {
                                            hour: "2-digit",
                                            minute: "2-digit"
                                        })}
                                    </p>
                                </div>
                            </div>
                        ))
                    )}
                    {isProcessing && (
                        <div className="flex justify-start">
                            <div className="bg-zinc-800 rounded-2xl px-4 py-3">
                                <div className="flex gap-1.5">
                                    <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                                    <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                                    <div className="w-2 h-2 bg-zinc-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Input Area */}
                <div className="p-4 border-t border-zinc-800">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                            placeholder="Describe edits to apply..."
                            disabled={isProcessing}
                            className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-purple-500 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        />
                        <button
                            onClick={handleSendMessage}
                            disabled={isProcessing || !inputValue.trim()}
                            className="w-10 h-10 rounded-lg bg-purple-600 hover:bg-purple-500 disabled:bg-zinc-700 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
                            aria-label="Send message"
                        >
                            <FontAwesomeIcon icon={faRocket} className="text-white" />
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}
