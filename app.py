import streamlit as st
from PIL import Image, ImageDraw, ImageFont

def watermark_image(image, text):
    # Open an image file
    with Image.open(image) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        # Position for watermark text
        text_position = (10, img.height - 30)

        # Add text to image
        draw.text(text_position, text, font=font)

        return img

st.title("Watermark Image App")

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
watermark_text = st.text_input("Enter watermark text:")

if uploaded_file and watermark_text:
    img = watermark_image(uploaded_file, watermark_text)
    st.image(img, caption='Watermarked Image', use_column_width=True)
