from utils import consts
from pydantic_settings import BaseSettings
from google.cloud import secretmanager
import os


client = secretmanager.SecretManagerServiceClient()


class Settings(BaseSettings):

    #GCP Settings
    project_id:str = ""
    location:str = "me-central1"
    file_type:str=consts.FileType.TXT.value

    #JOB Settings
    cloud_run_task_index:int=0
    cloud_run_task_count:int=1

    #VDB Connection Settings
    # db_instance:str="my_instance"
    # db_name:str="doc_search"
    # db_host:str=""
    db_port:str="5432"
    # db_user:str="postgres"
    # db_password:str="postgres"

    #Documents Only settings
    docs_bucket:str ="my-bucket-name"
    doc_collection:str="docs_col"
    doc_processing_batch_size:int=5

    @property
    def db_host(self):
        db_host_secret_name = os.environ['DB_HOST_SECRET_NAME']
        return self.get_secret_from_gcp(db_host_secret_name)

    @property
    def db_password(self):
        db_password_secret_name = os.environ['DB_PASSWORD_SECRET_NAME']
        return self.get_secret_from_gcp(db_password_secret_name)

    @property
    def db_instance(self):
        return os.environ['DB_INSTANCE']

    @property
    def db_name(self):
        return os.environ['DB_NAME']

    @property
    def db_user(self):
        return os.environ['DB_USER']

    def get_secret_from_gcp(self, secret_name: str) -> str:
        response = client.access_secret_version(request={"name": secret_name})
        return response.payload.data.decode("UTF-8")
