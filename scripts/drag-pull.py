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
        return f"upload failed reason :{e}"
    return "upload success"

def query_models(model_dir):
    if not model_dir:
        return gr.Dropdown.update(visible=False)
    files = list_dir(model_dir)
    return gr.Dropdown.update(choices=files,value=files[0] if files else [], visible=files)

def list_dir(model_dir):
    bsd=scripts.basedir()
    mdp=f'{bsd}/models/{model_dir}'
    return [f for f in os.listdir(mdp) if os.path.isfile(os.path.join(mdp, f))]
    
def download_file(model_dir, model_name):
    if not model_name:
        return gr.File.update( visible=False)
    bsd=scripts.basedir()
    mdp=f'{bsd}/models/{model_dir}/{model_name}'
    return gr.File.update(mdp, visible=True)

def on_ui_tabs():
    with gr.Blocks() as dragpull:
        with gr.Row():
            with gr.Column():
                gr.Markdown("You could put your local models to the model directory you want, for links download try  [batchlinks-webui extension](https://github.com/etherealxx/batchlinks-webui.git)")
                model_dir=gr.Dropdown(["Lora","Stable-diffusion","VAE","VAE-approx","LDSR","karlo","hypernetworks","GFPGAN","ESRGAN","deepbooru","ControlNet","Codeformer"],value="Lora",label="Model Dir")
                file = gr.File()
                output = gr.Textbox(label="upload result")
                uploadbtn = gr.Button("upload",variant="primary")
                uploadbtn.click(fn=upload,inputs=[file,model_dir],outputs=output)
            with gr.Column():
                gr.Markdown("You could download models from the model directory you want")
                model_dir=gr.Dropdown(["Lora","Stable-diffusion","VAE","VAE-approx","LDSR","karlo","hypernetworks","GFPGAN","ESRGAN","deepbooru","ControlNet","Codeformer"],value="Lora",label="Model Dir")
                model_name = gr.Dropdown(list_dir("Lora"),label='Model')
                model_dir.change(fn=query_models, inputs=model_dir, outputs=model_name)
                file = gr.File()
                model_name.change(fn=download_file,inputs=[model_dir,model_name], outputs=file)
    return (dragpull, "drag pull", "drag-pull"),
script_callbacks.on_ui_tabs(on_ui_tabs)
