# Image optimization tool
# Copyright Volkan Kücükbudak
# Source https://github.com/VolkanSah/image-optimizer/
import streamlit as st
from PIL import Image
import io
import traceback
import time

def compress_image(image, format='webp', quality=85):
    try:
        # Korrektur: Wandle 'jpg' in 'jpeg' um
        save_format = 'jpeg' if format.lower() == 'jpg' else format
        
        # Korrektur: Quality-Wert wird umgekehrt angewendet
        adjusted_quality = 101 - quality  # Dies dreht die Skala um
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=save_format.upper(), quality=adjusted_quality)
        img_byte_arr.seek(0)
        return Image.open(img_byte_arr)
    except Exception as e:
        st.error(f"Image compression error: {e}")
        st.error(traceback.format_exc())
        return None

def main():
    st.title("Image optimization tool")
    
    st.sidebar.header("Optimization settings")
    
    uploaded_file = st.file_uploader("Select an image", type=['jpg', 'png', 'jpeg', 'webp'])
    
    if uploaded_file is not None:
        try:
            original_image = Image.open(uploaded_file)
            
            current_format = original_image.format.lower() if original_image.format else uploaded_file.name.split('.')[-1].lower()
            current_format = 'jpeg' if current_format == 'jpg' else current_format
            
            st.subheader("Original image")
            st.image(original_image, caption=f"Original image ({current_format.upper()})")
            
            original_size_bytes = len(uploaded_file.getvalue())
            st.write(f"Original image size: {original_size_bytes} Bytes")
            
            compression_quality = st.sidebar.slider(
                "Compression quality (100 = best quality, 1 = smallest file)", 
                min_value=1, 
                max_value=100, 
                value=85
            )
            
            target_formats = [fmt for fmt in ['webp', 'jpg', 'png'] if fmt != current_format]
            
            target_format = st.sidebar.selectbox(
                "Target format", 
                target_formats
            )
            
            st.warning("⚠️ Please click 'Optimize Image' ONLY ONCE'!")
            
            progress_bar = st.progress(0)
            
            if st.button("Optimize image"):
                try:
                    progress_bar.progress(20)
                    time.sleep(0.5)
                    
                    optimized_image = compress_image(
                        original_image, 
                        format=target_format, 
                        quality=compression_quality
                    )
                    
                    progress_bar.progress(60)
                    time.sleep(0.5)
                    
                    if optimized_image:
                        save_format = 'jpeg' if target_format.lower() == 'jpg' else target_format
                        
                        img_byte_arr = io.BytesIO()
                        optimized_image.save(img_byte_arr, format=save_format.upper(), quality=101-compression_quality)
                        img_byte_arr.seek(0)
                        
                        progress_bar.progress(100)
                        time.sleep(0.5)
                        
                        optimized_size_bytes = img_byte_arr.getbuffer().nbytes
                        compression_ratio = (1 - optimized_size_bytes / original_size_bytes) * 100
                        
                        st.subheader("Optimization results")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.image(optimized_image, caption=f"Optimized ({target_format.upper()})")
                        
                        with col2:
                            st.write(f"Original size: {original_size_bytes} Bytes")
                            st.write(f"Optimized size: {optimized_size_bytes} Bytes")
                            st.write(f"Compression rate: {compression_ratio:.2f}%")
                        
                        st.download_button(
                            label=f"Download {target_format.upper()}",
                            data=img_byte_arr,
                            file_name=f"optimized_image.{target_format}",
                            mime=f"image/{target_format}"
                        )
                    
                    progress_bar.empty()
                
                except Exception as e:
                    st.error(f"Image optimization error: {e}")
                    progress_bar.empty()
        
        except Exception as e:
            st.error(f"Error loading image: {e}")

if __name__ == "__main__":
    main()
