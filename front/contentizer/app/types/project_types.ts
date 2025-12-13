export type ProjectTracksModel = {
    track_location: string;
    track_start_time: string;
}

export type ProjectFilesModel = {
    version: string;
    project_tracks: Array<ProjectTracksModel>;
}

export type ProjectModel = {
    name: string;
    project_id: string;
    user_id: string;
    project_directory: string;
    project_versions: Array<ProjectFilesModel>;
    last_edited: string;
    thumbnail: string;
}