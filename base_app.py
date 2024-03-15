import streamlit as st
import subprocess
import pandas as pd
from PIL import Image

def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Select App", ["Select App", "License Plate Detection", "Pothole Detection", "Vehicle Detection", "View Database"])

    # st.title("Base Streamlit App")
    # st.write("Upload an image or video on the sidebar and select an app to run.")

    # uploaded_file = st.sidebar.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4"])
    # csv_path = st.text_input("Enter the path of the Dataframe file:")

    # if csv_path:
    #     try:
    #         # Read the CSV file into a DataFrame
    #         df = pd.read_csv(csv_path)

    #         # Display the DataFrame using Streamlit DataFrame component
    #         st.write("### DataFrame:", csv_path)
    #         st.dataframe(df)
    #     except Exception as e:
    #         st.error(f"Error: {e}")

    # if uploaded_file is not None:
    #     print(uploaded_file.name)
    #     _, file_extension = uploaded_file.name.split(".")
    #     if file_extension.lower() in ["jpg", "jpeg", "png"]:
    #         image = Image.open(uploaded_file)
    #         st.sidebar.image(image, caption='Uploaded Image/Video', use_column_width=True)
    #     elif file_extension.lower() == "mp4":
    #         st.sidebar.video(uploaded_file)

    if option == "License Plate Detection":
            subprocess.run(["streamlit", "run", "License-Plate-Detection-WebApp/src/app.py"])


    elif option == "Pothole Detection":
            subprocess.run(["streamlit", "run", "pothole-detection-using-python/app.py"])


    elif option == "Vehicle Detection":
            subprocess.run(["streamlit", "run", "Vehicle-Detection-and-Counting-System/demo.py", "--server.maxUploadSize=500"])

    elif option == "View Database":
            subprocess.run(["streamlit", "run", "View-Database/demo.py"])



if __name__ == "__main__":
    main()
