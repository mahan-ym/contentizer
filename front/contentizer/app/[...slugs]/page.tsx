"use client";
import { useParams } from "next/navigation";
import VideoEditor from "../components/VideoEditor";

export default function EditPage() {
    const params = useParams();
    const slugs = params.slugs as string[];
    const vidId = slugs[0];

    return <VideoEditor vidId={vidId} />;
}