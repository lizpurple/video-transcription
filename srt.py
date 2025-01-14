import streamlit as st
import subprocess
import os
import re

# Title of the web app
st.title("Transcrição de Vídeo por Arquivo SRT")

# Create a text input widget for the video URL
video_url = st.text_input("Cole o link do vídeo aqui")

# Create a button to process the URL
if st.button("Transcrever o vídeo"):
    if not video_url:
        st.error("O link é inválido.")
    else:
        try:
            # Download the subtitles using ffmpeg
            subprocess.run(['ffmpeg', '-i', video_url, '-y', '/content/sub.srt'], check=True)

            # Check if the subtitle file exists
            if os.path.exists('/content/sub.srt'):
                # Read and process the SRT file
                with open('/content/sub.srt', 'r') as input_file:
                    srt = input_file.read()

                # Remove tags and unwanted content
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

                # Display the processed SRT text
                st.text_area("Texto transcrito", srt, height=300)

                # Provide a copy button for users
                st.download_button(
                    label="Copiar Transcrição",
                    data=srt,
                    file_name="transcription.txt",
                    mime="text/plain"
                )

                # Clean up
                os.remove('/content/sub.srt')
            else:
                st.error("Este vídeo não possui um arquivo de legendas.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
