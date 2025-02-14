import gradio as gr
from theme_classifier import ThemeClassifier


def get_themes(theme_list_str, subtitles_path, save_path):
    theme_list = theme_list_str.split(",")
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)

    # Remove dialogue ufrom the theme list
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]

    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme', 'Score']

    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y='Score',
        title="테마 분석",
        tooltip=['Theme', 'Score'],
        vertical=False,
        width=500,
        height=260,
    )

    return output_chart


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