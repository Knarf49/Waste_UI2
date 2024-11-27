import cv2
import torch
import numpy as np

# Load the model
model_path = r"C:\Python\Kivy\Layout\best.pt"  # Replace with your model path
checkpoint = torch.load(model_path)  # Load the file
print(type(checkpoint))  # Check the type of object
if isinstance(checkpoint, dict):
    print(checkpoint.keys())  # Print keys if it's a dictionary
else:
    print("The file is not a dictionary; it might be a full model object.")

# Define preprocessing function
def preprocess(frame, input_size):
    """
    Preprocess the image for model input.
    - Resize to model input size.
    - Normalize.
    - Convert to tensor.
    """
    frame_resized = cv2.resize(frame, input_size)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    frame_normalized = frame_rgb / 255.0
    tensor = torch.tensor(frame_normalized, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0).to(device)
    return tensor

# Postprocessing function
def postprocess(output, frame):
    """
    Post-process model output to draw bounding boxes and labels on the frame.
    """
    # This depends on your model's output format. Assuming it outputs:
    # [x1, y1, x2, y2, confidence, class_index]
    for det in output:
        x1, y1, x2, y2, conf, class_idx = det
        if conf > 0.8:  # Confidence threshold
            # Draw bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            label = f"Class {int(class_idx)}: {conf:.2f}"  # Modify class mapping as needed
            cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

# Open camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Define input size based on the model's requirement
input_size = (640, 640)  # Adjust based on the model's input size

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Preprocess frame
    input_tensor = preprocess(frame, input_size)

    # Inference
    with torch.no_grad():
        output = model(input_tensor)  # Modify if your model has a specific method

    # Assuming output is a list of detections
    output = output[0].cpu().numpy()  # Convert to NumPy array for easier handling

    # Postprocess and display the frame
    frame = postprocess(output, frame)
    cv2.imshow("Object Detection", frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
