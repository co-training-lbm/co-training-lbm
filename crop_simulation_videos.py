import os
import cv2
import argparse
from tqdm import tqdm

def get_camera_box(camera_id, width):
    """
    Get the crop box for a specific camera.
    Camera layout:
    - For 1298 width (2x2 grid):
      Camera 0: top-left (6, 74, 640, 480)
      Camera 1: top-right (652, 74, 640, 480)
      Camera 2: bottom-left (6, 594, 640, 480)
      Camera 3: bottom-right (652, 594, 640, 480)
    - For 1944 width (3x2 grid):
      Camera 0: top-left (6, 74, 640, 480)
      Camera 1: top-middle (652, 74, 640, 480)
      Camera 2: top-right (1298, 74, 640, 480)
      Camera 3: bottom-left (6, 588, 640, 480)
      Camera 4: bottom-middle (652, 588, 640, 480)
      Camera 5: bottom-right (1298, 588, 640, 480)
    """
    if width == 1298:
        # 2x2 grid
        boxes = [
            (6, 74, 640, 480),    # Camera 0: top-left
            (652, 74, 640, 480),  # Camera 1: top-right
            (6, 594, 640, 480),   # Camera 2: bottom-left
            (652, 594, 640, 480), # Camera 3: bottom-right
        ]
    else:  # width == 1944
        # 3x2 grid
        boxes = [
            (6, 74, 640, 480),     # Camera 0: top-left
            (652, 74, 640, 480),   # Camera 1: top-middle
            (1298, 74, 640, 480),  # Camera 2: top-right
            (6, 588, 640, 480),    # Camera 3: bottom-left
            (652, 588, 640, 480),  # Camera 4: bottom-middle
            (1298, 588, 640, 480), # Camera 5: bottom-right
        ]
    
    if camera_id >= len(boxes):
        raise ValueError(f"Camera {camera_id} not available for width {width}. Available cameras: 0-{len(boxes)-1}")
    
    return boxes[camera_id]

def main():
    parser = argparse.ArgumentParser(description='Extract a specific camera view from simulation videos')
    parser.add_argument('--camera', type=int, default=0, choices=[0, 1, 2, 3, 4, 5],
                        help='Camera ID to extract (0-3 for 2x2 grid, 0-5 for 3x2 grid)')
    parser.add_argument('--video-dir', type=str, default='videos/simulation_unseen_tasks/',
                        help='Directory containing simulation videos')
    args = parser.parse_args()
    
    camera_id = args.camera
    video_dir = args.video_dir
    
    # Get all video files (excluding already processed cam files)
    video_files = []
    for root, dirs, files in os.walk(video_dir):
        for file in files:
            if file.endswith('.mp4') and '_cam' not in file:
                video_files.append(os.path.join(root, file))
    
    print(f"Found {len(video_files)} video files to process")
    print(f"Extracting camera {camera_id}")
    
    for video_path in tqdm(video_files, desc="Processing videos"):
        # Read video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Warning: Could not open {video_path}")
            continue
        
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Determine crop box based on video width and camera ID
        if width not in [1944, 1298] or height != 1080:
            print(f"Warning: Unexpected video size: {height}x{width} for {video_path}, skipping")
            cap.release()
            continue
        
        try:
            x, y, w, h = get_camera_box(camera_id, width)
        except ValueError as e:
            print(f"Warning: {e} for {video_path}, skipping")
            cap.release()
            continue
        
        # Create output filename
        dir_path = os.path.dirname(video_path)
        filename = os.path.basename(video_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = name_without_ext + f'_cam{camera_id}.mp4'
        output_path = os.path.join(dir_path, output_filename)
        
        # Skip if output already exists
        if os.path.exists(output_path):
            cap.release()
            continue
        
        # Create video writer with mp4v codec (will need re-encoding to H.264 later)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
        
        # Process frames
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Crop the specified camera
            crop = frame[y:y+h, x:x+w]
            out.write(crop)
            frame_count += 1
        
        cap.release()
        out.release()
        
        if frame_count == 0:
            print(f"Warning: No frames processed for {video_path}")
            if os.path.exists(output_path):
                os.remove(output_path)
    
    print(f"Done processing all videos! Camera {camera_id} extracted.")

if __name__ == '__main__':
    main()
