import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Function to add watermark to image
def add_watermark(image, watermark_text):
    width, height = image.size
    # Create a new image with RGBA mode for transparency
    watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark, 'RGBA')
    font = ImageFont.load_default()
    
    # Calculate text size and position
    text_width, text_height = draw.textsize(watermark_text, font)
    position = (width - text_width - 10, height - text_height - 10)
    
    # Draw watermark text
    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))
    
    # Combine original image with watermark
    watermarked_image = Image.alpha_composite(image.convert('RGBA'), watermark)
    return watermarked_image.convert('RGB')

st.title('Image Watermarking App')

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
watermark_text = st.text_input("Enter watermark text:")

if uploaded_file and watermark_text:
    # Load and display image
    image = Image.open(uploaded_file)
    st.image(image, caption='Original Image', use_column_width=True)
    
    # Add watermark
    watermarked_image = add_watermark(image, watermark_text)
    
    # Display watermarked image
    st.image(watermarked_image, caption='Watermarked Image', use_column_width=True)
    
    # Convert watermarked image to bytes for download
    buffer = io.BytesIO()
    watermarked_image.save(buffer, format="JPEG")
    buffer.seek(0)
    
    st.download_button(
        label="Download Watermarked Image",
        data=buffer,
        file_name="watermarked_image.jpg",
        mime="image/jpeg"
    )
