# Rapport de projet case IA #
# Gaussian Splatting / Eye Tracking -- README

## Overview

This project explores the integration of 3D Gaussian Splatting with
VR-based eye tracking. It documents what was attempted, what worked,
what failed, and how to run the working components.

## What We Tried

- *Quaternion modification*  
  We tried changing the quaternions coming from the VR headset to make the gaze direction match the 3D Gaussian Splatting scene. We tested normalization, axis changes, and rotation adjustments. Some attempts worked, but the orientation was not always stable over time.

- *Position modification*  
  We tested different ways to convert the eye or head position into the GS coordinate system. This included simple translations, full transformation matrices, and filters to reduce shaking. The results were acceptable, but small errors remained without proper calibration.

- *Multiple 3D Gaussian Splatting configurations*  
  We tried several GS setups: standard, optimized, and versions with different density or resolution. Some worked smoothly with VR tracking, while others created delay or visual problems.

- *Scaling factor adjustments*  
  We adjusted scaling factors to match GS units (meters or millimeters) with VR units. Correct scaling was important to avoid deformation, wrong zoom levels, or depth issues.

- *Fusion of left/right eye videos*  
  We tested ways to combine the left and right eye video streams to get a single gaze point. We tried averaging, choosing the dominant eye, and interpolating between both. The results depended on the quality and timing accuracy of the input videos.

- *Eye-tracking circle overlay (with color options)*  
  We added an on-screen circle to show where the user is looking. We also allowed color, size, and transparency changes. This helped us check how well the tracking matched the rendered scene.

- *Data processing workflows*  
  We created different workflows to synchronize eye-tracking logs, video frames, and 3D transforms. This included cleaning logs, aligning timestamps, and formatting data for the GS renderer. Each version improved timing and reduced sync problems.

- *Code configuration*  
  We explored several code structures: modular files, single scripts, direct GS integration, and helper tools for transformations. The goal was to make the code easier to maintain and adapt.

- *VR headset configuration*  
  We tested different headset settings: eye-tracking calibration, tracking resets, IPD changes, distortion settings, and high-frequency capture modes. Some settings improved accuracy, while others caused timing or position issues.

## What Did Not Work (and Why)

-   Quaternion modification → command malfunction
-   Base GitHub code → only one function worked; other failed due to
    version issues and data format changes
-   Data retrieval from the software → nearly unchanged eye‑tracking
    values → likely a data‑write issue
-   Versioning mismatch in data + FFMPEG-related issues

## What Worked

-   Software installation
-   Integration of Gaussian Splatting in the VR headset
-   Initial position modification
-   Retrieval of left/right eye videos
-   Display of the eye‑tracking circle

## How to Run What Worked

1.  Use a computer with a compatible VR player input
2.  VR headset: HTC Vive or equivalent, tracking sensors, joystick
3.  Install Steam + SteamVR
4.  Ensure a room large enough for VR calibration
5.  Configure room boundaries + perform eye‑tracking calibration
6.  Launch **SRanipalRuntime**
7.  Execute the following command:

```{=html}
    C:\Users\Creactif\Documents\GaussianSplattinq\EyeNavGS_Software\EyeNavGS_Software\install\bin>
    SIBR_gaussianViewer_app_d.exe -m ../../../../bicycle/bicycle --rendering-mode 2
```
8.  Optional initial position override:

```{=html}
--initial-position X Y Z
```

## Notes

-   No response received from the GitHub project owner.
