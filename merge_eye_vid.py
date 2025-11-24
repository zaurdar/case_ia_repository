# SPDX-FileCopyrightText: 2025 Systems and Multimedia Lab @ Rutgers University
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of the 👁️NavGS (EyeNavGS) project.
# See LICENSE_EYENAVGS.txt and NOTICE for details.



import cv2
from pathlib import Path
from tqdm import tqdm
import subprocess

def fix_mp4_with_ffmpeg(input_path: Path, output_path: Path):
    """
    Use ffmpeg to make MP4 streamable and compatible with most players.
    """
    cmd = f'ffmpeg -i {str(input_path)} -c:v libx264 -pix_fmt yuv420p -movflags +faststart -r 30 {str(output_path)}'
    print(f"Running ffmpeg to fix MP4 compatibility:\n{' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def combine_videos_side_by_side(left_video_path, right_video_path, output_path):
    import cv2
    from pathlib import Path
    from tqdm import tqdm
    import subprocess

    # Output path setup
    output_path = Path(output_path)
    temp_raw_output = output_path.with_name(output_path.stem + "_raw.mp4")

    left_cap = cv2.VideoCapture(str(left_video_path))
    right_cap = cv2.VideoCapture(str(right_video_path))

    width = int(left_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(left_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = left_cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(min(left_cap.get(cv2.CAP_PROP_FRAME_COUNT), right_cap.get(cv2.CAP_PROP_FRAME_COUNT)))

    # Output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_size = (width * 2, height)
    out = cv2.VideoWriter(str(temp_raw_output), fourcc, fps, output_size)

    print(f"Combining {frame_count} frames...")
    for _ in tqdm(range(frame_count)):
        ret_l, frame_l = left_cap.read()
        ret_r, frame_r = right_cap.read()
        if not ret_l or not ret_r:
            break

        combined_frame = cv2.hconcat([frame_l, frame_r])
        out.write(combined_frame)

    left_cap.release()
    right_cap.release()
    out.release()
    print(f"Combined video saved to: {output_path}")

    fix_mp4_with_ffmpeg(temp_raw_output, output_path)

    # Optional: remove temp file
    #temp_raw_output.unlink(missing_ok=True)

    print(f"Final combined video saved to: {output_path}")

if __name__ == "__main__":
    # Example usage — update these paths to match your video output
    left_video = Path(r"C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\figurines_splatting_left.mp4")
    right_video = Path(r"C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\figurines_splatting_right.mp4")
    output_video = Path(r"C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\playroom_trace_0_combined.mp4")

    combine_videos_side_by_side(left_video, right_video, output_video)
