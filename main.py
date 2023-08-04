import os
import uuid
import webbrowser
import streamlit as st
import subprocess
import shutil

def download_and_split(set_link, tracks):
    session_id = str(uuid.uuid4())

    # Prepare data for audio-splitter
    os.mkdir(f"/tmp/{session_id}")
    os.mkdir(f"/tmp/{session_id}/output")
    f = open(f"/tmp/{session_id}/tracks.txt", "w")
    f.write(tracks)
    f.close()

    # Download set
    with st.spinner("Dunload do set..."):
        try:
            # Run the command and capture the output
            output = subprocess.check_output(
                f"cd /tmp/{session_id} && yt-dlp -x --audio-format mp3 --audio-quality 0 {set_link} --output set.mp3",
                shell=True,
                stderr=subprocess.STDOUT,
                text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            st.error(f"Erro ao baixar o set:\n{e.output}")
            return

    # Split set
    with st.spinner("Cortando o set..."):
        try:
            # Run the command and capture the output
            output = subprocess.check_output(
                f"cd /tmp/{session_id} && python3 -m album_splitter --file set.mp3 --output ./output",
                shell=True,
                stderr=subprocess.STDOUT,
                text=True)
            print(output)
        except subprocess.CalledProcessError as e:
            st.error(f"Erro a cortar o set:\n{e.output}")

    # Remove metadata
    with st.spinner("Morte aos metadados..."):
        output = subprocess.check_output(
            f"eyeD3 --remove-all /tmp/{session_id}/output",
            shell=True,
            stderr=subprocess.STDOUT,
            text=True)
        print(output)
        
    # Make zip
    with st.spinner("Zipando..."):
        try:
            shutil.move(f"/tmp/{session_id}/set.mp3", f"/tmp/{session_id}/output/set.mp3")
            shutil.make_archive(f"/tmp/{session_id}/output", 'zip', f"/tmp/{session_id}/output")
            shutil.rmtree(f"/tmp/{session_id}/output")
            os.remove(f"/tmp/{session_id}/tracks.txt")
        except subprocess.CalledProcessError as e:
            st.error(f"Erro a zipar:\n{e.output}")

    webbrowser.open_new_tab('google.com')

st.header("Dunload de sets para membros honorários do batimento do chinelo 🩴")
link_yt = st.text_input("Link YouTube", placeholder="https://www.youtube.com/watch?v=rxH2q9VhEXM")
timestamps = st.text_area("Timestamps", placeholder="00:00:05 | ID (Sub Focus & Dimension?) - ID (Intro Dub?)\n00:01:48 | Sub Focus - Trip\n00:03:36 | Sub Focus - Rock It (Wilkinson Remix)\n00:04:18 | Sub Focus & Culture Shock - Recombine")
st.button("DALEEEEEE ⬇️", use_container_width=True, on_click=download_and_split, args=(link_yt, timestamps))