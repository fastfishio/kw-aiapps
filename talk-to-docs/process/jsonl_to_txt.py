import time
from utils import config

settings = config.Settings()


def jsonl_to_multiple_txt():
    method_start = time.time()

    counter = 1
    with open(settings.local_jsonl_file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            with open(f'{settings.jsonl_to_txt_output_dir}/{counter}.txt', 'w') as text_file:
                text_file.write(line)
                counter += 1

    time_taken = round(time.time() - method_start, 3)
    print(f"Job Processed in {time_taken}s ")


if __name__ == "__main__":
    jsonl_to_multiple_txt()
