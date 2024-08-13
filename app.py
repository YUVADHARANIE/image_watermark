import streamlit as st
from PIL import Image, ImageEnhance

def add_watermark(image, watermark, position, transparency):
    # Resize watermark if it's too large
    if watermark.size[0] > image.size[0] or watermark.size[1] > image.size[1]:
        watermark = watermark.resize((image.size[0] // 5, image.size[1] // 5), Image.ANTIALIAS)

    # Make the watermark semi-transparent
    watermark = watermark.convert("RGBA")
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(transparency)
    watermark.putalpha(alpha)

    # Position the watermark
    if position == "Top-Left":
        image.paste(watermark, (0, 0), watermark)
    elif position == "Top-Right":
        image.paste(watermark, (image.size[0] - watermark.size[0], 0), watermark)
    elif position == "Bottom-Left":
        image.paste(watermark, (0, image.size[1] - watermark.size[1]), watermark)
    elif position == "Bottom-Right":
        image.paste(watermark, (image.size[0] - watermark.size[0], image.size[1] - watermark.size[1]), watermark)
    elif position == "Center":
        image.paste(watermark, ((image.size[0] - watermark.size[0]) // 2, (image.size[1] - watermark.size[1]) // 2), watermark)

    return image

# Streamlit app layout
st.title("Image Watermarking App")

# Upload an image
image_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
watermark_file = st.file_uploader("Upload a Watermark", type=["png"])

if image_file and watermark_file:
    # Load the image and watermark
    image = Image.open(image_file).convert("RGBA")
    watermark = Image.open(watermark_file).convert("RGBA")

    # Watermark position selection
    position = st.radio("Select Watermark Position", ["Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right", "Center"])
    
    # Transparency slider
    transparency = st.slider("Watermark Transparency", 0.0, 1.0, 0.5)

    # Add watermark to the image
    watermarked_image = add_watermark(image, watermark, position, transparency)

    # Display the watermarked image
    st.image(watermarked_image, caption="Watermarked Image", use_column_width=True)

    # Option to download the image
    output_image = watermarked_image.convert("RGB")
    output_image_path = "watermarked_image.jpg"
    output_image.save(output_image_path)
    with open(output_image_path, "rb") as file:
        st.download_button(label="Download Watermarked Image", data=file, file_name="watermarked_image.jpg", mime="image/jpeg")
