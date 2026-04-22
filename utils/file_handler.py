import os

def save_uploaded_file(uploaded_file,path="data/temp_resume.pdf"):
    os.makedirs("data",exist_ok=True)
    with open(path,"wb") as f:
        f.write(uploaded_file.read())
    return path

