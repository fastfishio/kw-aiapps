export GCP_PROJECT_ID=''
export GCP_LOCATION='me-central1'
export DOCS_BUCKET=''

export DB_HOST_SECRET_NAME=''
export DB_PASSWORD_SECRET_NAME=''
export DB_INSTANCE=''
export DB_NAME=''
export DB_USER=''
export SERVICE_ACCOUNT=''

AR_REPO='kw-repo' 
JOB_NAME='process-job-kw'
JOB_MEMORY='4Gi'
JOB_CPU=8
JOB_MAX_RETRIES=0
PROCESS_NUM_TASKS=10
TASK_TIMEOUT='5h'

TASK_PARALLELISM=4

IMAGE_NAME="$GCP_LOCATION-docker.pkg.dev/$GCP_PROJECT_ID/$AR_REPO/$JOB_NAME"


echo "Configure gcloud to use $GCP_LOCATION for Cloud Run"
gcloud config set run/region $GCP_LOCATION

echo "Enabling required services"
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com

echo "Creating Artifact Repository"
gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker

echo "Auth Configure Docker"
gcloud auth configure-docker "$GCP_LOCATION-docker.pkg.dev"


echo "Building image into a container"
gcloud builds submit --tag $IMAGE_NAME


echo "Deleting job if it already exists"
gcloud run jobs delete $JOB_NAME --quiet

echo "Creating $JOB_NAME using $IMAGE_NAME"
gcloud run jobs create $JOB_NAME --execute-now \
    --image $IMAGE_NAME \
    --command python \
    --args process.py \
    --tasks $PROCESS_NUM_TASKS \
    --max-retries $JOB_MAX_RETRIES \
    --task-timeout $TASK_TIMEOUT \
    --parallelism $TASK_PARALLELISM \
    --cpu $JOB_CPU \
    --memory $JOB_MEMORY \
    --set-env-vars=PROJECT_ID=$GCP_PROJECT_ID,DOCS_BUCKET=$DOCS_BUCKET,DB_HOST_SECRET_NAME=$DB_HOST_SECRET_NAME,DB_PASSWORD_SECRET_NAME=$DB_PASSWORD_SECRET_NAME,DB_INSTANCE=$DB_INSTANCE,DB_NAME=$DB_NAME,DB_USER=$DB_USER \
    --service-account=$SERVICE_ACCOUNT








