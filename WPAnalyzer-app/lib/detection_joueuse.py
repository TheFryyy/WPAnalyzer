# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:03:02 2020

@author: garni
"""

import cv2 as cv
import numpy as np
import json

class Detection_joueuse: 
    
    def __init__(self, low_HSV, high_HSV, low_HSV_ball, high_HSV_ball, path_video):
        self.low_HSV = low_HSV
        self.high_HSV = high_HSV
        self.low_HSV_ball = low_HSV_ball
        self.high_HSV_ball = high_HSV_ball
        self.path_video = path_video

    
    def show_video(self):
        video = cv.VideoCapture(self.path_video)
        ret, frame = video.read()
        kernel_ouverture = np.ones((4,4),np.uint8)
        kernel_dilatation = np.ones((6,6),np.uint8)
        size = (1920,1080)
        out = cv.VideoWriter('./output/output.avi',cv.VideoWriter_fourcc(*'DIVX'), 15, size)
        data = {}
        data["frameArray"]= []
        
        while(video.isOpened() and ret):
            
            image_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(image_HSV, self.low_HSV, self.high_HSV)
            mask_ouvert = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel_ouverture)
            mask_dilate = cv.dilate(mask_ouvert,kernel_dilatation,iterations = 12)
            contours= cv.findContours(mask_dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            contours = select_contour(contours, 4000, 50000)
            centers = get_center_of_contour(contours, frame)
            cv.drawContours(frame,contours, -1, (0,0,255), 2)
            ball_position = get_ball_position(self.low_HSV_ball, self.high_HSV_ball, kernel_ouverture, kernel_dilatation, frame)
            cv.imshow('Video',frame)
            out.write(frame)
            centers = arrange_data(centers)
            write_data(data, centers, ball_position)
            ret, frame = video.read()
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
        video.release()
        out.release()
        cv.destroyAllWindows()
        with open('./output/data.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False, sort_keys = True, indent=3)


def get_ball_position(low_HSV_ball, high_HSV_ball, kernel_ouverture, kernel_dilatation, frame) : #renvoie la position du ballon
    res = []
    image_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(image_HSV, low_HSV_ball, high_HSV_ball)
    mask_ouvert = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel_ouverture)
    mask_dilate = cv.dilate(mask_ouvert,kernel_dilatation,iterations = 12)
    contours= cv.findContours(mask_dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    contours = select_contour(contours, 0, 7000)
    centers = get_center_of_contour(contours, frame)
    for center in centers :
        if center[1] > 200 and center[1] < 900 :
            res += [center]
    if (len(res) == 0) :
        res = [-1, -1]
    else :
        res = res[0]
    cv.circle(frame, (res[0], res[1]), 13, (0, 0, 255), -1)
    return res
    
def select_contour(contours, min, max): #filtre les contours
    res = []
    for contour in contours :
        if cv.contourArea(contour) < max and cv.contourArea(contour) > min :
            res += [contour]
    return res

def get_center_of_contour(contours,frame) : #le nom est plutôt explicite
    res = []
    for contour in contours :
        M = cv.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        #cv.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        res.append([cX, cY])
    return res

def arrange_data(centers) : #Fais en sorte qu'il y'ait exactement 16 joueuses. Remplis avec des coordonnées (-1, -1) si besoin
    size = len(centers)
    if size >= 16 :
        res = centers[:16]
    else :
        diff = 16 - size
        res = centers + diff*[[-1, -1]]
    return res

def write_data(data, centers, ball_position) : #ecris en format JSON
    playerArray = {}
    playerArray["opponentArray"] = []
    playerArray["allyArray"] = []
    playerArray["ball"] = []
    for i in range(8) :
        coords = {"coords": centers[i]}
        playerArray["opponentArray"].append(coords)
    
    for i in range(8,16) :
        coords = {"coords": centers[i]}
        playerArray["allyArray"].append(coords)
    coords = {"coords": ball_position}
    playerArray["ball"].append(coords)
    data["frameArray"].append(playerArray)
