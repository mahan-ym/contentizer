
/**
 * Upload a file to the server
 */
export async function uploadVideo(
    file: File,
    title?: string
): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);
    if (title) {
        formData.append("title", title);
    }

    const response = await fetch("http://localhost:8000/api/upload", {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        throw new Error("Failed to upload video");
    }

    return response.json();
}