import gradio as gr
from theme_classifier import ThemeClassifier


def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(",")
    theme_classifier = ThemeClassifier(theme_list)


def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>테마 분류기(Zero shot classifier</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(label="테마")
                        subtitles_path = gr.Textbox(label="자막 경로")
                        save_path = gr.Textbox(label="저장 경로")
                        get_themes_button = gr.Button("테마 확인")
                        get_themes_button.click(get_themes, inputs=[theme_list, subtitles_path, save_path], outputs=[plot])

    iface.launch(share=True)

if __name__ == "__main__":
    main()