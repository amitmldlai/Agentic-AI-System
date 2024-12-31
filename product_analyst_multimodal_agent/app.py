import streamlit as st
import os
from dotenv import load_dotenv
from utils import resize_image_for_display, save_uploaded_file
from agent import analyze_image


load_dotenv()
MAX_IMAGE_WIDTH = 300


def main():
    st.title("Ingredient Insight: Your Nutrition Guide")

    tab_upload, tab_camera = st.tabs(["📤 Upload Image", "📸 Capture Photo"])

    with tab_upload:
        image_choice = st.radio(label="Choose", options=['Image file', 'Image Url'], horizontal=True)
        if image_choice == 'Image file':

            uploaded_file = st.file_uploader(
                "Upload product image",
                type=["jpg", "jpeg", "png"],
            )
        else:
            uploaded_file = st.text_input("Please provide image Url")
            st.button('Submit')
        if uploaded_file:
            resized_image = resize_image_for_display(uploaded_file)
            st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("🔍 Analyze Uploaded Image", key="analyze_upload_image"):
                temp_path = save_uploaded_file(uploaded_file)
                analyze_image(temp_path)
                os.unlink(temp_path)

    with tab_camera:
        camera_photo = st.camera_input("Take a picture of the product")
        if camera_photo:
            resized_image = resize_image_for_display(camera_photo)
            st.image(resized_image, caption="Captured Photo", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("🔍 Analyze Captured Photo", key="analyze_camera_image"):
                temp_path = save_uploaded_file(camera_photo)
                analyze_image(temp_path)
                os.unlink(temp_path)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Nutrition Guide Agent",
        layout="wide",
        page_icon='./icon/nutrition.png'
    )
    main()