import streamlit as st
import yt_dlp
import os
import re
from pydub import AudioSegment
from io import BytesIO

# Função para validar URL do YouTube
def is_valid_youtube_url(url):
    youtube_regex = r'(https?://)?(www\.)?youtube\.(com|be)/(watch\?v=|embed/|v/|shorts/)?([^&=%\?]{11})'
    match = re.match(youtube_regex, url)
    return match is not None

# Função para converter vídeo do YouTube para MP3
def convert_youtube_to_mp3(youtube_url):
    mp3_audio = None
    try:
        st.info(f"Baixando o áudio do URL: {youtube_url}")
        
        ydl_opts = {
            'format': 'bestaudio/best',  # Baixa o melhor áudio disponível
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',  # Baixa como m4a primeiro
            }],
            'quiet': True  # Para evitar logs excessivos
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            filename = ydl.prepare_filename(info_dict)

        # Convertendo m4a para mp3 com pydub
        st.info(f"Convertendo {filename} para MP3...")
        audio = AudioSegment.from_file(filename)
        mp3_audio = BytesIO()
        audio.export(mp3_audio, format="mp3")
        mp3_audio.seek(0)  # Reseta o ponteiro do BytesIO

        st.success("Download e conversão concluídos!")
    except Exception as e:
        st.error(f"Erro ao converter vídeo para MP3: {e}")
    return mp3_audio

# Interface Streamlit
st.title("Extrator de Áudio MP3 do YouTube")

# Entrada de URL do YouTube
youtube_url = st.text_input("Digite a URL do vídeo do YouTube")

# Quando o usuário insere uma URL válida, o áudio é baixado automaticamente
if youtube_url:
    if is_valid_youtube_url(youtube_url):
        mp3_audio = convert_youtube_to_mp3(youtube_url)
        if mp3_audio:
            st.download_button("Baixar MP3", mp3_audio, file_name="audio.mp3")
        else:
            st.error("Falha ao localizar o arquivo baixado.")
    else:
        st.error("URL do YouTube inválida. Verifique e tente novamente.")
