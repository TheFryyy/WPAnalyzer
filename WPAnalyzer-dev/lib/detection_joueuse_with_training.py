# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 18:03:02 2020

@author: garni
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
import math
import uuid
from contrastive_loss_keras.pyimagesearch_contrastive.siamese_network import build_siamese_model
from contrastive_loss_keras.pyimagesearch_contrastive import utils
from contrastive_loss_keras.pyimagesearch_contrastive import metrics
from contrastive_loss_keras.pyimagesearch_contrastive import config
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Lambda
import glob

class Detection_joueuse: 
    
    def __init__(self, low_HSV, high_HSV, low_HSV_ball, high_HSV_ball, path_video, path_weights):
        self.low_HSV = low_HSV
        self.high_HSV = high_HSV
        self.low_HSV_ball = low_HSV_ball
        self.high_HSV_ball = high_HSV_ball
        self.path_video = path_video
        self.path_weights = path_weights


    def create_model(self) :
        imgA = Input(shape=config.IMG_SHAPE)
        imgB = Input(shape=config.IMG_SHAPE)
        featureExtractor = build_siamese_model(config.IMG_SHAPE)
        featsA = featureExtractor(imgA)
        featsB = featureExtractor(imgB)
        distance = Lambda(utils.euclidean_distance)([featsA, featsB])
        model = Model(inputs=[imgA, imgB], outputs=distance)
        model.compile(loss=metrics.contrastive_loss, optimizer="adam")
        model.load_weights(self.path_weights)
        self.model = model

    
    def show_video(self):
        video = cv.VideoCapture(self.path_video)
        ret, frame = video.read()
        kernel_ouverture = np.ones((4,4),np.uint8)
        kernel_dilatation = np.ones((6,6),np.uint8)
        size = (1920,1080)
        out = cv.VideoWriter('../output/output.avi',cv.VideoWriter_fourcc(*'DIVX'), 15, size)
        data = {}
        data["frameArray"]= []
        flag = True
        last_centers = []
        last_labels = []
        cycle = 0
        
        while(video.isOpened() and ret):
            
            image_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            mask = cv.inRange(image_HSV, self.low_HSV, self.high_HSV)
            #image_seuil = cv.bitwise_and(frame, frame, mask = mask)
            mask_ouvert = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel_ouverture)
            mask_dilate = cv.dilate(mask_ouvert,kernel_dilatation,iterations = 12)
            #image_seuil_ouvert = cv.bitwise_and(frame, frame, mask = mask_ouvert)
            #image_seuil_dilate = cv.bitwise_and(frame, frame, mask = mask_dilate)
            contours= cv.findContours(mask_dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            contours = select_contour(contours, 4000, 50000)
            #pixels = pixels_from_contours(contours, frame)
            #masks = masks_from_contours(contours, frame)
            #cimg = cv.bitwise_and(frame, frame, mask = masks[3])
            #colors_in_contour(pixels[0]) 
            #show_bounding_rect(contours, frame)
            #bounding_rect = get_bounding_rect(contours, frame)
            #labels = get_number_of_players(self.model, bounding_rect)
            centers = get_center_of_contour(contours, frame)
            #labels = get_labels(centers, last_centers, last_labels, flag)
            #show_labels(frame, centers, labels)
            cv.drawContours(frame,contours, -1, (0,0,255), 2)
            ball_position = get_ball_position(self.low_HSV_ball, self.high_HSV_ball, kernel_ouverture, kernel_dilatation, frame)
            #last_centers = centers
            #last_labels = labels
            #image_positions = show_positions(centers, ball_position)
            cv.imshow('Video',frame)
            out.write(frame)
            centers = arrange_data(centers)
            write_data(data, centers, ball_position)
            ret, frame = video.read()
            flag = False
            cycle += 1
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        
        video.release()
        out.release()
        cv.destroyAllWindows()
        with open('../output/data.json', 'w', encoding='utf-8') as outfile:
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

def show_area(contours) :
    area = list(map(lambda contour: cv.contourArea(contour), contours))
    area.sort()
    print(area)

def show_bounding_rect(contours, frame) : #montre les bounding rectangle autour des contours
    for contour in contours :
        x,y,w,h = cv.boundingRect(contour)
        cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

def get_bounding_rect(contours, frame) : #met les images des bounding rectangle dans une liste
    res = []
    for contour in contours :
        x,y,w,h = cv.boundingRect(contour)
        bounding_rect = frame[y:y+h, x:x+w]
        resized_bounding_rect = cv.resize(bounding_rect, (128,128), interpolation = cv.INTER_AREA)
        res += [resized_bounding_rect]
    return res
        
def save_bouding_rect(contours, frame) : #sauvegarde les bounding rectangle autour des contours
    for contour in contours :
        x,y,w,h = cv.boundingRect(contour)
        bounding_rect = frame[y:y+h, x:x+w]
        resized_bounding_rect = cv.resize(bounding_rect, (128,128), interpolation = cv.INTER_AREA)
        filename = str(uuid.uuid4())
        cv.imwrite("contrastive-loss-keras/examples/" + filename + ".png", resized_bounding_rect)

def pixels_from_contours(contours, frame): #renvoie le nombre de pixel dans un contour
    res = []
    for i in range(len(contours)):
        cimg = np.zeros_like(frame)
        cv.drawContours(cimg, contours, i, color=255, thickness=-1)
        pts = np.where(cimg == 255)
        res.append(frame[pts[0], pts[1]])
    return res

def colors_in_contour(pixels): #montre un graphe de la couleur des pixels
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=pixels[:,2], ys=pixels[:,1], zs=pixels[:,0], s=2, lw=0)
    ax.set_xlabel('H')
    ax.set_ylabel('S')
    ax.set_zlabel('V')
    ax.view_init(60, 0)
    plt.show()
    
def masks_from_contours(contours, frame) :
    res = []
    for i in range(len(contours)):
        cimg = np.zeros_like(frame)
        cv.drawContours(cimg, contours, i, color=(255,255,255), thickness=-1)
        cimg = cv.cvtColor(cimg, cv.COLOR_BGR2GRAY)
        res.append(cimg)
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

def get_closest_label(center, last_centers, last_labels) : #récupère le label le plus proche dans la frame précédente
    closest_distance = 9999999
    for i in range(len(last_centers)) :
        distance = math.sqrt((last_centers[i][0]-center[0])**2 + (last_centers[i][1]-center[1])**2)
        if distance < closest_distance :
            closest_distance = distance
            closest_label = last_labels[i]
    return closest_label
    
def get_labels(centers, last_centers, last_labels, flag) : #récupère les labels de la frame précédente
    if flag :
        return range(len(centers))
    else :
        res = []
        for center in centers :
            res.append(get_closest_label(center, last_centers, last_labels))
        return res
        

def show_labels(frame, centers, labels) : #montre les labels
    for i in range(len(centers)) :
        cv.putText(frame, str(labels[i]), tuple(centers[i]), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        
def get_number_of_players(model, images) : #renvoie le nombre de joueuses dans chaque image avec le modèle des réseaux siamois
    res = []
    for image in images :
        filenames = glob.glob("../input/data_test/0_player/*.png")
        path = np.random.choice(filenames)
        image0 = cv.imread(path)
        filenames = glob.glob("../input/data_test/1_player/*.png")
        path = np.random.choice(filenames)
        image1 = cv.imread(path)
        filenames = glob.glob("../input/data_test/2_players/*.png")
        path = np.random.choice(filenames)
        image2 = cv.imread(path)
        filenames = glob.glob("../input/data_test/3+_players/*.png")
        path = np.random.choice(filenames)
        image3 = cv.imread(path)
        
       	image = np.expand_dims(image, axis=0)
       	image0 = np.expand_dims(image0, axis=0)
        image1 = np.expand_dims(image1, axis=0)
        image2 = np.expand_dims(image2, axis=0)
        image3 = np.expand_dims(image3, axis=0)
        
       	image = np.array(image) / 255.0
       	image0 = np.array(image0) / 255.0
        image1 = np.array(image1) / 255.0
        image2 = np.array(image2) / 255.0
        image3 = np.array(image3) / 255.0

       	preds = model.predict([image, image0])
       	distance0 = preds[0][0]
        preds = model.predict([image, image1])
       	distance1 = preds[0][0]
        preds = model.predict([image, image2])
       	distance2 = preds[0][0]
        preds = model.predict([image, image3])
       	distance3 = preds[0][0]

        distances = [distance0, distance1, distance2, distance3]
        number_of_player = distances.index(min(distances))
        res += [number_of_player]
    return res

def show_positions (centers, ball) :
    imres = np.zeros((1080,1920,3), np.uint8)
    for center in centers :
        cv.circle(imres, (center[0], center[1]), 5, (255, 255, 255), -1)
    cv.circle(imres, (ball[0], ball[1]), 7, (0, 0, 255), -1)
    return imres

    

