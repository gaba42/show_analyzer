# import gradio as gr
# from theme_classifier import ThemeClassifier


# def get_themes(theme_list_str, subtitles_path, save_path):
#     theme_list = theme_list_str.split(",")
#     theme_classifier = ThemeClassifier(theme_list)
#     output_df = theme_classifier.get_themes(subtitles_path, save_path)

#     # Remove dialogue ufrom the theme list
#     theme_list = [theme for theme in theme_list if theme != 'dialogue']
#     output_df = output_df[theme_list]

#     output_df = output_df[theme_list].sum().reset_index()
#     output_df.columns = ['Theme', 'Score']

#     output_chart = gr.BarPlot(
#         output_df,
#         x="Theme",
#         y='Score',
#         title="테마 분석",
#         tooltip=['Theme', 'Score'],
#         vertical=False,
#         width=500,
#         height=260,
#     )

#     return output_chart


# def main():
#     with gr.Blocks() as iface:
#         with gr.Row():
#             with gr.Column():
#                 gr.HTML("<h1>테마 분류기(Zero shot classifier</h1>")
#                 with gr.Row():
#                     with gr.Column():
#                         plot = gr.BarPlot()
#                     with gr.Column():
#                         theme_list = gr.Textbox(label="테마")
#                         subtitles_path = gr.Textbox(label="자막 경로")
#                         save_path = gr.Textbox(label="저장 경로")
#                         get_themes_button = gr.Button("테마 확인")
#                         get_themes_button.click(get_themes, inputs=[theme_list, subtitles_path, save_path], outputs=[plot])

#     iface.launch(share=True)

# if __name__ == "__main__":
#     main()


import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier

# def get_themes(theme_list_str, subtitles_path, save_path):
#     print("Button Clicked - Processing Started")  # Debugging print
    
#     try:
#         # Convert theme string to a list
#         theme_list = theme_list_str.split(",")
#         print(f"Theme List: {theme_list}")

#         # Initialize classifier and get results
#         theme_classifier = ThemeClassifier(theme_list)
#         print("Theme Classifier Initialized")

#         output_df = theme_classifier.get_themes(subtitles_path, save_path)
#         print("Classification Completed")

#         # Remove 'dialogue' from themes if present
#         theme_list = [theme for theme in theme_list if theme != 'dialogue']
        
#         if not theme_list:  # Avoid empty list error
#             print("Warning: No themes to process!")
#             return None

#         # Sum scores for each theme
#         output_df = output_df[theme_list].sum().reset_index()
#         output_df.columns = ['Theme', 'Score']
#         print("Data Processed for Bar Plot")

#         # Convert DataFrame to dictionary for Gradio
#         data_dict = {"Theme": output_df["Theme"].tolist(), "Score": output_df["Score"].tolist()}
#         print(f"Data to Display: {data_dict}")

#         # Return the BarPlot with correct data
#         return gr.BarPlot(
#             value=data_dict,  
#             x="Theme",
#             y="Score",
#             title="테마 분석",
#             tooltip=["Theme", "Score"],
#             vertical=False,
#             width=500,
#             height=260
#         )

#     except Exception as e:
#         print(f"Error Occurred: {e}")
#         return f"Error: {e}"

def get_themes(theme_list_str, subtitles_path, save_path):
    print("✅ get_themes() Function Triggered!")  # Debugging print
    return f"Received themes: {theme_list_str}, Subtitles Path: {subtitles_path}, Save Path: {save_path}"



def main():
    with gr.Blocks() as iface:
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>테마 분류기 (Zero Shot Classifier)</h1>")

                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot(value=None)  # Empty placeholder

                    with gr.Column():
                        theme_list = gr.Textbox(label="테마 (쉼표로 구분)")
                        subtitles_path = gr.Textbox(label="자막 경로")
                        save_path = gr.Textbox(label="저장 경로")
                        get_themes_button = gr.Button("테마 확인")

                        def debug_wrapper(*args):
                            print("✅ Button Clicked!")
                            return get_themes(*args)

                        get_themes_button.click(
                            debug_wrapper,  # Wrap function to check if it triggers
                            inputs=[theme_list, subtitles_path, save_path], 
                            outputs=[plot]
                        )

    iface.launch(debug=True)

if __name__ == "__main__":
    main()