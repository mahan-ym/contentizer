const API_BASE = "http://localhost:8000/api";

export const getVideoStream = (vidId: string) => {
    const videoSrc = `${API_BASE}/stream/${vidId}`;
    return videoSrc;
};

