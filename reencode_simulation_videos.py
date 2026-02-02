import os
import subprocess
from tqdm import tqdm

video_dir = 'videos/simulation_unseen_tasks/'

# Get all cam video files (cam0, cam2, etc.)
video_files = []
for root, dirs, files in os.walk(video_dir):
    for file in files:
        if '_cam' in file and file.endswith('.mp4'):
            video_files.append(os.path.join(root, file))

print(f"Found {len(video_files)} video files to re-encode")

for video_path in tqdm(video_files, desc="Re-encoding videos"):
    # Create temporary output path
    temp_path = video_path + '.temp'
    
    # Re-encode to H.264 using ffmpeg
    # Explicitly specify output format and handle special characters in filename
    cmd = [
        'ffmpeg', '-i', video_path,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-movflags', '+faststart',
        '-f', 'mp4',  # Explicitly specify output format
        '-y',  # Overwrite output file
        temp_path
    ]
    
    try:
        # Run ffmpeg silently
        result = subprocess.run(cmd, capture_output=True, check=True)
        
        # Replace original with re-encoded version
        os.replace(temp_path, video_path)
    except subprocess.CalledProcessError as e:
        print(f"Error re-encoding {video_path}: {e.stderr.decode()}")
        # Clean up temp file if it exists
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        if os.path.exists(temp_path):
            os.remove(temp_path)

print("Done re-encoding all videos!")

