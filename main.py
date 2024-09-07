import cv2
import subprocess
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Initialize the webcam feed.
cap = cv2.VideoCapture(0)

# STEP 1: Create the BaseOptions with the path to the model asset.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')

# STEP 2: Create GestureRecognizerOptions using the base options.
options = vision.GestureRecognizerOptions(base_options=base_options)

# STEP 3: Create the GestureRecognizer from options.
recognizer = vision.GestureRecognizer.create_from_options(options)

# Initialize MediaPipe Image API.
mp_image = mp.Image
anaconda_prompt = r'start cmd /K "C:\Users\<username>\anaconda3\Scripts\activate.bat"'
whatsapp=r'start cmd /K "C:\Program Files\WindowsApps\<path to your whatsapp application>\WhatsApp.exe"'
# A set to track if a command was already executed for a gesture
executed_commands = set()
anaconda_prompt_opened = False

def open_app_windows(app_name):
    """Function to open apps based on the recognized gesture."""
    global anaconda_prompt_opened
    
    try:
        if app_name == "chrome":
            subprocess.Popen('start chrome', shell=True)
        elif app_name == "explorer":
            subprocess.Popen('explorer', shell=True)  # File Explorer
        elif app_name == "whatsapp":
            subprocess.Popen(whatsapp, shell=True)  # Replace with actual path
        elif app_name == "anaconda prompt":
            if not anaconda_prompt_opened:
                subprocess.Popen(anaconda_prompt, shell=True)
                anaconda_prompt_opened = True
        elif app_name == "MS_Edge":
            subprocess.Popen('start msedge',shell=True)        
        print(f"Attempted to open {app_name}")
    except Exception as e:
        print(f"Error opening {app_name}: {str(e)}")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the image to the format required by MediaPipe (RGB).
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # STEP 4: Create an mp.Image object from the webcam frame.
    mp_frame_image = mp_image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # STEP 5: Run gesture recognition on the current frame.
    gesture_result = recognizer.recognize(mp_frame_image)

    # STEP 6: Check and act on the recognized gestures.
    if gesture_result.gestures:  # If gestures are detected
        for gesture_list in gesture_result.gestures:
            if gesture_list:  # Check if the list is not empty
                # Get the name of the first gesture in the list
                gesture_name = gesture_list[0].category_name
                
                # Print out the exact gesture name detected
                print(f"Detected Gesture: {gesture_name}")  # Debugging gesture name

                # Display gesture name on the frame.
                cv2.putText(frame, f'Gesture: {gesture_name}', (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # STEP 7: Trigger system commands based on gestures.
                if gesture_name == "Thumb_Up" and 'chrome' not in executed_commands:
                    print("Thumbs Up detected, launching Chrome...")
                    open_app_windows('chrome')
                    executed_commands.add('chrome')
                elif gesture_name == "Thumb_Down" and 'explorer' not in executed_commands:
                    print("Thumbs Down detected, launching File Explorer...")
                    open_app_windows('explorer')
                    executed_commands.add('explorer')
                elif gesture_name == "Victory" and 'whatsapp' not in executed_commands:
                    print("Victory detected, launching WhatsApp...")
                    open_app_windows('whatsapp')
                    executed_commands.add('whatsapp')
                elif gesture_name == "Open_Palm" and 'anaconda' not in executed_commands:
                    print("Open Palm detected, launching Anaconda Prompt...")
                    open_app_windows('anaconda prompt')
                    executed_commands.add('anaconda prompt')

                elif gesture_name == "Closed_Fist" and 'MS_Edge' not in executed_commands:
                    print("Open Palm detected, launching MS_Edge...")
                    open_app_windows('MS_Edge')
                    executed_commands.add('MS_Edge')    
                
                else:
                    print(f"No command triggered for gesture: {gesture_name}")  # Fallback for unrecognized gestures

    # Show the camera feed with gesture recognition results.
    cv2.imshow('Hand Gesture Recognition', frame)

    # Press 'q' to exit the webcam window.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close OpenCV windows.
cap.release()
cv2.destroyAllWindows()
