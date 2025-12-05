import Link from 'next/link';

const MOCK_PROJECTS = [
    { id: 'proj-1', title: 'Summer Vacation 2024', lastEdited: '2 hours ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Summer' },
    { id: 'proj-2', title: 'Product Demo v2', lastEdited: '1 day ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Demo' },
    { id: 'proj-3', title: 'Instagram Reel', lastEdited: '3 days ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Reel' },
    { id: 'proj-4', title: 'Instagram Reel', lastEdited: '3 days ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Reel' },
    { id: 'proj-5', title: 'Instagram Reel', lastEdited: '3 days ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Reel' },
    { id: 'proj-6', title: 'Instagram Reel', lastEdited: '3 days ago', thumbnail: 'https://placehold.co/600x400/1a1a1a/FFF?text=Reel' }
];

export default function RecentProjects() {
    return (
        <div className="w-full">
            <h2 className="md:text-2xl text-xl font-bold mb-6 text-white">Recent Projects</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {MOCK_PROJECTS.map((project) => (
                    <Link href={`/${project.id}`} key={project.id} className="group block">
                        <div className="bg-zinc-900 rounded-xl overflow-hidden border border-zinc-800 transition-all duration-300 hover:border-zinc-600 hover:shadow-lg hover:shadow-purple-500/10 hover:-translate-y-1">
                            <div className="aspect-video relative bg-zinc-800 overflow-hidden">
                                <img
                                    src={project.thumbnail}
                                    alt={project.title}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105 opacity-80 group-hover:opacity-100"
                                />
                                <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                            </div>
                            <div className="p-4">
                                <h3 className="md:text-lg text-base font-semibold text-white group-hover:text-purple-400 transition-colors">{project.title}</h3>
                                <p className="md:text-sm text-xs text-zinc-400 mt-1">Edited {project.lastEdited}</p>
                            </div>
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}
