# Rapport de projet case IA #
# Gaussian Splatting / Eye Tracking -- README

## Overview

This project explores the integration of 3D Gaussian Splatting with
VR-based eye tracking. It documents what was attempted, what worked,
what failed, and how to run the working components.

## What We Tried

- *Quaternion modification*  
  We tried changing the quaternions coming from the VR headset to make the gaze direction match the 3D Gaussian Splatting scene but the command did not work. 

- *Position modification*  
  We changed the initial position. The command worked properly. 

- *Multiple 3D Gaussian Splatting configurations*  
  We tried 2 differents 3D Gaussian Splatting (bicycle and table with objects) 

- *Scaling factor adjustments*  
  We adjusted scaling factors to match VR units with real life mouvement. The command worked properly.

- *Fusion of left/right eye videos*  
  Using the code proposed on the github XXX, we are able to generate a single video with the output videos (left and right eye).
  
- *Eye-tracking circle overlay (with color options)*  
  We added an on-screen circle to show where the user is looking. We also allowed color, size, and transparency changes. This helped us check how well the tracking matched the rendered scene. 

- *Data processing workflows*  
  Using the code given in the github XXX modified by ourself, we were able to process the data which is the output of the software. This processing allow us to add the circle at the right position.

- *VR headset configuration*  
  We set up the position captors, the HTC-vive, the joysticks and the software proposed in the github XXX. 

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
