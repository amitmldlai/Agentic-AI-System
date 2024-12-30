import streamlit as st
import os
from dotenv import load_dotenv
from utils import resize_image_for_display, save_uploaded_file
from agent import analyze_image


load_dotenv()
MAX_IMAGE_WIDTH = 300


def main():
    st.title("🍎 Ingredient Insight: Your Nutrition Guide")

    if 'selected_example' not in st.session_state:
        st.session_state.selected_example = None
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False

    tab_upload, tab_camera = st.tabs([
        "📤 Upload Image",
        "📸 Take Photo"
    ])

    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload product image",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of the product's ingredient list"
        )
        if uploaded_file:
            resized_image = resize_image_for_display(uploaded_file)
            st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("🔍 Analyze Uploaded Image", key="analyze_upload"):
                temp_path = save_uploaded_file(uploaded_file)
                analyze_image(temp_path)
                os.unlink(temp_path)

    with tab_camera:
        camera_photo = st.camera_input("Take a picture of the product")
        if camera_photo:
            resized_image = resize_image_for_display(camera_photo)
            st.image(resized_image, caption="Captured Photo", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("🔍 Analyze Captured Photo", key="analyze_camera"):
                temp_path = save_uploaded_file(camera_photo)
                analyze_image(temp_path)
                os.unlink(temp_path)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Nutrition Guide Agent",
        layout="wide",
        initial_sidebar_state="collapsed")
    main()