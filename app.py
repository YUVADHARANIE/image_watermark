import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Set up Streamlit app title and description
st.title("Image Watermarking App")
st.write("Upload an image and add a watermark text to it.")

# Upload image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Load image
    image = Image.open(uploaded_image)

    # Display the original image
    st.image(image, caption="Original Image", use_column_width=True)

    # Input for watermark text
    watermark_text = st.text_input("Enter watermark text", "Sample Watermark")

    # Input for watermark position
    position = st.selectbox("Watermark position", ["Top Left", "Top Right", "Bottom Left", "Bottom Right", "Center"])

    # Input for watermark opacity
    opacity = st.slider("Watermark opacity", 0, 255, 128)

    # Font size and color settings
    font_size = st.slider("Font size", 10, 100, 50)
    color = st.color_picker("Choose font color", "#FFFFFF")

    # Upload font file (optional)
    font_file = st.file_uploader("Upload a font file (e.g., arial.ttf)", type=["ttf"])

    # Watermark processing
    if st.button("Add Watermark"):
        # Make the image editable
        editable_image = image.copy()
        draw = ImageDraw.Draw(editable_image)

        # Choose font
        if font_file is not None:
            font = ImageFont.truetype(font_file, font_size)
        else:
            font = ImageFont.load_default()

        # Set watermark position
        width, height = image.size
        
        # Get text dimensions
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        if position == "Top Left":
            pos = (10, 10)
        elif position == "Top Right":
            pos = (width - text_width - 10, 10)
        elif position == "Bottom Left":
            pos = (10, height - text_height - 10)
        elif position == "Bottom Right":
            pos = (width - text_width - 10, height - text_height - 10)
        else:  # Center
            pos = ((width - text_width) // 2, (height - text_height) // 2)

        # Add watermark
        draw.text(pos, watermark_text, fill=color + hex(opacity)[2:], font=font)

        # Display watermarked image
        st.image(editable_image, caption="Watermarked Image", use_column_width=True)

        # Allow user to download the image
        buf = io.BytesIO()
        editable_image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button("Download watermarked image", byte_im, "watermarked_image.png", "image/png")
