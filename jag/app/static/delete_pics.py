import os
import glob

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Script directory: {script_directory}")

# Define the folder path relative to the script's location
folder_path = os.path.join(script_directory, 'images')

# Print the full path of the folder being searched
print(f"Full path to the folder being searched: {folder_path}")

# Use glob to find all .png files in the specified folder (not subfolders)
png_files = glob.glob(os.path.join(folder_path, '*.png'))

# Print the number of .png files found
print(f"Number of .png files found: {len(png_files)}")

# Loop through and delete each .png file (limiting to 5 for safety)
i = 0
for file in png_files:
    i += 1
    # if i > 1500:
    #     print("Reached limit of 1500 deletions for safety. Stopping.")
    #     break
    try:
        # print(f"Attempting to delete: {file}")
        os.remove(file)
        # print(f"Deleted: {file}")
    except Exception as e:
        print(f"Error deleting {file}: {e}")
print(f'Deleted {i} files')
