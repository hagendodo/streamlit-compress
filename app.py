import streamlit as st
import os
from pydub import AudioSegment
from io import BytesIO

# Function to compress audio
def compress_audio(input_file, bitrate='64k'):
    audio = AudioSegment.from_file(input_file)
    compressed_audio = audio.set_frame_rate(44100).set_channels(1)
    output_buffer = BytesIO()
    compressed_audio.export(output_buffer, format='mp3', bitrate=bitrate)
    return output_buffer.getvalue()

# Main function
def main():
    st.title("Audio Compression Apps")
    
    # Sidebar
    st.sidebar.title("Settings")
    bitrate = st.sidebar.selectbox("Select bitrate", ["64k", "128k", "192k", "256k", "320k"])
    
    # Main content
    st.write("""
    ## Upload your audio file and compress it!
    """)
    
    # File upload
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Uploaded File Details:")
        file_details = {"Filename":audio_file.name,"FileType":audio_file.type,"FileSize":audio_file.size}
        st.write(file_details)
        
        # Compress button
        if st.button("Compress"):
            st.write("Compressing...")
            compressed_audio = compress_audio(audio_file, bitrate=bitrate)
            st.success("Compression successful!")
            
            # Download button for the compressed audio
            st.write("### Download Compressed Audio")
            download_button_str = f"Download Compressed Audio File ({os.path.splitext(audio_file.name)[0]}_compressed.mp3)"
            st.download_button(label=download_button_str, data=compressed_audio, file_name=f"{os.path.splitext(audio_file.name)[0]}_compressed.mp3", mime="audio/mpeg", key=None)

# Run the app
if __name__ == '__main__':
    main()
