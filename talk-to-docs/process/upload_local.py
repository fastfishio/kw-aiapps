import time
from utils import data_loader
from utils import config

settings = config.Settings()


def upload_lc_dir_to_gcs():
    method_start = time.time()

    dl = data_loader.Client(settings=settings)
    dl.upload_lc_dir_to_gcs(
        dir_path=settings.upload_local_dir_path,
        bucket_name=settings.docs_bucket,
    )

    time_taken = round(time.time() - method_start, 3)
    print(f"Job Processed in {time_taken}s ")


if __name__ == "__main__":
    upload_lc_dir_to_gcs()
