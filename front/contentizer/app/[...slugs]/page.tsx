"use client";
import { useParams } from "next/navigation";
import VideoEditor from "../components/VideoEditor";

export default function EditPage() {
    const params = useParams();
    const slugs = params.slugs as string[];
    const project_id = slugs[0];

    return <VideoEditor project_id={project_id} />;
}