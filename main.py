import streamlit as st
import yt_dlp
import os
import re

# Função para validar URL do YouTube
def is_valid_youtube_url(url):
    youtube_regex = r'(https?://)?(www\.)?youtube\.(com|be)/(watch\?v=|embed/|v/|shorts/)?([^&=%\?]{11})'
    match = re.match(youtube_regex, url)
    if match:
        return True
    return False

# Função para converter vídeo do YouTube para MP3
def convert_youtube_to_mp3(youtube_url):
    mp3_filename = None
    try:
        st.info(f"Baixando o áudio do URL: {youtube_url}")
        ydl_opts = {
            'format': 'bestaudio/best',  # Baixa o melhor áudio disponível
            'outtmpl': '%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Qualidade do áudio (pode ajustar)
            }],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            info = ydl.extract_info(youtube_url, download=False)
            mp3_filename = ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"  # Salva como MP3
        
        st.success(f"Áudio MP3 baixado com sucesso: {mp3_filename}")
        return mp3_filename

    except Exception as e:
        st.error(f"Erro ao converter vídeo para MP3: {str(e)}")
        return None

# Interface Streamlit

# Carreguando o ícone da aba
favicon = "img/mp4_icon.png"

# Configurações da página Streamlit
st.set_page_config(page_title="Conversor de YouTube para MP4", page_icon=favicon)

# Caminho absoluto para o diretório atual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho completo para o banner
banner_image = os.path.join(current_dir, "img", "Make-A-YouTube-Video.jpg")

# Adiciona o banner ao aplicativo
st.image(banner_image, use_column_width=True)

# Interface Streamlit
st.title("Extrator de Áudio MP3 do YouTube")

youtube_url = st.text_input("Digite a URL do vídeo do YouTube")

# Quando o usuário insere uma URL válida, o áudio é baixado automaticamente
if youtube_url:
    if is_valid_youtube_url(youtube_url):
        mp3_filename = convert_youtube_to_mp3(youtube_url)
        if mp3_filename and os.path.exists(mp3_filename):
            with open(mp3_filename, "rb") as f:
                st.download_button("Baixar MP3", f, file_name=os.path.basename(mp3_filename))
            st.info(f"Limpando arquivo: {mp3_filename}")
            os.remove(mp3_filename)  # Remove o arquivo local após o download
        else:
            st.error("Falha ao localizar o arquivo baixado.")
    else:
        st.error("URL do YouTube inválida. Verifique e tente novamente.")
