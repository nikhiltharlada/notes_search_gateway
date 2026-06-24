from shared_data.supabase_client import supabase, BUCKET


def upload_file(local_path, remote_path):

    try:
        file_data = f.read()

        print("FILE SIZE =", len(file_data))
        print("REMOTE PATH =", remote_path)

        result = supabase.storage.from_(BUCKET).upload(
        path=remote_path,
        file=file_data,
        file_options={"upsert": "true"}
        )

        print("UPLOAD RESULT =", result)

    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise e

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