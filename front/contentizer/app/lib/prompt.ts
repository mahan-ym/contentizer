export async function generatePrompt(
    video_id: string,
    time: string,
    prompt: string
): Promise<any> {
    const response = await fetch("http://localhost:8000/api/agent/prompt", {
        method: "POST",
        body: JSON.stringify({
            video_id: video_id,
            time: time,
            prompt: prompt,
        })
    });

    if (!response.ok) {
        throw new Error("Failed to generate prompt");
    }

    return response.json();
}