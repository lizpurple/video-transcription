import imageio
import re
import streamlit as st

# Function to process the video URL and extract subtitles
def process_video_url(video_url):
    try:
        # Use imageio to download the video and extract metadata
        reader = imageio.get_reader(video_url)
        metadata = reader.get_meta_data()

        # Assuming subtitles are embedded in the metadata (adjust based on the file format)
        if 'subtitles' in metadata:
            srt = metadata['subtitles']
            
            # Process the SRT text
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

            # Create HTML content with the formatted subtitle text
            html_content = f"""
            <div style="white-space: pre-wrap; word-wrap: break-word; font-family: Arial, sans-serif; line-height: 1.5; padding: 10px;">
            {srt}
            </div>
            <button id="copy-button" style="background-color:#4CAF50; color:white; padding:5px 10px; border:none; cursor:pointer;">
            Copy Text
            </button>
            <textarea id="copy-text" style="display:none;">{srt}</textarea>
            <script>
            document.querySelector("#copy-button").addEventListener("click", function() {{
                var copyText = document.querySelector("#copy-text");
                copyText.style.display = "block";
                copyText.select();
                document.execCommand("copy");
                copyText.style.display = "none";
                alert("Text copied to clipboard!");
            }});
            </script>
            """
            st.markdown(html_content, unsafe_allow_html=True)
        else:
            st.error("Este vídeo não possui um arquivo de legendas.")
    
    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")

# Streamlit UI elements
st.title('Transcrição de Vídeo com Subtítulos')
video_url = st.text_input('Cole o link do vídeo aqui:')

if st.button("Transcrever o vídeo"):
    if video_url:
        process_video_url(video_url)
    else:
        st.warning("Por favor, insira o link do vídeo.")
