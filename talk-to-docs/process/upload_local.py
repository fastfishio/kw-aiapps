import math
import time
import threading
from utils import data_loader
from utils import config

settings = config.Settings()

processed_files_counter = 0
lock = threading.Lock()


def upload_chunk(dl: data_loader.Client, dir_path: str, file_names: list[str], bucket_name: str):
    global processed_files_counter
    local_counter = 0
    for file_name in file_names:
        file_path = f"{dir_path}/{file_name}"
        dl.upload_local_to_gcs(file_path=file_path, bucket_name=bucket_name, blob_name=file_name)

        local_counter += 1
        if local_counter % 200 == 0:
            with lock:
                processed_files_counter += local_counter
                local_counter = 0
                print(f"=====Processed {processed_files_counter} documents")


def upload_lc_dir_to_gcs():
    method_start = time.time()

    dl = data_loader.Client(settings=settings)

    files_names = set(dl.get_files_in_dir(dir_path=settings.upload_local_dir_path))
    uploaded_file_names = set(dl.load_gcs_files(settings.docs_bucket))
    files_to_upload = list(files_names - uploaded_file_names)
    print('documents to upload: ', len(files_to_upload))

    threads_count = 16
    batch_size = math.ceil(len(files_to_upload) / threads_count)
    threads = []
    for batch_number in range(threads_count):
        start = batch_number * batch_size
        end = min(start + batch_size, len(files_to_upload))
        thread = threading.Thread(
            target=upload_chunk,
            args=(
                dl,
                settings.upload_local_dir_path,
                files_to_upload[start:end],
                settings.docs_bucket,
            )
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    time_taken = round(time.time() - method_start, 3)
    print(f"Job Processed in {time_taken}s ")


if __name__ == "__main__":
    upload_lc_dir_to_gcs()
