import gradio as gr
from package import resynthesize

def process(input):
    if not input:
        raise gr.Error('No input image')
    image = input['image']
    mask = input['mask']
    return resynthesize(image, mask)

with gr.Blocks(title="Resynthesizer", analytics_enabled=False) as iface:
    with gr.Row():
        with gr.Column():
            input = gr.Image(
                label="Source",
                source="upload",
                interactive=True,
                type="pil",
                tool="sketch",
                image_mode="RGBA",
                brush_color='#84FF9A',
                height=700
            )

        with gr.Column():
            output = gr.Image(
                label="Result",
                interactive=False,
            )
    with gr.Row():
        run = gr.Button("Run")
    run.click(fn=process, inputs=[input], outputs=[output])

iface.launch()
