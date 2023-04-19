import os.path
from typing import List

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
import win32api
import datetime

from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/upload_files/")
async def create_upload_files(request: Request,
                              files: List[UploadFile] = File(description="Multiple files as UploadFile"),
                              ):
    current_time = str(datetime.datetime.now())
    save_path = f'./upload/{current_time}'
    save_path = save_path.replace(" ", "_")
    save_path = save_path.replace(":", "_")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    for fn in files:
        save_file = os.path.join(save_path, fn.filename)
        f = open(save_file, 'wb')
        data = await fn.read()
        f.write(data)
        f.close()
        win32api.ShellExecute(
            0,
            "print",
            save_file,
            None,
            ".",
            0
        )
    return templates.TemplateResponse(
        "print_files.html",
        {"request": request, "files": files},
        status_code=200,
        media_type="text/html",
    )


@app.get("/")
async def main():
    content = """
<style>
  body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 20px;
  }
  h1 {
    color: #008080;
  }
  p {
    color: #333;
  }
  form {
    border: 1px solid #ccc;
    padding: 10px;
  }
  input[type="file"] {
    margin-bottom: 10px;
  }
</style>
<body>
  <h1>文件上传</h1>
  <p>请选择要上传的文件：</p>
  <form action="/upload_files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <br>
    <br>
    <input type="submit" value="上传">
  </form>
</body>
    """
    return HTMLResponse(content=content)
