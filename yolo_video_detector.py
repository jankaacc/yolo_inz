from capture_manager import VideoCaptureManager, VideoCaptureRecognizer
import tensorflow as tf
from keras import backend as K



if __name__ == '__main__':
    
    config = tf.ConfigProto()
    #config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.5
    K.tensorflow_backend.set_session(tf.Session(config=config))
    
    with VideoCaptureManager(device_nr=0, output_size=(224,224)) as cap:     
            cap.capture()
