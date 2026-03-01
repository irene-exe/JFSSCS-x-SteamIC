import cv2
import time

cap = cv2.VideoCapture(0)

ret, frame_1 = cap.read()
ret, frame_2 = cap.read()


frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))


fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None

recording = False
video = 0

while True:
    diff = cv2.absdiff(frame_1, frame_2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, threshold = cv2.threshold(blur, 75, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    area = 0
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if (cv2.contourArea(contour) < 1000):
            continue 
        cv2.rectangle(frame_1, (x,y), (x+w, y+h), (0, 255, 0), 2)
        area += cv2.contourArea(contour)
        
    if (area):
        cv2.putText(frame_1, "Status: {}".format("Movement"), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        if (not recording):
            out = cv2.VideoWriter(str(video)+"output.mp4", fourcc, 60.0, (frameWidth, frameHeight))
            recording = True
        if recording and out is not None:
            out.write(frame_1)
    else:
        cv2.putText(frame_1, "Status: {}".format("Static"), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        if (recording):
            if out:
                out.release()
                video+=1
                recording = False
            out = None
    #cv2.drawContours(frame_1, contour, -1, (0, 255, 0), 2)
    
    cv2.imshow("Motion Detection", frame_1)
    frame_1 = frame_2
    
    ret, frame_2 = cap.read()
    
    if not ret:
        print("Camera failed to load.")
        break
    
    if (cv2.waitKey(1)==ord("q")):
        break
    

cv2.destroyAllWindows()