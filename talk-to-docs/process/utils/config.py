from utils import consts
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    #GCP Settings
    project_id:str = ""
    location:str = "us-central1"
    file_type:str=consts.FileType.HTML.value

    #JOB Settings
    cloud_run_task_index:int=0
    cloud_run_task_count:int=1

    #VDB Connection Settings
    db_instance:str="my_instance"
    db_name:str="doc_search"
    db_host:str=""
    db_port:str="5432"
    db_user:str="postgres"
    db_password:str="postgres"


    #Documents Only settings
    docs_bucket:str ="kw-filtered-files"
    doc_collection:str="docs_col"
    doc_processing_batch_size:int=5

    # Uploading local dir of files to GCS
    upload_local_dir_path: str = "docs/jsonl_to_txt"

    # Local JSONL file to multiple text file
    local_jsonl_file_path: str = "docs/jsonl_file.json"
    jsonl_to_txt_output_dir: str = "docs/jsonl_to_txt"
