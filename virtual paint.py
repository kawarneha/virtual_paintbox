import cv2
import numpy as np

def find_color(image ,hsv_colors ,bgr_colours):
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)                         
    for i, colour in enumerate(hsv_colours):
        lower = np.array(colour[:3])
        upper = np.array(colour[3:])
        img = cv2.inRange(img_hsv, lower, upper)                            
        x, y = get_contours(img)

        if(x!= 0 and y!= 0):                                               
            points.append((x, y, i))
        draw_on_canvas(points,bgr_colours)

def get_contours(img):
    contours,hierarchy = cv2.findContours(img ,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)                                                       
        if(area > 250):
            peri = cv2.arcLength(cnt, True)
            corners = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x,y,w,h = cv2.boundingRect(corners)
    return (x+ w//2,y) 


def draw_on_canvas(points, bgr_colours):
    for point in points:
        cv2.circle(final_image ,(point[0] ,point[1]) ,5 ,bgr_colours[point[2]] ,cv2.FILLED)

        
width ,height=5000,4000
points=[]


hsv_colours = [[0, 50, 50, 10, 255, 255],              #red
             [94, 80, 2, 126, 255, 255],               #blue
             [0, 0, 0, 180, 255, 30],                  #black
             [138, 22, 85, 179, 127, 255],             #pink
             [20, 100, 100, 30, 255, 255]]             #yellow
             
bgr_colours = [[0, 0, 255],                             #red
             [255, 0, 0],                               #blue
             [0, 0, 0],	                                #black
             [203,192,255],                             #pink
             [0, 255, 255]]                             #yellow
              
captured = cv2.VideoCapture(0)                          #camera by default
captured.set(4, width)                                  #width
captured.set(5, height)                                 #height
captured.set(10, 130)                                   #brightness


while True:
    success , image = captured.read()
    if not success:
        print("error occured while capturing the video")
        break
    
    final_image = image.copy()
    find_color(image, hsv_colours, bgr_colours)                                  
    cv2.imshow('Your Virtual Paint Box :)', final_image)
    if(cv2.waitKey(1) & 0XFF == ord('q')):                #press "q" to exit
        break
