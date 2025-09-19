#Importamos librerias
import cv2 as cv
import numpy as np
#import matplotlib.pyplot as plt
import os

#imagenes a procesar
def process_qr_image(img_path) :


    if not os.path.exists(img_path + ".jpg"):
        print("La imagen no existe en el bancod de imagenes")
        return
    

    img1=cv.imread(img_path + ".jpg")
    gray=cv.cvtColor(img1,cv.COLOR_BGR2GRAY) #convertir imagen a escala de grises

    _, mask = cv.threshold(gray, 100, 255, cv.THRESH_BINARY) #aplicar mascara pero binaria

    #aplicar blur para difuminar aspectos extras
    mask_blur = cv.GaussianBlur(mask, (3,3), 0)

    #aplicar erosion y dilatación para resaltar bien las lineas del qr
    kernel = np.ones((5,5), np.uint8)
    mask_erode = cv.erode(mask_blur, kernel, iterations=1)   # Erosión
    mask_dilate = cv.dilate(mask_erode, kernel, iterations=2) # Dilatación

    #aplicar metodos para resaltar los bordes del qr
    laplacian = cv.Laplacian(mask_dilate, cv.CV_64F)
    sobelx = cv.Sobel(mask_dilate, cv.CV_64F, 1, 0, ksize=5)
    sobely = cv.Sobel(mask_dilate, cv.CV_64F, 0, 1, ksize=5)

    #invertir colores de la imagen procesada
    thresh = cv.bitwise_not(mask_dilate)
    cv.imwrite(img_path + "_filtrado" + ".jpg", thresh)
    print("Imagen guardada :D")

def main() : #menu principal
    print("Introduce que imagen quieres ")
    ruta=input().strip()
    process_qr_image(ruta)

main()
