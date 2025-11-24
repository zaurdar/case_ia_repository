# Rapport de projet case IA #
# Gaussian Splatting / Eye Tracking -- README

## Overview

This project explores the integration of 3D Gaussian Splatting with
VR-based eye tracking. It documents what was attempted, what worked,
what failed, and how to run the working components.

## What We Tried

-   Quaternion modification
-   Position modification
-   Multiple 3D Gaussian Splatting configurations
-   Scaling factor adjustments
-   Fusion of left/right eye videos
-   Addition of an eye‑tracking circle overlay (with color editing)
-   Data processing workflows
-   Code configuration
-   VR headset configuration

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
