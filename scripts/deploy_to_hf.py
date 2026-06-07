"""
Déploiement automatique vers Hugging Face Spaces.
"""
import os
from huggingface_hub import HfApi

HF_TOKEN   = os.environ["HF_TOKEN"]
HF_REPO_ID = os.environ["HF_SPACE_ID"]  # ex: Ediagabate/ml-api-deploy

FILES_TO_UPLOAD = [
    "app/__init__.py",
    "app/main.py",
    "app/model.py",
    "app/schemas.py",
    "app/routers/__init__.py",
    "app/routers/predict.py",
    "requirements.txt",
    "Dockerfile",
    "README_SPACES.md",
]

api = HfApi(token=HF_TOKEN)

for filepath in FILES_TO_UPLOAD:
    path_in_repo = filepath
    if filepath == "README_SPACES.md":
        path_in_repo = "README.md"

    api.upload_file(
        path_or_fileobj=filepath,
        path_in_repo=path_in_repo,
        repo_id=HF_REPO_ID,
        repo_type="space",
    )
    print(f"✅ Uploaded: {filepath}")

print(f"\n🚀 Déployé sur https://huggingface.co/spaces/{HF_REPO_ID}")
