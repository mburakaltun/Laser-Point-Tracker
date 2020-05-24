import cv2
import numpy as np
import time
import serial

arduino = serial.Serial(port='/dev/cu.usbmodem14101', baudrate=9600)
time.sleep(2)
print("Connected to Arduino...")

cap = cv2.VideoCapture(0)
print("Getting camera image...")

horizontal_center_of_the_frame = cap.get(3) / 2
vertical_center_of_the_frame = cap.get(4) / 2

horizontal_servo_position = 90
vertical_servo_position = 180

current_horizontal_value = int(horizontal_center_of_the_frame)
current_vertical_value = int(vertical_center_of_the_frame)

while True:
    _, frame = cap.read()
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #green
    low = np.array([58, 204, 219])
    high = np.array([101, 255, 255])

    #blue
    #low = np.array([110, 50, 50])
    #high = np.array([130, 255, 255])

    #red
    #low = np.array([161, 155, 84])
    #high = np.array([179, 255, 255])

    laser = cv2.inRange(hsv_frame, low, high)

    contours, _ = cv2.findContours(laser, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    x = 0
    y = 0
    w = 0
    h = 0
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        current_horizontal_value = int((x + x + w) / 2)
        current_vertical_value = int((y + y + h) / 2)

        if current_horizontal_value > horizontal_center_of_the_frame + 60:
            horizontal_servo_position -= 2
        if current_horizontal_value < horizontal_center_of_the_frame - 60:
            horizontal_servo_position += 2
        if current_vertical_value > vertical_center_of_the_frame + 60:
            vertical_servo_position += 2
        if current_vertical_value < vertical_center_of_the_frame - 60:
            vertical_servo_position -= 2

        if horizontal_servo_position <= 0:
            horizontal_servo_position = 0
        if horizontal_servo_position >= 180:
            horizontal_servo_position = 180
        if vertical_servo_position <= 0:
            vertical_servo_position = 0
        if vertical_servo_position >= 90:
            vertical_servo_position = 0

        data = "X{0:d}Y{1:d}Z".format(horizontal_servo_position, vertical_servo_position)
        arduino.write(data.encode())
        #print(current_vertical_value, " - ", current_horizontal_value)
        break

    cv2.line(frame, (current_horizontal_value, 0), (current_horizontal_value, 720), (0, 255, 0), 1)
    cv2.line(frame, (0, current_vertical_value), (1280, current_vertical_value), (0, 255, 0), 1)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)

    print(vertical_servo_position, " - ", horizontal_servo_position)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()