import os
import cv2
from tqdm import tqdm

frame_dir = 'extracted_frames/'
save_dir = 'cropped_frames/'

task_list = os.listdir(frame_dir)
for task_name in tqdm(task_list):
    task_path = os.path.join(frame_dir, task_name)
    ds_flag_list = os.listdir(task_path)
    for ds_flag in ds_flag_list:
        video_path = os.path.join(task_path, ds_flag)
        video_files = os.listdir(video_path)
        for video_file in video_files:
            video_file_path = os.path.join(video_path, video_file)
            frame_list = os.listdir(video_file_path)
            
            for frame_name in frame_list:
                frame_path = os.path.join(video_file_path, frame_name)
                img = cv2.imread(frame_path)
                h, w, _ = img.shape
                assert w in [1944, 1298] and h == 1080, f"Unexpected frame size: {h}x{w}"

                if w == 1298:
                    boxes = [
                        (6,   74, 640, 480),
                        (652, 74, 640, 480),
                        (6,   594, 640, 480),
                        (652, 594, 640, 480),
                    ]
                else:
                    boxes = [
                        (6, 74, 640, 480),
                        (652, 74, 640, 480),
                        (1298, 74, 640, 480),
                        (6, 588, 640, 480),
                        (652, 588, 640, 480),
                        (1298, 588, 640, 480),
                    ]

                out_path = os.path.join(save_dir, task_name, ds_flag, video_file)
                os.makedirs(out_path, exist_ok=True)
                for i, (x, y, w, h) in enumerate(boxes):
                    crop = img[y:y+h, x:x+w]
                    cv2.imwrite(os.path.join(out_path, frame_name.split('.')[0] + f'_{i}.jpg'), crop)