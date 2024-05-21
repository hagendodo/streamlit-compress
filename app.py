import streamlit as st
import os
from pydub import AudioSegment
from PIL import Image
from moviepy.editor import VideoFileClip
import io
import tempfile
import PIL 

PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

def compress_audio(input_file, bitrate='64k'):
    audio = AudioSegment.from_file(input_file)
    compressed_audio = audio.set_frame_rate(44100).set_channels(1)
    output_buffer = io.BytesIO()
    compressed_audio.export(output_buffer, format='mp3', bitrate=bitrate)
    return output_buffer.getvalue()

def compress_image(input_file, quality=50):
    img = Image.open(input_file)
    output_buffer = io.BytesIO()
    img_format = input_file.name.split(".")[-1].lower()
    
    if img_format not in ["jpg", "jpeg"]:
        st.warning("Only JPEG format is supported for compression. Converting the image to JPEG...")
        img = img.convert("RGB")
    
    img.save(output_buffer, format='JPEG', quality=quality)
    return output_buffer.getvalue()

def compress_video(input_file, target_resolution=(480, 270), bitrate='500k'):
    try:
        # Use BytesIO to handle in-memory file
        tfile = io.BytesIO(input_file.read())
        
        # Write the BytesIO content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(tfile.getbuffer())
            temp_filename = temp_file.name
        
        # Process the video using moviepy
        video = VideoFileClip(temp_filename)
        video_resized = video.resize(height=target_resolution[1])
        
        # Write the resized video to another temporary file
        temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_output_filename = temp_output_file.name
        temp_output_file.close()
        
        video_resized.write_videofile(temp_output_filename, bitrate=bitrate, codec='libx264')

        # Read the compressed video back into memory
        with open(temp_output_filename, "rb") as f:
            compressed_video = f.read()

        # Clean up temporary files
        os.remove(temp_filename)
        os.remove(temp_output_filename)

        return compressed_video

    except Exception as e:
        # Handle errors
        st.error(f"Error compressing video: {e}")
        return None

def audio_compression():
    st.title("Audio Compression")
    
    st.sidebar.title("Settings")
    audio_bitrate = st.sidebar.selectbox("Select audio bitrate", ["64k", "128k", "192k", "256k", "320k"])
    
    st.write("## Upload your audio file and compress it!")
    
    audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])
    
    if audio_file is not None:
        st.audio(audio_file, format='audio/mp3', start_time=0)
        st.write("Uploaded Audio File Details:")
        audio_details = {"Filename": audio_file.name, "FileType": audio_file.type, "FileSize": audio_file.size}
        st.write(audio_details)
        
        if st.button("Compress Audio"):
            st.write("Compressing audio...")
            compressed_audio = compress_audio(audio_file, bitrate=audio_bitrate)
            st.success("Audio compression successful!")
            
            st.write("### Download Compressed Audio")
            audio_download_button_str = f"Download Compressed Audio File ({os.path.splitext(audio_file.name)[0]}_compressed.mp3)"
            st.download_button(label=audio_download_button_str, data=compressed_audio, file_name=f"{os.path.splitext(audio_file.name)[0]}_compressed.mp3", mime="audio/mpeg", key=None)

def image_compression():
    st.title("Image Compression")
    
    st.sidebar.title("Settings")
    image_quality = st.sidebar.slider("Select image quality", min_value=1, max_value=100, value=50)
    
    st.write("## Upload your image file and compress it!")
    
    image_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg"])
    
    if image_file is not None:
        st.image(image_file, caption="Uploaded Image", use_column_width=True)
        st.write("Uploaded Image File Details:")
        image_details = {"Filename": image_file.name, "FileType": image_file.type, "FileSize": image_file.size}
        st.write(image_details)
        
        if st.button("Compress Image"):
            st.write("Compressing image...")
            compressed_image = compress_image(image_file, quality=image_quality)
            st.success("Image compression successful!")
            
            st.write("### Download Compressed Image")
            image_download_button_str = f"Download Compressed Image File"
            st.download_button(label=image_download_button_str, data=compressed_image, file_name=f"{os.path.splitext(image_file.name)[0]}_compressed.jpg", mime="image/jpeg", key=None)

def video_compression():
    st.title("Video Compression")
    
    st.sidebar.title("Settings")
    target_resolution = st.sidebar.selectbox("Select resolution", ["480p", "720p", "1080p"])
    resolutions = {"480p": (480, 270), "720p": (1280, 720), "1080p": (1920, 1080)}
    video_bitrate = st.sidebar.selectbox("Select video bitrate", ["500k", "1000k", "1500k", "2000k"])
    
    st.write("## Upload your video file and compress it!")
    
    video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])
    
    if video_file is not None:
        st.video(video_file)
        st.write("Uploaded Video File Details:")
        video_details = {"Filename": video_file.name, "FileType": video_file.type, "FileSize": video_file.size}
        st.write(video_details)
        
        if st.button("Compress Video"):
            st.write("Compressing video...")
            compressed_video = compress_video(video_file, target_resolution=resolutions[target_resolution], bitrate=video_bitrate)

            if compressed_video:
                st.success("Video compression successful!")
                
                st.write("### Download Compressed Video")
                video_download_button_str = f"Download Compressed Video File ({os.path.splitext(video_file.name)[0]}_compressed.mp4)"
                st.download_button(label=video_download_button_str, data=compressed_video, file_name=f"{os.path.splitext(video_file.name)[0]}_compressed.mp4", mime="video/mp4", key=None)

def multipage():
    pages = {
        "Audio Compression": audio_compression,
        "Image Compression": image_compression,
        "Video Compression": video_compression
    }
    
    st.sidebar.title("AICOMPY - 1217050116")
    st.sidebar.write("Raden Ibnu Huygenz Widodo")
    page_selection = st.sidebar.radio("Go to", list(pages.keys()))
    
    page = pages[page_selection]
    page()

if __name__ == '__main__':
    multipage()
