import os
import subprocess
from projectaria_tools.core import data_provider
from projectaria_tools.core.stream_id import StreamId
from PIL import Image

def extract_first_images(subject_directory):
    # Iterate over all sessions
    for session_num in range(1, 9):  # Sessions range from 1 to 8
        session_str = f"sess{session_num:02d}"
        vrs_file_path = os.path.join(subject_directory, f"subj14_{session_str}.vrs")
        output_dir = os.path.splitext(vrs_file_path)[0] + "_extracted"
        image_file_path = os.path.join(output_dir, "rgb_0.jpg")
        
        if os.path.exists(image_file_path):
            print(f"Skipping already extracted image: {image_file_path}")
            continue

        print(f"Extracting first image from VRS file: {vrs_file_path}")
        extract_first_image(vrs_file_path, image_file_path)

def extract_first_image(vrs_file_path, image_file_path):
    output_dir = os.path.dirname(image_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

        # Initialize DataProvider
    provider = data_provider.create_vrs_data_provider(vrs_file_path)
    
    # Get the stream ID for the RGB camera
    stream_id = StreamId("214-1")

    # Extract and save images from the RGB camera stream
    image_data = provider.get_image_data_by_index(stream_id, 0)

    image_array = image_data[0].to_numpy_array()
    image_file_path = os.path.join(output_dir, f"rgb.jpg")
    save_image(image_array, image_file_path)
    print(f"Saved image: {image_file_path}")

def save_image(image_array, file_path):
    image = Image.fromarray(image_array)
    image.save(file_path)

if __name__ == "__main__":
    subject_directory = "/Users/lunachen/Movies/VRS/subj14"
    extract_first_images(subject_directory)
