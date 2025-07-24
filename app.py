from flask import Flask, render_template, Response, request, jsonify
from Camera import Camera 
import cv2
import lampControl
import mechanum # Import the entire mechanum module
import math

app = Flask(__name__)

# --- Robot State ---
# Store the current speed percentage, updated by the frontend slider.
current_speed_percent = 50

my_camera = Camera()
my_camera.camera_open()

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    """Generates video frames with a speed overlay."""
    global current_speed_percent
    
    while True:
        frame = my_camera.frame
        if frame is None:
            continue

        # --- Add Speed Overlay ---
        # Define text properties for the speed display
        speed_text = f"Speed: {current_speed_percent}%"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        color = (0, 255, 0) # Green color in BGR
        thickness = 2
        position = (15, 40) # Position on the frame (x, y)

        # Draw the text onto the frame
        cv2.putText(frame, speed_text, position, font, font_scale, color, thickness, cv2.LINE_AA)
        
        # Encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", frame)

        # Ensure the frame was successfully encoded
        if not flag:
            continue

        # Yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')
@app.route('/video_feed')
def video_feed():
    """Video streaming route that calls the generator."""
    return Response(gen_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/control', methods=['POST'])
def control():
    global current_speed_percent
    data = request.get_json()
    command = data.get('command')
    value = data.get('value')

    print(f"Received command: {command}, value: {value}, speed: {current_speed_percent}%")

    # --- Speed Control ---
    if command == 'speed':
        current_speed_percent = int(value)
        print(f"Speed set to: {current_speed_percent}%")
    
    # --- Light Bar Control ---
    elif command == 'light_bar':
        if value == 'on':
            lampControl.lampOn(lampControl.LAMP_COLOR)
            print("Lamp turned ON")
        else:
            lampControl.lampOff()
            print("Lamp turned OFF")

    # --- Movement Control ---
    elif command == 'move':
        # NOTE: Using a small time value (0.1) for continuous movement.
        # The frontend will send 'stop' when the button is released.
        move_time = 0.5
        if value == 'forward':
            # Corrected function call from 'forward' to 'moveForward'
            mechanum.moveForward(current_speed_percent, move_time)
            print("Moving forward")
        elif value == 'backward':
            # Corrected function call from 'backward' to 'moveBackward'
            mechanum.moveBackward(current_speed_percent, move_time)
            print("Moving backward")
        elif value == 'left':
            # Corrected function call from 'left' to 'moveLeft'
            mechanum.moveLeft(current_speed_percent, move_time)
            print("Strafing left")
        elif value == 'right':
            # Corrected function call from 'right' to 'moveRight'
            mechanum.moveRight(current_speed_percent, move_time)
            print("Strafing right")
        elif value == 'stop':
            # The stop function is correct
            mechanum.stop()
            print("Movement stopped")

    # --- Turning Control ---
    elif command == 'turn':
        # NOTE: Using 'turn' function with positive/negative speed.
        turn_time = 0.1
        if value == 'left':
            # Corrected to use 'turn' with a negative speed
            mechanum.turn(-current_speed_percent, turn_time)
            print("Turning left")
        elif value == 'right':
            # Corrected to use 'turn' with a positive speed
            mechanum.turn(current_speed_percent, turn_time)
            print("Turning right")
        elif value == 'stop':
            # The stop function is correct
            mechanum.stop()
            print("Turning stopped")
            
    # --- Gimbal Control (Placeholder) ---
    elif command == 'gimbal':
        if value == 'left':
            print("Pivoting gimbal left")
        elif value == 'right':
            print("Pivoting gimbal right")
        elif value == 'stop':
            print("Gimbal stopped")

    # This will now return a valid JSON response, preventing the client-side error.
    return jsonify(status="success", command=command, value=value)


@app.route('/update_speed', methods=['POST'])
def update_speed():
    data = request.get_json()
    speed_percent = int(data.get('speed'))

    # Calculate velocity, RPM, and FPS using mechanum functions
    fb_velocity = mechanum.sepVel(speed_percent)
    if fb_velocity is None:
        fb_velocity = 0

    rpm = mechanum.getRPM(fb_velocity)
    fps = fb_velocity / 304.8

    return jsonify(rpm=rpm, fps=fps)

if __name__ == '__main__':
    # Initialize the robot motor pins on startup
    try:
        mechanum.init()
        print("✅ Motor pins initialized successfully.")
    except Exception as e:
        print(f"⚠️  Could not initialize motor pins: {e}")
        print("Running in simulation mode without GPIO control.")

    app.run(debug=True, host='0.0.0.0')
