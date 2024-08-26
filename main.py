"""import os
import subprocess
import glob
import time
from datetime import datetime, timedelta
import psutil



def process_vrs_files(subject_directory, username, password):
    # Iterate over all sessions
    for session_num in range(1, 9):  # Sessions range from 1 to 8
        session_str = f"sess{session_num:02d}"
        vrs_file_path = os.path.join(subject_directory, f"subj11_{session_str}.vrs")
        mps_folder_name = f"mps_subj11_{session_str}_vrs"
        eye_gaze_path_pattern = os.path.join(subject_directory, mps_folder_name, "eye_gaze", "*")
        
        print(f"Checking session: {vrs_file_path}")
        
        if glob.glob(eye_gaze_path_pattern):
            print(f"Skipping already processed session: {vrs_file_path}")
            continue
        
        print(f"Processing VRS file: {vrs_file_path}")

        # Construct the aria_mps single command
        command = [
            "aria_mps",
            "single",
            "--input", vrs_file_path,
            "--username", username,
            "--password", password,
            "--features", "EYE_GAZE"
        ]

        # Run the command as a subprocess
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Set the start time for the timer
        start_time = datetime.now()
        timeout = timedelta(hours=2)  # 2 hour timeout
        
        # Wait until the eye_gaze folder appears or timeout occurs
        eye_gaze_found = False
        while not eye_gaze_found:
            eye_gaze_dirs = glob.glob(eye_gaze_path_pattern)
            
            if eye_gaze_dirs:
                eye_gaze_found = True
                print(f"Found 'eye_gaze' folder. Terminating process for: {vrs_file_path}")
                break
            else:
                elapsed_time = datetime.now() - start_time
                if elapsed_time > timeout:
                    print(f"Timeout reached. Terminating process for: {vrs_file_path}")
                    break
                time.sleep(5)  # Wait for 5 seconds before checking again
        
        # Terminate the aria_mps process if it's still running
        try:
            parent = psutil.Process(process.pid)
            for child in parent.children(recursive=True):
                child.terminate()
            process.terminate()
            print(f"Process terminated for: {vrs_file_path}")
        except psutil.NoSuchProcess:
            print(f"No process found to terminate for: {vrs_file_path}")
"""    

import os
import subprocess
import glob

def process_vrs_files(subject_directory, username, password, max_duration):
    # Iterate over all VRS files in the directory
    for session_num in range(1, 2):  # Sessions range from 1 to 8
        session_str = f"sess{session_num:02d}"
        vrs_file_path = os.path.join(subject_directory, f"subj35_{session_str}.vrs")
        mps_folder_name = f"mps_subj35_{session_str}_vrs"
        eye_gaze_path_pattern = os.path.join(subject_directory, mps_folder_name, "eye_gaze", "*")
        
        print(f"Checking session: {vrs_file_path}")
        
        if glob.glob(eye_gaze_path_pattern):
            print(f"Skipping already processed session: {vrs_file_path}")
            continue
        
        print(f"Processing VRS file: {vrs_file_path}")

        # Construct the aria_mps single command
        command = [
            "aria_mps",
            "single",
            "--input", vrs_file_path,
            "--username", username,
            "--password", password,
            "--features", "EYE_GAZE"
        ]

        try:
            # Run the command and wait for it to complete, with a timeout
            result = subprocess.run(command, capture_output=True, text=True, timeout=max_duration)
            if result.returncode == 0:
                print(f"Successfully processed: {vrs_file_path}")
            else:
                print(f"Failed to process: {vrs_file_path}")
                print(result.stderr)
        except subprocess.TimeoutExpired:
            print(f"Processing timed out for: {vrs_file_path}")

if __name__ == "__main__":
    vrs_directory = "/Users/lunachen/Movies/VRS/subj35"
    username = "upenn_rxd1ec"
    password = "upenn0001"
    max_duration = 16 * 60 * 60  # 2 hours in seconds

    process_vrs_files(vrs_directory, username, password, max_duration)
