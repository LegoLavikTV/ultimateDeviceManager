import cv2, os

cap = cv2.VideoCapture(0)

# Attempt to disable the backlight (this might not work on all cameras)
cap.set(cv2.CAP_PROP_BACKLIGHT, 0)

# Read a frame to apply the settings
ret, frame = cap.read()

# Release the camera
cap.release()

# Check if the settings were applied
if ret:
    print("Camera settings applied successfully.")
else:
    print("Failed to apply camera settings.")