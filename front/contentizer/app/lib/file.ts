
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
}