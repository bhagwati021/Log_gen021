import pandas as pd
import random
import logging
import string
import numpy as np
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    Generate a random log entry with a timestamp,loglevel,action and user
    """
    timestamp=pd.Timestamp.now().strftime("%Y-%m-%D %H:%M:%S")
    log_level=random.choice(["INFO","DEBUG","ERROR","WARNING"])
    action=random.choice(["login","logout","Data Request","File Uplode","File Download","Error"])
    user=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}-{log_level}-{action}- User:{user}"

# Fuction to write logs to a file
def write_log_to_file(log_filename,num_entries=100):
    """
    Write the specific no of logs in the given file
    """
    try:
        with open(log_filename,'w')as file:
            for _ in range(num_entries):
                log=generate_log_entry()
                file.write(log + '\n')
        print(f"Logs have been succesfully writen in the file {log_filename}.")
    except Exception as e:
        logging.error(f"Error in writ_log_to_file: {e}")
        print("An error occured while writing log to the file.")

#function to read the log file and process it.
def load_and_process_logs(log_filename="generated_logs.txt"):
    """
    Load and process the logs from the given files,cleaning and parsing the time stamp.
    """
    try:
        # Read the log file into a pandas dataframe,splitting by the '-' separator
        df=pd.read_csv(log_filename,sep=' - ',header=None,names=["Timestamp","Log Level","Action","User"])

        # Clean and trim the space around the timestamp
        df['Timestamp']=df["Timestamp"].str.strip()
        
        # convert the timestamp column to datetime
        df["Timestamp"]=pd.to_datetime(df['Timestamp'],errors='coerce')

        # Drop rows with invalid timestamps
        df=df.dropna(subset=['timestamp'])

        if df.empty:
            print("No valid data found after timestamp conversion.")
        else:
            print("Data after timestamp conversion:")
            print(df.head())  # show the data after cleaning

        #set the Timestamp column as the index from time-based operation/calculations
        df.set_index('Timestamp',inplace=True)

        return df 

# Function to perform basic satatistical analysis using pandas and numpy
def analyze_data(df):
    """
    Perform basic analysis ,such as counting log levels and actions, and computing basic stastics such as
    """
    try:
        if df is None or df.empty:
            print ("No data available for analysis.")
            return None, None
        
        #count the occurance of each log level
        log_level_counts=df['Log_Level'].value_counts()

        #Count the occurance of each action
        action_counts=df['Action'].value_counts()

        log_count=len(df)    #total number of logs
        unique_users=df['User'].nunique()  #number of unique users
        logs_per_day=df.resample('D').size()   #number of log per day

        #averages of action per day
        average_logs_per_dat=logs_per_day.mean()

        #max logs per day
        max_logs_per_day=logs_per_day.max()

        #Display summary statistics
        print("\nLog Level Counts:\n",log_level_counts)
        print("\nAction Counts:\n",action_counts)
        print(f"\nTotal Number of Logs: {log_count}")
        print(f"\nNumber of Unique Users: {unique_users}")
        print(f"Average Logs per Day: {average_logs_per_dat:.2f}")
        print(f"Maximum Logs Per Day: {max_logs_per_day}")

        #Create a dictionary to return the analysis results
        stats={
            "Log Level Counts": log_level_counts,
            "action_counts":action_counts,
            "log_count":log_count,
            "unique_user":unique_users,
            "average_logs_per_day":average_logs_per_dat,
            "max_logs_per_day":max_logs_per_day
        }

        return stats
    except Exception as e:
        print(f"Error analysing date: {e}")
        return None
    

# function to visualize trends over time using Matplotlib
def visualize_trend(df):
    """
    visualizing log frequency trend
    """
