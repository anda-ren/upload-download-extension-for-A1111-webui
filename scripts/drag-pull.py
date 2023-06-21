from modules import script_callbacks ,scripts
import shutil
import gradio as gr
import os

def upload(file,file_type):
    filename=os.path.basename(file.name)
    bsd=scripts.basedir()
    try:
        shutil.move(file.name, f'{bsd}/models/{file_type}/{filename}')
    except Exception as e:
        return f"uploading failed reason :{e}"
    return "uploading success"


def on_ui_tabs():
    with gr.Blocks() as dragpull:
        gr.Markdown("You could put your local models to the directory you would like")
        type=gr.Dropdown(["Lora","Stable-diffusion","VAE","VAE-approx","LDSR","karlo","hypernetworks","GFPGAN","ESRGAN","deepbooru","ControlNet","Codeformer"],value="Lora",label="Model Dir")
        file = gr.File()
        output = gr.Textbox(label="upload result")
        uploadbtn = gr.Button("upload",variant="primary")
        uploadbtn.click(fn=upload,inputs=[file,type],outputs=output)
    return (dragpull, "drag pull", "drag-pull"),
script_callbacks.on_ui_tabs(on_ui_tabs)
