import numpy as np
import cv2
from PIL import ImageGrab
import time
import alertzy.req as alertzy

frame_count = 0
previous_frame = None
prepared_frame = None
vid = cv2.VideoCapture("rtsp://admin:ZSDHJT@192.168.0.15/h264_stream")
isMoving = False
endTime = 0
out = None

alez = alertzy.New("zanov1i1fulmr56")

while True:
    frame_count += 1

    # 1. Load image; convert to RGB
    ret, frame = vid.read()

    if frame is not None:
        #frame = cv2.resize(frame,( 600, 400))
        #img_rgb = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2RGB)
        f = frame
        frame = frame[:1000]
        
        if ((frame_count % 2) == 0):
            # 2. Prepare image; grayscale and blur
            prepared_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
            #cv2.imshow("Video", prepared_frame)
            
        if (previous_frame is None):
            # First frame; there is no previous one yet
            previous_frame = prepared_frame
            continue
    
    
    
        # calculate difference and update previous frame
        diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
        
        previous_frame = prepared_frame

        maxV = np.amax(diff_frame)
    
            
        if maxV > 100:
            endTime = 0
            if isMoving == False:
                print("Entra una vez")
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                milliseconds = int(round(time.time() * 10000))
                out = cv2.VideoWriter('{}.mp4'.format(milliseconds), fourcc, 20.0, (1920,1080))
                alez.Send("Se detectaron movimientos","Se detectaron movimientos, video: {}.mp4".format(milliseconds), "traking")
                
            isMoving = True
            time_frame = frame_count + 100
            
            
            while time_frame > frame_count:
                ret, f = vid.read()
                out.write(f)
                frame_count += 1
                
        else:
            print("endTime", endTime)
            endTime += 1
            
            if isMoving == True and endTime > 30:
                out.release()
                isMoving = False
            

out.release()
vid.release()
cv2.destroyAllWindows()