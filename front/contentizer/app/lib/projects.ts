
export async function getUserProjects(
    user_id: string
): Promise<any> {

    const response = await fetch("http://localhost:8000/api/recent_projects", {
        method: "GET"
    });

    if (!response.ok) {
        throw new Error("Failed to get recent projects");
    }

    return response.json();
}