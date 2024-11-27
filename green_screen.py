import cv2
import numpy as np

def process_green_screen(input_path, output_path):
    """
    Removes the green background from the input video and saves the processed video.
    """
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Save as MP4
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the green screen color range
        lower_green = np.array([35, 55, 55])  # Adjust for your green screen
        upper_green = np.array([85, 255, 255])

        # Create a mask for green color
        mask = cv2.inRange(hsv, lower_green, upper_green)

        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Apply the mask to remove green
        bg_removed = cv2.bitwise_and(frame, frame, mask=mask_inv)

        out.write(bg_removed)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
