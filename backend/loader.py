import os 
ALLOWED_EXTENSIONS = {
    ".py",".js",".jsx",".ts",".tsx",".java",".cpp",".c",".html",".go",".css",".md"
} 

def load_files (repo_path:str):
    documents = []

    for root ,dirs, files in os.walk(repo_path):  # traverse directory and load content. 
        for file in files:
            extension = os.path.splitext(file)[1] #splits the filename into (name ,extension) 

            if extension not in ALLOWED_EXTENSIONS:
                continue

            file_path = os.path.join(root ,file)


            try:
                with open(file_path , "r", encoding="utf-8") as f:
                    content = f.read()

                    documents.append({
                        "content":content,
                        "file_path":file_path
                    })

            except UnicodeDecodeError:
                continue


    return documents
    
