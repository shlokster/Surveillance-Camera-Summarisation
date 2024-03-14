import streamlit as st
import subprocess
from PIL import Image

def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Select App", ["License Plate Detection", "Pothole Detection", "Vehicle Detection"])

    st.title("Base Streamlit App")
    st.write("Upload an image or video on the sidebar and select an app to run.")

    uploaded_file = st.sidebar.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4"])

    if uploaded_file is not None:
        _, file_extension = uploaded_file.name.split(".")
        if file_extension.lower() in ["jpg", "jpeg", "png"]:
            image = Image.open(uploaded_file)
            st.sidebar.image(image, caption='Uploaded Image/Video', use_column_width=True)
        elif file_extension.lower() == "mp4":
            st.sidebar.video(uploaded_file)

    if option == "License Plate Detection":
        if uploaded_file is not None:
            if file_extension.lower() in ["jpg", "jpeg", "png"]:
                st.image(image, caption='Uploaded Image/Video', use_column_width=True)
            elif file_extension.lower() == "mp4":
                st.video(uploaded_file)
            subprocess.run(["streamlit", "run", "License-Plate-Detection-WebApp/src/app.py"])
        else:
            st.warning("Please upload an image or video.")

    elif option == "Pothole Detection":
        if uploaded_file is not None:
            if file_extension.lower() in ["jpg", "jpeg", "png"]:
                st.image(image, caption='Uploaded Image/Video', use_column_width=True)
            elif file_extension.lower() == "mp4":
                st.video(uploaded_file)
            subprocess.run(["streamlit", "run", "pothole-detection-using-python/app.py"])
        else:
            st.warning("Please upload a video.")

    elif option == "Vehicle Detection":
        if uploaded_file is not None:
            if file_extension.lower() in ["jpg", "jpeg", "png"]:
                st.image(image, caption='Uploaded Image/Video', use_column_width=True)
            elif file_extension.lower() == "mp4":
                st.video(uploaded_file)
            subprocess.run(["streamlit", "run", "Vehicle_Detection_and_Counting_System/demo.py", "--server.maxUploadSize=500"])
        else:
            st.warning("Please upload an image or video.")


if __name__ == "__main__":
    main()
