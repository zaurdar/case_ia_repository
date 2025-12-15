# Data Processing and Analysis Pipeline

## Overview

In the intended pipeline, a virtual reality (VR) headset is used to collect eye-tracking saliency data while the user navigates within previously generated Gaussian Splatting (3DGS) scenes. These saliency data are then compared with the model developed during this project.

---

## Data Acquisition

To acquire the saliency data, the implementation instructions provided in the following GitHub repository were initially followed:

https://github.com/symmru/EyeNavGS_Software

However, due to issues related to the implementation of OpenXR layers on our local machine, it was not possible to generate our own eye-tracking data. As a result, we relied on the CSV files provided in the following public dataset:

https://github.com/symmru/EyeNavGS_Rutgers_Dataset

---

## Regenerating Eye-Tracking Videos

In the case of a failure or corruption during data acquisition, it is necessary to regenerate the eye-tracking videos, as these videos are required for subsequent data processing steps.

To do so, we use the `SIBR_gaussianViewer_app_d.exe` application compiled from the repository provided by symmru.

The videos can be generated using the following command:

```bash
SIBR_gaussianViewer_app_d.exe \
  -m <path_to_3DGS_scene> \
  -in <trace_file.csv> \
  --rendering-mode 4 \
  --rendering-size <width> <height>
```
### Video Rescaling
Once the video has been generated, its resolution must be adapted in order to be compatible with the data processing code.

The video can be resized using the following ffmpeg command:

```bash
ffmpeg -i "C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\user101_bicycleright.mp4" \
-vf "scale=2740:2468:flags=lanczos" \
-c:v libx264 -crf 18 -preset medium -c:a copy \
"C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\user101_bicycleright_scaled.mp4"
```
## Video Merging and Preprocessing
Once both the rescaled video and the corresponding CSV file are available, the actual data processing can begin.

After installing the dependencies listed in requirements.txt, the script add_gaze.py can be executed using the following command:

```bash
Copier le code
python add_gaze.py \
  --csv "csv_path" \
  --right "right_path" \
  --left "left_path"
```
This script generates:

a merged video containing the gaze overlay

a file named dataset.txt containing all eye-tracking data

These outputs are used in the subsequent processing steps.

## Data Analysis Methods
This repository provides two different data analysis approaches.

### Fixation Point Identification
The first approach focuses on identifying gaze fixation points and transitions in gaze dynamics.

To perform this analysis, execute the notebook fixation_id.ipynb, making sure to update the file paths accordingly.

If the execution is successful, a visualization similar to the expected output should be obtained.

### Object-Aware Saliency Analysis (YOLO)
The second analysis method is implemented in the notebook EyeGAS_yolo.ipynb.

To simplify model loading and dependency management, it is strongly recommended to run this notebook using Google Colab.

Steps:

Upload the merged video and the corresponding CSV file to Colab

Execute the notebook cells sequentially

At the end of the process, several outputs can be analyzed, such as:

the percentage of time the subject looks at a bicycle when it appears on screen

a video combining a YOLO object detector and a saliency generation model

Video Export
To download the generated video, it must be converted into a standard, browser-readable format.

This can be done using the following ffmpeg command:

```bash
ffmpeg -y \
-i "C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\output_.avi" \
-c:v libx264 -preset medium -crf 20 \
-pix_fmt yuv420p -movflags +faststart -an \
"C:\Users\hugom\OneDrive\Documents\CASE_IA\EyeNavGS_Software\utils\AddEyeGazeTracking\converted_.mp4"
```
## Summary
This pipeline enables the processing and analysis of eye-tracking saliency data within Gaussian Splatting environments, using both fixation-based metrics and object-aware saliency analysis. The resulting outputs provide quantitative and visual insights into gaze behavior relative to scene content.
