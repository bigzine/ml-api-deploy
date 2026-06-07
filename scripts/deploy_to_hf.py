"""
Déploiement automatique vers Hugging Face Spaces.
Appelé par le pipeline CD.
"""
import os
from huggingface_hub import HfApi

HF_TOKEN   = os.environ["HF_TOKEN"]
HF_REPO_ID = os.environ.get("HF_SPACE_ID", "votre-username/ml-api-deploy")

FILES_TO_UPLOAD = [
    "app/main.py",
    "app/model.py",
    "app/schemas.py",
    "app/routers/predict.py",
    "app/routers/__init__.py",
    "app/__init__.py",
    "requirements.txt",
    "Dockerfile",
    "README.md",
]

api = HfApi(token=HF_TOKEN)

for filepath in FILES_TO_UPLOAD:
    api.upload_file(
        path_or_fileobj=filepath,
        path_in_repo=filepath,
        repo_id=HF_REPO_ID,
        repo_type="space",
    )
    print(f"✅ Uploaded: {filepath}")

print(f"\n🚀 Déployé sur https://huggingface.co/spaces/{HF_REPO_ID}")
