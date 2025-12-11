"use client";
import Link from 'next/link';
import { useEffect, useState } from 'react';
import { getUserProjects } from '../lib/projects';

type ProjectModel = {
    name: string;
    project_id: string;
    project_file_id: string;
    user_id: string;
    project_location: string;
    last_edited: string;
    thumbnail: string;
}

export default function RecentProjects() {

    const [projects, setProjects] = useState([]);

    useEffect(() => {
        getUserProjects("0").then((data) => {
            console.log(data);
            setProjects(data);
        });
    }, []);

    return (
        <div className="w-full">
            <h2 className="md:text-2xl text-xl font-bold mb-6 text-white">Recent Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {projects.map((project: ProjectModel) => (
                    <Link href={`/${project.project_file_id}`} key={project.project_id} className="group block">
                        <div className="bg-zinc-900 rounded-xl overflow-hidden border border-zinc-800 transition-all duration-300 hover:border-zinc-600 hover:shadow-lg hover:shadow-purple-500/10 hover:-translate-y-1">
                            <div className="aspect-video relative bg-zinc-800 overflow-hidden">
                                <img
                                    src={project.thumbnail}
                                    alt={project.name}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 opacity-80 group-hover:opacity-100"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            </div>
                            <div className="p-4">
                                <h3 className="md:text-lg text-base font-semibold text-white group-hover:text-purple-400 transition-colors">{project.name}</h3>
                                <p className="md:text-sm text-xs text-zinc-400 mt-1">Edited {project.last_edited}</p>
                            </div>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
