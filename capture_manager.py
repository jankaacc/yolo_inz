import cv2
import numpy as np
from PIL import Image
from yolo import YOLO
from timeit import default_timer as timer


class VideoCaptureManager():
    
    def __init__(self, device_nr, output_size):
        self.device_nr = device_nr
        self.output_size = output_size
        
    def __enter__(self):
         self.cap = VideoCaptureRecognizer(self.device_nr)
         
         if (self.cap.isOpened() == False): 
            print("Unable to read camera feed")
            return -1
        
         return self.cap
        
    def __exit__(self, exctype, value, tb):
        self.cap.release()
        cv2.destroyAllWindows()
        return False
    
        
class VideoCaptureRecognizer(cv2.VideoCapture):

    def __init__(self, device_nr):
        super(VideoCaptureRecognizer, self).__init__(device_nr)
        self.yolo = YOLO()
        
    def capture(self):
        accum_time = 0
        curr_fps = 0
        fps = "FPS: ??"
        prev_time = timer()
        while(True):
            ret, frame = self.read() 
            if ret:
                image = Image.fromarray(frame, 'RGB')
                image = self.yolo.detect_image(image)
                img_array = np.array(image)
                cv2.imshow('frame', img_array)  
                
                curr_time = timer()
                exec_time = curr_time - prev_time
                prev_time = curr_time
                accum_time = accum_time + exec_time
                curr_fps = curr_fps + 1
                if accum_time > 1:
                    accum_time = accum_time - 1
                    fps = "FPS: " + str(curr_fps)
                    curr_fps = 0
                print(fps)
    
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        self.yolo.close_session()
        
        
