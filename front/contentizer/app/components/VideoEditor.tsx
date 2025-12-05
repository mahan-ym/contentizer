export default function VideoEditor({ vidId }: { vidId: string }) {
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
                    <button className="px-4 py-1.5 text-xs font-medium bg-purple-600 hover:bg-purple-500 rounded-md transition-colors">Export</button>
                </div>
            </header>

            {/* Main Content */}
            <div className="flex-1 flex overflow-hidden">
                {/* Left Sidebar - Assets/Tools */}
                <div className="w-16 border-r border-zinc-800 flex flex-col items-center py-4 gap-4 bg-zinc-900/30">
                    <div className="w-10 h-10 bg-zinc-800 rounded-md" />
                    <div className="w-10 h-10 bg-zinc-800 rounded-md" />
                    <div className="w-10 h-10 bg-zinc-800 rounded-md" />
                </div>

                {/* Center - Player & Prompt */}
                <div className="flex-1 flex flex-col min-w-0">
                    <div className="flex-1 p-4 flex items-center justify-center bg-zinc-950 relative">
                        {/* Player Placeholder */}
                        <div className="aspect-video w-full max-w-4xl bg-zinc-900 rounded-lg border border-zinc-800 flex items-center justify-center shadow-2xl">
                            <p className="text-zinc-500">Video Player Preview</p>
                        </div>
                    </div>

                    {/* Prompt Area */}
                    <div className="h-32 border-t border-zinc-800 bg-zinc-900/50 p-4">
                        <div className="max-w-3xl mx-auto w-full h-full flex gap-2">
                            <input
                                type="text"
                                placeholder="Describe edits to apply..."
                                className="flex-1 bg-zinc-800 border border-zinc-700 rounded-lg px-4 focus:outline-none focus:border-purple-500 transition-colors"
                            />
                            <button className="px-6 bg-white text-black font-medium rounded-lg hover:bg-zinc-200 transition-colors">
                                Generate
                            </button>
                        </div>
                    </div>
                </div>

                {/* Right Sidebar - Properties */}
                <div className="w-64 border-l border-zinc-800 bg-zinc-900/30 p-4">
                    <h3 className="text-xs font-bold text-zinc-500 uppercase mb-4">Properties</h3>
                    <div className="space-y-4">
                        <div className="h-8 bg-zinc-800 rounded" />
                        <div className="h-24 bg-zinc-800 rounded" />
                        <div className="h-8 bg-zinc-800 rounded" />
                    </div>
                </div>
            </div>

            {/* Bottom - Timeline */}
            <div className="h-64 border-t border-zinc-800 bg-zinc-900/80 p-2">
                <div className="flex items-center justify-between px-2 mb-2">
                    <span className="text-xs text-zinc-500">00:00:00</span>
                    <div className="flex gap-2">
                        <div className="w-4 h-4 bg-zinc-700 rounded-full" />
                        <div className="w-4 h-4 bg-zinc-700 rounded-full" />
                    </div>
                </div>
                <div className="h-full bg-zinc-950/50 rounded border border-zinc-800/50 relative overflow-hidden">
                    {/* Timeline Tracks */}
                    <div className="absolute top-4 left-0 right-0 h-12 bg-purple-900/20 border-y border-purple-500/20 mx-4 rounded">
                        <div className="absolute inset-y-0 left-0 w-1/3 bg-purple-600/20 border-r border-purple-500/50" />
                    </div>
                    <div className="absolute top-20 left-0 right-0 h-12 bg-blue-900/20 border-y border-blue-500/20 mx-4 rounded">
                        <div className="absolute inset-y-0 left-1/4 w-1/2 bg-blue-600/20 border-r border-blue-500/50" />
                    </div>

                    {/* Playhead */}
                    <div className="absolute top-0 bottom-0 left-1/3 w-px bg-red-500 z-10">
                        <div className="absolute -top-1 -left-1.5 w-3 h-3 bg-red-500 transform rotate-45" />
                    </div>
                </div>
            </div>
        </div>
    );
}
