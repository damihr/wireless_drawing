import cv2
import mediapipe as mp
import numpy as np
import math
import joblib
import os

# --- Setup mediapipe ---
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

# Try to load custom gesture model
gesture_model = None
if os.path.exists("asl_model.joblib"):
    gesture_model = joblib.load("asl_model.joblib")
    print("✅ Custom gesture model loaded!")
else:
    print("ℹ️ No custom gesture model found — using basic gestures.")

# --- Canvas setup ---
canvas = None
prev_points = {}

# --- Utility functions ---
def count_extended_fingers(lm):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    for tip in tips[1:]:  # skip thumb
        if lm[tip].y < lm[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)

def is_pinch_gesture(lm, w, h, threshold=0.05):
    """Detect if thumb and index finger are pinching together"""
    # Get thumb tip (landmark 4) and index finger tip (landmark 8)
    thumb_tip = np.array([lm[4].x, lm[4].y])
    index_tip = np.array([lm[8].x, lm[8].y])
    
    # Calculate distance (normalized coordinates)
    distance = np.linalg.norm(thumb_tip - index_tip)
    
    # Pinch if distance is below threshold
    return distance < threshold

def get_hand_surface_points(lm, w, h):
    """Get points that represent the hand surface for erasing (mop effect)"""
    # Get palm center and key points
    palm_center = (int(lm[9].x * w), int(lm[9].y * h))  # Middle finger MCP
    wrist = (int(lm[0].x * w), int(lm[0].y * h))
    
    # Get finger base points (MCP joints)
    index_mcp = (int(lm[5].x * w), int(lm[5].y * h))
    middle_mcp = (int(lm[9].x * w), int(lm[9].y * h))
    ring_mcp = (int(lm[13].x * w), int(lm[13].y * h))
    pinky_mcp = (int(lm[17].x * w), int(lm[17].y * h))
    
    # Get finger tips (even if closed, they help define the hand shape)
    index_tip = (int(lm[8].x * w), int(lm[8].y * h))
    middle_tip = (int(lm[12].x * w), int(lm[12].y * h))
    ring_tip = (int(lm[16].x * w), int(lm[16].y * h))
    pinky_tip = (int(lm[20].x * w), int(lm[20].y * h))
    
    # Create a polygon that covers the hand surface
    # Use MCP joints and tips to form the erasing area
    points = np.array([
        wrist,
        index_mcp,
        index_tip,
        middle_tip,
        ring_tip,
        pinky_tip,
        pinky_mcp,
        wrist
    ], np.int32)
    
    return points, palm_center

# --- Webcam loop ---
cap = cv2.VideoCapture(0)
print("🎨 Draw=Pinch (thumb+index) | Fist=Erase (mop) | C=Clear canvas | Q=Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    if canvas is None:
        canvas = np.zeros_like(frame)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    if res.multi_hand_landmarks:
        for hand_idx, hand_landmarks in enumerate(res.multi_hand_landmarks):
            lm = hand_landmarks.landmark
            x8, y8 = int(lm[8].x * w), int(lm[8].y * h)
            fingers_up = count_extended_fingers(lm)
            is_pinch = is_pinch_gesture(lm, w, h)

            # --- Modes ---
            if is_pinch:
                # Draw mode: pinch gesture (thumb and index finger together)
                # Use midpoint between thumb and index finger for smoother drawing
                thumb_tip_x = int(lm[4].x * w)
                thumb_tip_y = int(lm[4].y * h)
                index_tip_x = int(lm[8].x * w)
                index_tip_y = int(lm[8].y * h)
                
                # Midpoint for drawing
                draw_x = (thumb_tip_x + index_tip_x) // 2
                draw_y = (thumb_tip_y + index_tip_y) // 2
                
                if hand_idx not in prev_points:
                    prev_points[hand_idx] = (draw_x, draw_y)
                cv2.line(canvas, prev_points[hand_idx], (draw_x, draw_y), (0, 0, 255), 5)
                prev_points[hand_idx] = (draw_x, draw_y)

            elif fingers_up == 0:
                # Erase mode: fist (all fingers closed) - use hand surface as mop
                hand_points, palm_center = get_hand_surface_points(lm, w, h)
                
                # Draw filled polygon to erase (mop effect)
                cv2.fillPoly(canvas, [hand_points], (0, 0, 0))
                
                # Also add circles at key points for smoother erasing
                cv2.circle(canvas, palm_center, 40, (0, 0, 0), -1)
                
                # Clear previous point for this hand
                prev_points.pop(hand_idx, None)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    combined = cv2.addWeighted(frame, 0.5, canvas, 1, 0)
    cv2.putText(combined, "Draw=Pinch | Fist=Erase (mop) | C=Clear | Q=Quit",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Smart Air Draw 🖌️", combined)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c') or key == ord('C'):
        # Clear canvas with 'c' key
        canvas = np.zeros_like(frame)
        prev_points.clear()
        cv2.putText(combined, "🧼 Canvas cleared!", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        cv2.imshow("Smart Air Draw 🖌️", combined)
        cv2.waitKey(500)  # Show message for 500ms

cap.release()
cv2.destroyAllWindows()
