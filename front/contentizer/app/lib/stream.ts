const API_BASE = "http://localhost:8000/api";

export const getVideoStream = (filepath: string) => {
    const videoSrc = `${API_BASE}/stream/${filepath}`;
    return videoSrc;
};

