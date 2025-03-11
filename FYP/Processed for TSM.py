import os
import shutil
import pandas as pd

# Paths
DATASET_PATH = r"D:\FYP_\Datasets\DCSASS Dataset"
LABELS_PATH = os.path.join(DATASET_PATH, "Labels")
OUTPUT_PATH = r"D:\FYP_\Processed_DCSASS"

# Ensure output path exists
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Process each label file
for label_file in os.listdir(LABELS_PATH):
    if label_file.endswith(".csv"):
        label_file_path = os.path.join(LABELS_PATH, label_file)
        print(f"Processing {label_file_path}...")  # Debugging

        # Read CSV correctly
        df = pd.read_csv(label_file_path, delimiter=",", header=None, names=["clip_name", "class", "label"])
        df.dropna(inplace=True)
        df["label"] = df["label"].astype(int)

        # Process each row
        for _, row in df.iterrows():
            clip_name = row["clip_name"] + ".mp4"  # Ensure correct format
            class_name = row["class"]
            label = row["label"]

            # Find the correct path (check inside main video folders)
            class_path = os.path.join(DATASET_PATH, class_name)
            found = False

            # Search for the clip inside video folders
            for video_folder in os.listdir(class_path):
                video_folder_path = os.path.join(class_path, video_folder)
                clip_path = os.path.join(video_folder_path, clip_name)

                if os.path.exists(clip_path):  
                    found = True
                    # Create destination folder based on class and label
                    dest_folder = os.path.join(OUTPUT_PATH, class_name, "Activity" if label == 1 else "No_Activity")
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.copy(clip_path, os.path.join(dest_folder, clip_name))
                    print(f"Copied: {clip_path} -> {dest_folder}")  # Debugging
                    break  # Stop searching once found
            
            if not found:
                print(f"❌ Clip not found: {clip_name} in {class_path}")  # Debugging

print("Processing complete.")
