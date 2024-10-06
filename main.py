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

# Função para listar formatos disponíveis
def list_formats(youtube_url):
    try:
        with yt_dlp.YoutubeDL() as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            formats = info.get('formats', [])
            return formats
    except Exception as e:
        st.error(f"Erro ao listar formatos: {str(e)}")
        return []

# Função para converter vídeo do YouTube para MP4
def convert_youtube_to_mp4(youtube_url, format_id):
    mp4_filename = None
    try:
        st.info(f"Baixando o vídeo do URL: {youtube_url}")
        ydl_opts = {
            'format': format_id,  # formato selecionado pelo usuário
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
            info = ydl.extract_info(youtube_url, download=False)
            mp4_filename = ydl.prepare_filename(info)
        
        st.success(f"Vídeo baixado com sucesso: {mp4_filename}")
        return mp4_filename

    except Exception as e:
        st.error(f"Erro ao converter vídeo: {str(e)}")
        return None

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
st.title("Conversor de YouTube para MP4")

youtube_url = st.text_input("Digite a URL do vídeo do YouTube")

if youtube_url:
    if is_valid_youtube_url(youtube_url):
        if 'formats' not in st.session_state:
            st.session_state['formats'] = list_formats(youtube_url)

        formats = st.session_state['formats']
        if formats:
            format_options = {f"{fmt['format']} ({fmt['ext']}, {fmt.get('resolution', 'N/A')})": fmt['format_id'] for fmt in formats}
            format_choice = st.selectbox("Escolha um formato", list(format_options.keys()))

            if 'format_id' not in st.session_state or st.session_state['format_id'] != format_choice:
                st.session_state['format_id'] = format_options[format_choice]

            if st.button("Converter para MP4"):
                format_id = st.session_state.get('format_id', 'best')
                mp4_filename = convert_youtube_to_mp4(youtube_url, format_id)
                if mp4_filename and os.path.exists(mp4_filename):
                    with open(mp4_filename, "rb") as f:
                        st.download_button("Baixar MP4", f, file_name=os.path.basename(mp4_filename))
                    st.info(f"Limpando arquivo: {mp4_filename}")
                    os.remove(mp4_filename)  # Remove o arquivo local após o download
                else:
                    st.error("Falha ao localizar o arquivo baixado.")
        else:
            st.error("Nenhum formato disponível para o vídeo.")
    else:
        st.error("URL do YouTube inválida. Verifique e tente novamente.")
