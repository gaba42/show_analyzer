import gradio as gr
from theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator
from text_classification import JutsuClassifier
import os
from dotenv import load_dotenv
load_dotenv()


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

def get_character_network(subtitles_path, ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)

    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)

    return html

def classify_text(text_classification_model, text_classification_data_path, text_to_classify):
    jutsu_classifier = JutsuClassifier(model_path = text_classification_model,
                                       data_path = text_classification_data_path,
                                       huggingface_token=os.getenv("huggingface_token"))
    
    output = jutsu_classifier.classify_jutsu(text_to_classify)

    return output

def main():
    with gr.Blocks() as iface:
        # Theme Classificaiton section
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
        
        # Character Network Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>캐릭터 네트워크 (NERs and 그래프)</h1>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="자막 경로")
                        ner_path = gr.Textbox(label="NERs 저장 경로")
                        get_network_graph_button = gr.Button("Get Character Network Graph")
                        get_network_graph_button.click(get_character_network, inputs=[subtitles_path, ner_path], outputs=[network_html])

        # Text Classification with LLMs
                with gr.Row():
                    with gr.Column():
                        gr.HTML("<h1>LLMs 활용한 텍스트 분류</h1>")
                        with gr.Row():
                            with gr.Column():
                                text_classification_output = gr.Textbox(label="텍스트 분류 결과")
                            with gr.Column():
                                text_classification_model = gr.Textbox(label="모델 경로")
                                text_classification_data_path = gr.Textbox(label="데이터 경로")
                                text_to_classify = gr.Textbox(label="텍스트 입력")
                                classify_text_button = gr.Button("텍스트 분류 (술법)")
                                classify_text_button.click(classify_text, inputs=[text_classification_model, text_classification_data_path, text_to_classify], outputs=[text_classification_output])


    iface.launch(share=True)

if __name__ == "__main__":
    main()