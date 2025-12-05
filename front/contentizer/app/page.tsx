import VideoUploader from "./components/VideoUploader";
import RecentProjects from "./components/RecentProjects";

export default function Home() {
  return (
    <main className="min-h-screen bg-black text-white p-6 md:p-12 font-sans">
      <div className="max-w-7xl mx-auto">
        <header className="flex items-center justify-between mb-12">
          <div className="flex items-center gap-3">
            <span className="text-4xl font-bold tracking-tight">Contentizer</span>
          </div>
        </header>

        <VideoUploader />
        <RecentProjects />
      </div>
    </main>
  );
}
