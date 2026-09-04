import os 
import shutil 
from git import Repo 


def clone_repo (github_url:str)->str:
    repo_name = github_url.strip("/").split("/")[-1].replace(".git","")

    repo_path = os.path.join("data" ,"repos",repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)



    os.makedirs("data/repos" ,exist_ok=True)

    Repo.clone_from(github_url ,repo_path)

    return repo_path





    