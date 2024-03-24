import streamlit as st
import subprocess
import pandas as pd
import os
import matplotlib.pyplot as plt

def inside_area(data):
    plates = data['License Plate Number']
    count = 0
    for plate_number in plates:
        entries = data[data['License Plate Number'] == plate_number]

        if len(entries) % 2 == 1:
            count+=1

    return f"{count} vehicles are inside the area."

def merge_data(db1, db2):

    time_window = 20

    result = pd.DataFrame(columns=['License Plate Number', 'Vehicle Type', 'Time Stamps'])
    for index, row in db1.iterrows():
        timestamp = row['Time Stamps']
        matching_rows = db2[(db2['Time Stamps'] >= timestamp - time_window) & (db2['Time Stamps'] <= timestamp + time_window)]
        if not matching_rows.empty:
            matching_row = matching_rows.iloc[0]  # Get the first matching row
            result = result.append({
                'License Plate Number': row['License Plate Number'],
                'Vehicle Type': matching_row['Vehicle Type'],
                'Time Stamps': row['Time Stamps'],  # Use db1 timestamp
                # 'Serial Number': row['Serial Number']
            }, ignore_index=True)

    return result

def types_of_vehicle_pie_chart(dataframe):
    plt.figure(figsize=(8, 6))
    dataframe['Vehicle Type'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
    plt.title('Types of Vehicle Pie Chart')
    plt.axis('equal')

    plt.savefig('pie.png', format='png')
    array = plt.imread('pie.png')
    # st.write("In func")
    return array

def number_of_unique_vehicles(dataframe):
    unique_vehicles = dataframe['License Plate Number'].nunique()
    return unique_vehicles

def most_frequent_license_plate_graph(dataframe):
    plt.figure(figsize=(10, 6))
    dataframe['License Plate Number'].value_counts().plot(kind='bar')
    plt.title('Most Frequent License Plate Graph')
    plt.xlabel('License Plate Number')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)

    plt.savefig('freq.png', format='png')
    array = plt.imread('freq.png')
    # st.write("In func")
    return array

def main():
    st.sidebar.title("Navigation")
    option = st.sidebar.selectbox("Select App", ["Select App", "License Plate Detection", "Pothole Detection", "Vehicle Detection", "View Database"])
    csv_path = None
    csv_path = st.text_input("Enter the path of the Dataframe file:")
    # print(csv_path)
    # Directory containing files
    directory = 'temp'

    if not csv_path:
        files = os.listdir(directory)
        csv_files = [f for f in files if f.endswith('.csv')]
        st.write(f"Available Databases: {csv_files}")

        csv_path = csv_files[0]
        csv_path = "temp/" + csv_path

    # Checking if vehicle detection dataset exists
    csv_path1 = "Vehicle-Detection-and-Counting-System/" + csv_path

    if csv_path:
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_path)
           
        except Exception as e:
            st.error(f"Error: {e}")

    # Checking if vehicle detection dataset exists
    csv_path1 = "Vehicle-Detection-and-Counting-System/" + csv_path
    if csv_path1:
        try:
            # Read the CSV file into a DataFrame
            df1 = pd.read_csv(csv_path1)
            DF = merge_data(df, df1)
            st.dataframe(DF)

        except Exception as e:
            st.write("### DataFrame:", csv_path)
            st.dataframe(df)
            st.error(f"Error: {e}")


    # Running functions
    st.write(inside_area(DF))
    st.write(number_of_unique_vehicles(DF))
    st.image(types_of_vehicle_pie_chart(DF))
    st.image(most_frequent_license_plate_graph(DF))
    
    
    if option == "License Plate Detection":
            subprocess.run(["streamlit", "run", "License-Plate-Detection-WebApp/src/app.py"])


    elif option == "Pothole Detection":
            subprocess.run(["streamlit", "run", "pothole-detection-using-python/app.py"])


    elif option == "Vehicle Detection":
            
        wd = os.getcwd()
        new_dir = os.path.join(wd, "Vehicle-Detection-and-Counting-System")
        os.chdir(new_dir)
        wd = os.getcwd()
        print(wd)
        subprocess.run(["streamlit", "run", "demo.py", "--server.maxUploadSize=500"])

    elif option == "View Database":
            subprocess.run(["streamlit", "run", "View-Database/app.py"])



if __name__ == "__main__":
    main()
