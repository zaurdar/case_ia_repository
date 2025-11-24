# SPDX-FileCopyrightText: 2025 Systems and Multimedia Lab @ Rutgers University
# SPDX-License-Identifier: Apache-2.0
#
# This file is part of the 👁️NavGS (EyeNavGS) project.
# See LICENSE_EYENAVGS.txt and NOTICE for details.



import numpy as np
import pandas as pd
import cv2
from scipy.spatial.transform import Rotation as R
import argparse
from tqdm import tqdm
import os

from merge_eye_vid import combine_videos_side_by_side

def parse_csv(file_path):
    """
    Parse the CSV file containing eye gaze data.
    """
    try:
        df = pd.read_csv(file_path)
    except:
        try:
            data = []
            columns = [
                "ViewIndex", "FOV1", "FOV2", "FOV3", "FOV4",
                "PositionX", "PositionY", "PositionZ",
                "QuaternionX", "QuaternionY", "QuaternionZ", "QuaternionW",
                "GazeQX", "GazeQY", "GazeQZ", "GazeQW",
                "GazePosX", "GazePosY", "GazePosZ"
            ]
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
                
                first_line = lines[0].strip().split()
                if not all(item.replace('-', '').replace('.', '').isdigit() for item in first_line):
                    lines = lines[1:]  # Skip header line
                
                for line in lines:
                    values = line.strip().split()
                    if len(values) == len(columns):
                        data.append(values)
            
            df = pd.DataFrame(data, columns=columns)
            for col in df.columns:
                if col != "ViewIndex":
                    df[col] = df[col].astype(float)
            df["ViewIndex"] = df["ViewIndex"].astype(int)
        except Exception as e:
            print(f"Error parsing CSV file: {e}")
            raise
    
    return df

def project_gaze_to_screen_openxr(row, screen_width=2160, screen_height=2224): 
    """
    Converts a 3D gaze direction into 2D screen coordinates based on OpenXR FOV values.
    Properly accounts for asymmetric FOV by adjusting the projection relative to the screen center.

    This function operates in OpenCV's coordinate system, where the origin (0,0) is at the **top-left** corner.

    Parameters:
    - row: A Pandas DataFrame row containing quaternion values for the camera and gaze, along with FOV data.
    - screen_width: The width of the screen in pixels.
    - screen_height: The height of the screen in pixels.

    Returns:
    - A list [x, y] representing the 2D screen coordinates (in pixels) of the projected gaze point.
    """
    cam_quat = [row.QuaternionX, row.QuaternionY, row.QuaternionZ, row.QuaternionW]  # Camera orientation
    gaze_quat = [row.GazeQX, row.GazeQY, row.GazeQZ, row.GazeQW]  # Eye gaze direction

    R_cam = R.from_quat(cam_quat)
    R_cam_inv = R_cam.inv()
    R_gaze = R.from_quat(gaze_quat)
    R_rel = R_cam_inv * R_gaze
    
    gaze_dir = R_rel.apply([0, 0, -1])
    
    FOV_left = row.FOV1
    FOV_right = row.FOV2
    FOV_down = row.FOV3
    FOV_up = row.FOV4
    
    # for screen-space projection
    tan_left = np.tan(FOV_left)    
    tan_right = np.tan(FOV_right)  
    tan_down = np.tan(FOV_down)    
    tan_up = np.tan(FOV_up)        

    if gaze_dir[2] < 0:
        h_ratio = gaze_dir[0] / -gaze_dir[2]
        v_ratio = gaze_dir[1] / -gaze_dir[2]

        x_normalized = (h_ratio - tan_left) / (tan_right - tan_left)
        y_normalized = 1.0 - (v_ratio - tan_down) / (tan_up - tan_down)

        screen_x = x_normalized * screen_width
        screen_y = y_normalized * screen_height
        screen_x = max(0, min(screen_x, screen_width))
        screen_y = max(0, min(screen_y, screen_height))
        screen_x = max(0, min(screen_x, screen_width))
        screen_y = max(0, min(screen_y, screen_height))
        
        return [screen_x, screen_y]
    
    else:
        # If the gaze is not directed at the screen, return the center of the screen
        return [screen_width / 2, screen_height / 2] 


def overlay_circle_with_alpha(frame, center_x, center_y, radius=5, alpha=0.8):
    """
    Overlay a hollow orange gaze marker with a soft gradient shadow.
    Inspired by VR eye-tracker challenge visualizations.

    Customizable elements:
    - radius: base radius of the orange ring
    - alpha: overall overlay strength
    - shadow_width: how far the outer gradient shadow extends
    - ring_thickness: thickness of the orange ring
    - shadow_strength: how dark the shadow looks
    """

    overlay = frame.copy()
    shadow = frame.copy()

    orange_bgr = (255, 84, 153)

    # === Customization: Shadow parameters ===
    shadow_width = 20
    shadow_strength = 0.7
    shadow_thickness = 5

    ring_thickness = 24

    for i in range(shadow_width, 0, -1):
        opacity = int(255 * (i / shadow_width) * shadow_strength)
        cv2.circle(
            shadow,
            (center_x, center_y),
            radius + i,
            (0, 0, 0, opacity),
            thickness=shadow_thickness,
            lineType=cv2.LINE_AA
        )

    overlay = cv2.addWeighted(shadow, 0.4, overlay, 0.6, 0)

    cv2.circle(
        overlay,
        (center_x, center_y),
        radius,
        orange_bgr,
        thickness=ring_thickness,
        lineType=cv2.LINE_AA
    )

    blended = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    return blended


def create_eye_videos_with_overlay(df, 
                                   left_video_path, 
                                   right_video_path, 
                                   output_prefix, 
                                   alpha=0.2):
    """
    Given two input videos (left eye and right eye), this function reads frames from each,
    computes the gaze projection for each frame, and overlays a semi-transparent red circle
    on the original frames. The modified frames are then written to new video files.
    """
    
    left_eye_data  = df[df["ViewIndex"] ==0].reset_index(drop=True)
    right_eye_data = df[df["ViewIndex"] ==1].reset_index(drop=True)
    
    print(len(left_eye_data), len(right_eye_data))
    # left-eye video
    print(left_eye_data)
    print(right_eye_data)
    left_cap = cv2.VideoCapture(left_video_path)
    left_fps = left_cap.get(cv2.CAP_PROP_FPS)
    left_width = int(left_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    left_height = int(left_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    left_frames = int(left_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # right-eye video
    right_cap = cv2.VideoCapture(right_video_path)
    right_fps = right_cap.get(cv2.CAP_PROP_FPS)
    right_width = int(right_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    right_height = int(right_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    right_frames = int(right_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"LEFT: {left_width}x{left_height}, {left_fps} fps, frames={left_frames}")
    print(f"RIGHT: {right_width}x{right_height}, {right_fps} fps, frames={right_frames}")
    # output video files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    left_eye_output = f"{output_prefix}_left_eye_overlay.mp4"
    right_eye_output = f"{output_prefix}_right_eye_overlay.mp4"
    
    left_out = cv2.VideoWriter(
        left_eye_output, 
        fourcc, 
        left_fps if left_fps > 0 else 30,
        (left_width, left_height)
    )
    right_out = cv2.VideoWriter(
        right_eye_output, 
        fourcc, 
        right_fps if right_fps > 0 else 30, 
        (right_width, right_height)
    )
    print("Opening left_out...")
    print("Opened?", left_out.isOpened())

    # Process the left-eye video

    print("Processing left eye video with overlay...")
    min_left_frames = min(left_frames, len(left_eye_data))
    for i in tqdm(range(min_left_frames)):
        ret, frame = left_cap.read()
        if not ret:
            break
        
        row = left_eye_data.iloc[i]
        # Compute the gaze projection
        screen_pos = project_gaze_to_screen_openxr(row, left_width, left_height)
        x, y = int(screen_pos[0]), int(screen_pos[1])
        
        # Overlay the semi-transparent circle on the original frame
        blended_frame = overlay_circle_with_alpha(frame, x, y, radius=200, alpha=alpha)
        
        # *Optional* add text
        cv2.putText(
            blended_frame, 
            f"Left Eye - Frame: {i}", 
            (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 0, 0), 
            2
        )
        
        left_out.write(blended_frame)
    
    # Process the right-eye video
    print("Processing right eye video with overlay...")
    min_right_frames = min(right_frames, len(right_eye_data))
    print(f"min_right frame : {min_right_frames}")
    for i in tqdm(range(min_right_frames)):
        ret, frame = right_cap.read()
        if not ret:
            break
        
        row = right_eye_data.iloc[i]
        screen_pos = project_gaze_to_screen_openxr(row, right_width, right_height)
        x, y = int(screen_pos[0]), int(screen_pos[1])
        
        blended_frame = overlay_circle_with_alpha(frame, x, y, radius=200, alpha=alpha)
        
        cv2.putText(
            blended_frame, 
            f"Right Eye - Frame: {i}", 
            (50, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 0, 0), 
            2
        )
        
        right_out.write(blended_frame)

    left_cap.release()
    right_cap.release()
    left_out.release()
    right_out.release()
    
    print(f"Left eye video saved to: {left_eye_output}")
    print(f"Right eye video saved to: {right_eye_output}")

    # Merge left and right eye videos into one final output
    merged_output_path = f"{output_prefix}_merged.mp4"
    combine_videos_side_by_side(left_eye_output, right_eye_output, merged_output_path)
    

def main():
    parser = argparse.ArgumentParser(description='Overlay gaze on existing left/right eye videos.')
    parser.add_argument('--csv', required=True, help='Path to the input CSV file with eye gaze data.')
    parser.add_argument('--left', required=True, help='Path to the input left-eye video.')
    parser.add_argument('--right', required=True, help='Path to the input right-eye video.')
    parser.add_argument('--output', '-o', default='eye_gaze', help='Output video file prefix.')
    parser.add_argument('--alpha', type=float, default=0.8, help='Transparency of the red circle overlay (0.0 - 1.0).')
    args = parser.parse_args()
    print(args)
    print(f"Parsing CSV file: {args.csv}")
    cols = [
    "ViewIndex","FOV1","FOV2","FOV3","FOV4",
    "PositionX","PositionY","PositionZ",
    "QuaternionX","QuaternionY","QuaternionZ","QuaternionW",
    "GazeQX","GazeQY","GazeQZ","GazeQW",
    "GazePosX","GazePosY","GazePosZ",
    "Extra1","Extra2","Extra3","Extra4","Extra5"
]

    # 1) Lire le CSV proprement
    df = pd.read_csv(
        "figurines_splatting_output_0.csv",
        names=cols,        # écraser header du CSV
        header=0,          # sauter première ligne
        engine="python"
    )
    
    # 2) Conversion des colonnes numériques
    float_cols = [
        "FOV1","FOV2","FOV3","FOV4",
        "PositionX","PositionY","PositionZ",
        "QuaternionX","QuaternionY","QuaternionZ","QuaternionW",
        "GazeQX","GazeQY","GazeQZ","GazeQW",
        "GazePosX","GazePosZ",
        "Extra1","Extra3","Extra5"
    ]
    
    int_cols = [
        "ViewIndex",
        "Extra2"   # identifiant type timestamp brut
    ]
    
    # Colonnes timestamp
    datetime_cols = [
        "GazePosY",  # contient l’heure version datetime
        "Extra4"     # timestamp ISO8601
    ]
    
    # Conversion
    df[float_cols] = df[float_cols].apply(pd.to_numeric, errors="coerce")
    df[int_cols]   = df[int_cols].apply(pd.to_numeric, errors="coerce").astype("Int64")
    df[datetime_cols] = df[datetime_cols].apply(pd.to_datetime, errors="coerce")

    
    create_eye_videos_with_overlay(
        df,
        args.left,
        args.right,
        args.output,
        alpha=args.alpha
    )


if __name__ == "__main__":
    main()