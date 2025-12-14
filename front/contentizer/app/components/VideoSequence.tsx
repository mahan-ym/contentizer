"use client";

interface Track {
    track_location: string;
    track_start_time: number;
    track_duration?: number;
    track_type: string;
}

interface VideoSequenceProps {
    tracks: Track[];
    duration: number;
    onTrackClick?: (track: Track, index: number) => void;
}

export default function VideoSequence({ tracks, duration, onTrackClick }: VideoSequenceProps) {
    const getTrackColor = (index: number) => {
        const colors = [
            'bg-purple-600/30 border-purple-500/50',
            'bg-blue-600/30 border-blue-500/50',
            'bg-green-600/30 border-green-500/50',
            'bg-yellow-600/30 border-yellow-500/50',
            'bg-pink-600/30 border-pink-500/50',
        ];
        return colors[index % colors.length];
    };

    const getTrackTextColor = (index: number) => {
        const colors = [
            'text-purple-200',
            'text-blue-200',
            'text-green-200',
            'text-yellow-200',
            'text-pink-200',
        ];
        return colors[index % colors.length];
    };

    return (
        <div className="relative h-16 flex gap-2">
            {tracks.map((track, index) => {
                const widthPercentage = duration > 0 && track.track_duration
                    ? (track.track_duration / duration) * 100
                    : 100 / tracks.length;

                return (
                    <div
                        key={index}
                        className={`h-full ${getTrackColor(index)} rounded-lg border relative group overflow-hidden cursor-pointer hover:opacity-80 transition-opacity flex-shrink-0`}
                        style={{ width: `${widthPercentage}%` }}
                        onClick={() => onTrackClick?.(track, index)}
                    >
                        {/* Video Strip Background Pattern */}
                        <div
                            className="absolute inset-0 opacity-20 flex"
                            style={{
                                backgroundImage: 'linear-gradient(90deg, #333 1px, transparent 1px)',
                                backgroundSize: '20px 100%'
                            }}
                        />

                        {/* Track Content */}
                        <div className="absolute inset-0 px-2 flex items-center overflow-hidden whitespace-nowrap">
                            <span className={`text-xs ${getTrackTextColor(index)} font-medium truncate select-none`}>
                                {track.track_location.split('/').pop() || `Video ${index + 1}`}
                            </span>

                            {/* Duration Badge */}
                            {track.track_duration && (
                                <span className="ml-auto text-[10px] text-white/60 bg-black/30 px-1.5 py-0.5 rounded">
                                    {Number(track.track_duration).toFixed(1)}s
                                </span>
                            )}
                        </div>

                        {/* Hover Effect */}
                        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity bg-white/5 pointer-events-none" />
                    </div>
                );
            })}
        </div>
    );
}
