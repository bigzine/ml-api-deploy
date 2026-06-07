import os
from pathlib import Path
from huggingface_hub import HfApi

HF_TOKEN = os.environ["HF_TOKEN"]
HF_REPO_ID = os.environ["HF_SPACE_ID"]

ROOT = Path(__file__).parent.parent

FILES_TO_UPLOAD = [
    ("app/__init__.py", "app/__init__.py"),
    ("app/main.py", "app/main.py"),
    ("app/model.py", "app/model.py"),
    ("app/schemas.py", "app/schemas.py"),
    ("app/routers/__init__.py", "app/routers/__init__.py"),
    ("app/routers/predict.py", "app/routers/predict.py"),
    ("requirements.txt", "requirements.txt"),
    ("Dockerfile", "Dockerfile"),
    ("README_SPACES.md", "README.md"),
]

api = HfApi(token=HF_TOKEN)

for local_path, repo_path in FILES_TO_UPLOAD:
    full_path = ROOT / local_path
    if not full_path.exists():
        print(f"Fichier manquant : {full_path}")
        continue
    api.upload_file(
        path_or_fileobj=str(full_path),
        path_in_repo=repo_path,
        repo_id=HF_REPO_ID,
        repo_type="space",
    )
    print(f"Uploaded: {local_path}")

print(f"Deploye sur https://huggingface.co/spaces/{HF_REPO_ID}")
