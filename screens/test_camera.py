import cv2

def test_camera():
    # ลองเปิดกล้องโดยใช้ OpenCV
    capture = cv2.VideoCapture(1)  # ลองเปลี่ยน index ตามกล้องที่เชื่อมต่อ
    if not capture.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Error: Could not read frame from the camera.")
            break

        # แสดงภาพจากกล้อง
        cv2.imshow('Camera Test', frame)

        # กด 'q' เพื่อออกจากการแสดงผล
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # ปล่อยทรัพยากรกล้องและปิดหน้าต่าง
    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()