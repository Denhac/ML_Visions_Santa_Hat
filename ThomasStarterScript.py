import cv2
import random
import numpy as np
import time
import threading

cv2.namedWindow("projector", cv2.WINDOW_NORMAL)
cv2.moveWindow("projector", 1536, 0)  # Move to HDMI-1 (right of eDP-1)
cv2.setWindowProperty("projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Show camera preview so user can position camera
cv2.namedWindow("camera_preview", cv2.WINDOW_NORMAL)
print("Camera preview window open. Position camera to see the projector area.")
print("Press Enter in the camera preview window when ready to start calibration.")

temp_cap = cv2.VideoCapture("/dev/video0")
while True:
    ret, frame = temp_cap.read()
    if ret:
        cv2.imshow("camera_preview", frame)
    # Check for Enter key in terminal (non-blocking)
    key = cv2.waitKey(30) & 0xFF
    if key == 13:  # Enter key
        break
temp_cap.release()
cv2.destroyWindow("camera_preview")
print("Starting calibration...")



# bufferless VideoCapture
class VideoCapture:
    """ this class stolen from stackoverflow
        # Source - https://stackoverflow.com/a
        # Posted by Bruno Degomme, modified by community. See post 'Timeline' for change history
        # Retrieved 2025-11-16, License - CC BY-SA 4.0
        # Modified: fixed race condition by storing latest frame in variable
    """
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.lock = threading.Lock()
        self.running = True
        self.latest_frame = None
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.latest_frame = frame
            else:
                break

    # retrieve latest frame
    def read(self):
        with self.lock:
            return self.latest_frame.copy() if self.latest_frame is not None else None

    def release(self):
        self.running = False
        self.t.join(timeout=1.0)
        self.cap.release()


cam = VideoCapture("/dev/video0")

def calibrate(window,cam,proj_size=(1920-100,1080-100)):
    cv2.waitKey(30)
    w,h = proj_size 
    radius = int(min(w,h)*0.05)

    pre = []
    positions = []

    for _ in range(10):
        print("snapping clear image")
        buffer = np.zeros([h,w,3],dtype=np.uint8)
        cv2.imshow(window,buffer)
        cv2.waitKey(2000)
        

        normal = cam.read().copy()


        print("drawing circle")
        pos = (int(random.random()*w*0.9+w*0.05), int(random.random()*h*0.9+h*0.05))
        cv2.circle(buffer,
                   center=pos,
                   radius=radius,
                   color=(255,255,255),
                   thickness=-1
        )
        cv2.imshow(window,buffer)
        cv2.waitKey(2000)

       
        frame = cam.read().copy()

        #cv2.imshow("normal",normal)
        #cv2.imshow("frame",frame)

        diff = (((normal + 0.0) - (frame + 0.0))**2).sum(axis=-1)**0.5

        diff = diff / diff.sum()

        #x_est = (diff.sum(axis=1)*np.arange(diff.shape[0])).sum()

        #y_est = (diff.sum(axis=0)*np.arange(diff.shape[1])).sum()

        x_est = diff.sum(axis=1).argmax()

        y_est = diff.sum(axis=0).argmax()

        pre.append(pos[::-1])
        positions.append([x_est,y_est])
        print(x_est,y_est)


    transform = np.linalg.lstsq(
            np.hstack([np.array(pre)[:,::-1],np.ones(len(pre))[:,None]]),
            np.array(positions)[:,::-1]
    ) 
    return transform[0]



transform = calibrate("projector",cam)

print("Calibration complete! Live feed starting on projector...")
print("Press 'q' in the monitor window or Ctrl+C in terminal to quit.")

# Re-ensure fullscreen on projector
cv2.setWindowProperty("projector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Monitor window on laptop screen
cv2.namedWindow("monitor", cv2.WINDOW_NORMAL)

prev = None
try:
    while True:
        frame = cam.read()
        if frame is None:
            print("Warning: No frame from camera")
            continue
        maybe = cv2.warpAffine(frame,transform.T,(1920-100,1080-100),flags=cv2.WARP_INVERSE_MAP)
        if prev is not None:
            draw = maybe * 0.25 + prev * 0.75
        else:
            draw = maybe

        prev = maybe.copy()
        cv2.imshow("projector", draw.astype(np.uint8))
        cv2.imshow("monitor", draw.astype(np.uint8))  # Show on laptop too
        key = cv2.waitKey(250) & 0xFF
        if key == ord('q'):
            break
except KeyboardInterrupt:
    print("\nStopping...")

cam.release()
cv2.destroyAllWindows()

