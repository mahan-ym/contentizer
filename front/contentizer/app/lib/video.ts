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