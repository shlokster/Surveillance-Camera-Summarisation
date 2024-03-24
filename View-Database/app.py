import streamlit as st
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2
from datetime import datetime, timedelta


def check_vehicle_status(data, plate_number):
    entries = data[data['License Plate Number'] == plate_number]

    if len(entries) % 2 == 1:
        return f"Vehicle {plate_number} hasn't left the area."

# Function to calculate the number of vehicles that entered during a time period
def calculate_entries_in_time_period(data, start_time, end_time):
    entries_in_period = data[(data['Time Stamps'] >= start_time) & (data['Time Stamps'] <= end_time)]
    num_entries = len(entries_in_period['License Plate Number'].unique())
    return num_entries

# Function to get all details of a given license plate number
def get_vehicle_details(data, plate_number):
    details = data[data['License Plate Number'] == plate_number]
    return details


def movement_rate(data):
    # Convert the timestamps to datetime objects
    hourly_movement = data.groupby('Time Stamps').size()

    # Plot the data
    plt.figure(figsize=(10, 6))
    hourly_movement.plot(kind='bar', color='skyblue')
    plt.title('Vehicle Movement Rate')
    plt.xlabel('Frame')
    plt.ylabel('Number of Vehicle Entries')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.savefig('plot.png', format='png')
    array = plt.imread('plot.png')
    # st.write("In func")
    return array

def avg_time_spent(data):
  # Group the dataset by license plate number
  grouped_data = data.groupby('License Plate Number')

  # Initialize lists to store time spent in entry
  time_spent_in_entry = []

  # Iterate over groups to calculate time spent in entry for each vehicle
  for _, group in grouped_data:
      entry_times = group['Time Stamps'].iloc[::2]  # Get entry times (1st occurrence)
      exit_times = group['Time Stamps'].iloc[1::2]  # Get exit times (2nd occurrence)

      # Calculate time spent in entry for each vehicle
      for entry_time, exit_time in zip(entry_times, exit_times):
          time_spent_in_entry.append((exit_time - entry_time).total_seconds())

  # Calculate the average time spent in entry
  average_time_spent = sum(time_spent_in_entry) / len(time_spent_in_entry)

  return average_time_spent

def get_frame(data, video_path, plate_number):

    st.write("In func")
    frame = data[data['License Plate Number'] == plate_number]
    frame_number = frame['Time Stamps'][0]

    # st.write(video_path)
    try:
        cap = cv2.VideoCapture(video_path)
    except:
        st.write("File")

    # Set the frame number to extract
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if ret:
        # Release the video capture object
        cap.release()
        frame = np.array(frame)
        return frame
    else:
        print(f"Error: Unable to extract frame {frame_number}.")

    # Release the video capture object
    cap.release()   
    

def main():
    # st.sidebar.title("Navigation")
    # option = st.sidebar.selectbox("Select App", ["Select App", "License Plate Detection", "Pothole Detection", "Vehicle Detection", "View Database"])

    csv_path = st.text_input("Enter the path of the Dataframe file:")
    video_path = csv_path.split('.csv')[0]
    if csv_path:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_path)

            # Display the DataFrame using Streamlit DataFrame component
            # st.write("### DataFrame:", csv_path)
            st.dataframe(df)
        except Exception as e:
            pass

    plate_number = st.text_input("Enter the numberplate for details:")

    if plate_number:
        try:
            st.write(check_vehicle_status(df, plate_number))
            st.dataframe(get_vehicle_details(df, plate_number))
            st.write(f"Number of vehicles between the time period of {10} - {180}: {calculate_entries_in_time_period(df, 10, 180)}")
            st.image(movement_rate(df))
            st.image(get_frame(df, video_path, plate_number))
        except Exception as e:
            pass


    # if option == "License Plate Detection":
    #         subprocess.run(["streamlit", "run", "/../License-Plate-Detection-WebApp/src/app.py"])


    # elif option == "Pothole Detection":
    #         subprocess.run(["streamlit", "run", "/../pothole-detection-using-python/app.py"])


    # elif option == "Vehicle Detection":
    #         subprocess.run(["streamlit", "run", "/../Vehicle-Detection-and-Counting-System/demo.py", "--server.maxUploadSize=500"])

    # elif option == "View Database":
    #         subprocess.run(["streamlit", "run", "View-Database/demo.py", "--server.maxUploadSize=500"], cwd="/")



if __name__ == "__main__":
    main()