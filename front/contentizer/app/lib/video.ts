export async function trimVideo(
    project_location: string,
    start_time: string,
    end_time: string
): Promise<any> {

    const response = await fetch("http://localhost:8000/api/video/trim", {
        method: "POST",
        body: JSON.stringify({
            project_location: project_location,
            start_time: start_time,
            end_time: end_time,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error("Failed to trim video");
    }

    console.log(response.json())

    return response.json();
}

export async function getVideoInfo(video_id: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/api/video/get_info/${video_id}`, {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error("Failed to get video info");
    }

    return response.json();
}

export async function addVideoToProject(
    project_id: string,
    video_path: string
): Promise<any> {
    const response = await fetch("http://localhost:8000/api/video/add_video", {
        method: "POST",
        body: JSON.stringify({
            project_id: project_id,
            video_path: video_path,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error("Failed to add video to project");
    }

    return response.json();
}

export async function concatenateVideos(
    project_id: string,
    output_filename?: string
): Promise<any> {
    const response = await fetch("http://localhost:8000/api/video/concatenate", {
        method: "POST",
        body: JSON.stringify({
            project_id: project_id,
            output_filename: output_filename,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error("Failed to concatenate videos");
    }

    return response.json();
}


export async function exportVideo(): Promise<any> {
    const response = await fetch("http://localhost:8000/api/video/export", {
        method: "POST",
    });

    if (!response.ok) {
        throw new Error("Failed to export video");
    }

    return response.json();
}

export async function getVideoDuration(file_path: string): Promise<any> {
    const response = await fetch(`http://localhost:8000/api/video/video_duration/${file_path}`, {
        method: "GET",
    });

    if (!response.ok) {
        throw new Error("Failed to get video info");
    }

    return response.json();
}