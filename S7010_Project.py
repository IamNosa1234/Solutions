import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Stabilization variables
stabilization_count = 0
stabilization_threshold = 5  # Number of consecutive frames with palm detected

def capture():
    global stabilization_count
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for a natural selfie-view display
        frame = cv2.flip(frame, 1)

        # Detect hand gestures
        if shutter_gesture(frame):
            stabilization_count += 1
            if stabilization_count >= stabilization_threshold:
                cv2.imwrite("photo.jpg", frame)
                print("Photo captured via palm gesture!")
                break
        else:
            stabilization_count = 0  # Reset if gesture not consistently detected

        # Show camera preview
        cv2.imshow("Camera Preview", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("photo.jpg", frame)
            print("Photo captured via key press!")
            break

    cap.release()
    cv2.destroyAllWindows()
    img = cv2.imread("photo.jpg")
    cv2.imshow("Photo", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def calculate_distance(point1, point2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

def calculate_angle(a, b, c):
    # Calculate the angle between points a, b, and c using the cosine rule
    ba = [a.x - b.x, a.y - b.y]  # Vector from b to a
    bc = [c.x - b.x, c.y - b.y]  # Vector from b to c
    dot_product = ba[0] * bc[0] + ba[1] * bc[1]  # scaled distance between a and b and c
    magnitude_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
    magnitude_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)
    if magnitude_ba * magnitude_bc == 0:
        return 0
    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)
    angle = math.acos(cosine_angle)
    return math.degrees(angle)

def shutter_gesture(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Check angles for each finger using landmarks for finger joints
            angles = []
            for finger in [
                [mp_hands.HandLandmark.INDEX_FINGER_MCP, mp_hands.HandLandmark.INDEX_FINGER_PIP, mp_hands.HandLandmark.INDEX_FINGER_DIP],
                [mp_hands.HandLandmark.MIDDLE_FINGER_MCP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, mp_hands.HandLandmark.MIDDLE_FINGER_DIP],
                [mp_hands.HandLandmark.RING_FINGER_MCP, mp_hands.HandLandmark.RING_FINGER_PIP, mp_hands.HandLandmark.RING_FINGER_DIP],
                [mp_hands.HandLandmark.PINKY_MCP, mp_hands.HandLandmark.PINKY_PIP, mp_hands.HandLandmark.PINKY_DIP],
            ]:
                mcp = hand_landmarks.landmark[finger[0]]
                pip = hand_landmarks.landmark[finger[1]]
                dip = hand_landmarks.landmark[finger[2]]

                angle = calculate_angle(mcp, pip, dip)
                angles.append(angle)

            # Define a threshold for the angles to detect open fingers
            open_finger_threshold = 160  # Angle threshold for open fingers
            open_fingers = [angle > open_finger_threshold for angle in angles]

            # Check if all four fingers are open (thumb is not considered)
            is_hand_open = all(open_fingers)

            # Draw landmarks on the frame for feedback
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            return is_hand_open

    return False


capture()
