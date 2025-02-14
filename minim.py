import gradio as gr

def test_fn(x):
    print("✅ Function Triggered!")
    return f"Input: {x}"

with gr.Blocks() as demo:
    txt = gr.Textbox()
    btn = gr.Button("Test Button")
    out = gr.Textbox()

    btn.click(test_fn, inputs=[txt], outputs=[out])

demo.launch()
