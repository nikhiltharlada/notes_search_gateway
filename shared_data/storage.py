from shared_data.supabase_client import supabase, BUCKET


def upload_file(local_path, remote_path):

    with open(local_path, "rb") as f:

        supabase.storage.from_(BUCKET).upload(
            remote_path,
            f.read(),
            {"upsert": True}
        )


def download_file(remote_path, local_path):

    data = supabase.storage.from_(BUCKET).download(
        remote_path
    )

    with open(local_path, "wb") as f:

        f.write(data)


def list_files(folder):

    return supabase.storage.from_(BUCKET).list(
        folder
    )


def delete_file(remote_path):

    supabase.storage.from_(BUCKET).remove(
        [remote_path]
    )


def delete_all(folder):

    files = list_files(folder)

    if len(files) == 0:
        return

    paths = []

    for file in files:

        paths.append(
            folder + "/" + file["name"]
        )

    supabase.storage.from_(BUCKET).remove(
        paths
    )