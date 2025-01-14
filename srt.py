import ffmpeg
import re
import os
import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard

# Function to process the video URL and extract subtitles using ffmpeg-python
def process_video_url(video_url):
    try:
        # Download the subtitles using ffmpeg
        output_path = '/tmp/sub.srt'
        ffmpeg.input(video_url).output(output_path, vn=None, **{'scodec': 'srt'}).overwrite_output().run()

        # Check if the subtitle file exists
        if os.path.exists(output_path):
            # Read and process the SRT file
            with open(output_path, 'r') as input_file:
                srt = input_file.read()

            # Process the SRT content to clean it up
            srt = re.sub(r'<.+?>', '', srt)
            srt = re.sub(r'{.+?}', '', srt)
            srt = re.sub(r'^\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n', '', srt, flags=re.M)
            srt = re.sub('\n', ' ', srt)
            srt = re.sub(r' ‏', ' ', srt)
            srt = re.sub(r'  ', ' ', srt)
            srt = re.sub(r'\. ', '.\n\n', srt)
            srt = re.sub(r'\? ', '?\n\n', srt)
            srt = re.sub(r'\.” ', '.”\n\n', srt)
            srt = re.sub('  ', ' ', srt)
            srt = re.sub(r'\.\n\n\.\n\n\.\n\n', '. . . ', srt)
            srt = re.sub(r'\.\n\n\.\n\n\.”', '. . .”', srt)
            srt = re.sub(r'\.\n\.\n\.\n', '. . . ', srt)

            # Store the subtitle text in session state so it persists across reruns
            st.session_state.srt_text = srt

            # Display the cleaned subtitle text in a text_area widget with updated title
            st.text_area("Vídeo transcrito com sucesso!", srt, height=300)

            # Render copy to clipboard button
            st_copy_to_clipboard("Copiar Texto")

        else:
            st.error("Este vídeo não possui um arquivo de legendas.")
    
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Streamlit UI elements
st.title('Transcrição de Vídeos')
video_url = st.text_input('Cole o link de download do vídeo aqui:')

if st.button("Transcrever o vídeo"):
    if video_url:
        process_video_url(video_url)
    else:
        st.warning("Por favor, insira o link do vídeo.")
