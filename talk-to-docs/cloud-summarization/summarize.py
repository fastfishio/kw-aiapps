import time, asyncio, math
from utils import doc_process, consts
from utils import config

import summarizer
import threading

settings = config.Settings()

TASK_INDEX = settings.cloud_run_task_index
TASK_COUNT = settings.cloud_run_task_count
DESTINATION_BUCKET = f"{settings.destination_bucket_base}-{settings.summary_word_count}"


def blob_name(doc):
    fname = doc.metadata["source"]
    return fname[fname.rindex("/") + 1 :]


processed_files_counter = 0
lock = threading.Lock()


def read_single_cloud_file():
    pass


def summarize_chunk(processor: doc_process.Client, doc_names: list[str]):
    global processed_files_counter
    local_counter = 0
    for doc_name in doc_names:
        local_fname = f"tmp/{doc_name}"
        processor.dl.download_gcs_to_local(settings.docs_bucket, doc_name, local_fname)
        with open(local_fname, "r") as f:
            content = f.read()
            print("wahaj", content)
        summary = summarizer.summarize(content)
        processor.dl.upload_string_to_gcs(
            content=summary, bucket_name=DESTINATION_BUCKET, blob_name=doc_name
        )

        local_counter += 1
        if local_counter % 100 == 0:
            with lock:
                processed_files_counter += local_counter
                local_counter = 0
                print(f"=====Processed {processed_files_counter} documents")


def process():
    print(
        f"Task {TASK_INDEX}: Processing part {TASK_INDEX} of {TASK_COUNT} "
        f"with following settings {settings.model_dump()}"
    )

    method_start = time.time()

    processor = doc_process.Client(settings=settings)

    doc_names = set(processor.dl.load_gcs_files(bucket_name=processor.docs_bucket))
    summmarized_doc_names = set(
        processor.dl.load_gcs_files(bucket_name=DESTINATION_BUCKET)
    )
    to_summarize_names = list(doc_names - summmarized_doc_names)
    N = len(to_summarize_names)
    print(f"******* {N} documents to be processed...")
    print(to_summarize_names)
    # ['20370.txt', '9357.txt', '29074.txt', '9355.txt', '29465.txt', '9356.txt', '20368.txt', '24349.txt', '24348.txt', '20369.txt', '29075.txt']

    threads_count = 16
    batch_size = math.ceil(N / threads_count)
    threads = []
    for batch_number in range(threads_count):
        start = batch_number * batch_size
        end = min(start + batch_size, N)
        thread = threading.Thread(
            target=summarize_chunk,
            args=(
                processor,
                to_summarize_names[start:end],
            ),
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    time_taken = round(time.time() - method_start, 3)

    print(f"Job Processed in {time_taken}s ")


if __name__ == "__main__":
    process()
