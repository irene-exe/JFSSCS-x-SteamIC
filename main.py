import cv2
import os
import time
from datetime import datetime

cap = cv2.VideoCapture(0)

ret, frame_1 = cap.read()
ret, frame_2 = cap.read()


frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

recording = False
start_time = 0
filename = ""

def delete_old_files(delete_time):
    for file in os.listdir("/Users/irenewang/Code/github/JFSSCS-x-SteamIC/saved_videos"):
        filename = os.fsdecode(file)
        if (filename==".DS_Store"):
            continue
        upload_date = datetime.strptime(filename[:-4], "%b %d %y %H:%M:%S")
        upload_time = time.mktime(upload_date.timetuple())
        if (time.time()-upload_time>delete_time):
            os.remove("saved_videos/"+filename)
    

while True:
    diff = cv2.absdiff(frame_1, frame_2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, threshold = cv2.threshold(blur, 95, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if (cv2.contourArea(contour) < 1000):
            continue 
        cv2.rectangle(frame_1, (x,y), (x+w, y+h), (0, 255, 0), 2)
        area += cv2.contourArea(contour)
        
    if (area):
        cv2.putText(frame_1, "Status: Movement", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        if (not recording):
            start_time = time.time()
            filename = "saved_videos/" + datetime.fromtimestamp(start_time).strftime("%b %d %y %H:%M:%S") + ".mp4"
            out = cv2.VideoWriter(filename, fourcc, 20.0, (frameWidth, frameHeight))
            recording = True
        if recording and out is not None:
            out.write(frame_1)
    else:
        cv2.putText(frame_1, "Status: Static", (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        if (recording):
            if out:
                out.release()
                recording = False
                duration = time.time() - start_time
                print(duration)
                if duration < 3:
                    if (filename and os.path.exists(filename)):
                        os.remove(filename)
            out = None
    #cv2.drawContours(frame_1, contour, -1, (0, 255, 0), 2)
    
    cv2.imshow("Motion Detection", frame_1)
    frame_1 = frame_2
    ret, frame_2 = cap.read()
    
    if(datetime.second!=0 and int(datetime.strftime(datetime.now(),"%S"))%10):
        delete_old_files(60)
    
    if not ret:
        print("Camera failed to load.")
        break
    
    if (cv2.waitKey(1)==ord("q")):
        break
    

cv2.destroyAllWindows()