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

CAMERA_ID = 0 #Id de la cámara, la del equipo es 0, por que es solo una cámara
DELAY = 1 #Delay de la cámara
WINDOW_NAME = "Lector de QR's"
QR_D = cv.QRCodeDetector() #Inializa la detección de QR's
CAP = cv2.VideoCapture(CAMERA_ID) #Inicializa la fuente de video

def read_qr_image(img_path) :
    #Leemos el código QR procesado y guardado
    processed_img = cv.imread(img_path)
    """
    Detectamos y decodificamos la imagen procesada en busca del QR
    Se asignan los siguientes valores a las siguientes variables dependiendo del input:
    - retval: Booleano, True si detecta por lo menos un código QR, none si no
    - decoded_info: TUpla cuyos elementos son strings de los QR; si se detectan pero no se decodifican será un string vació
    - points: Array de las coordenadas de las cuatro esquinas del QR
    - plain_qr_code: Tupla de arrays, valores binarios de 0 a 255 que representan los blancos y negros de cada celda de un QR
    """
    retval, decoded_info, points, plain_qr_code = QR_D.detectAndDecodeMulti(processed_img)
    """
    Añade un borde de color azul a la imagen del QR, si es que se detectó
    Inputs:
    - processed_img: imagen ya procesada con el posible QR
    - points.astype(int): Las coordenadas de las cuatro esquinas del QR convertidas a enteros
    - True: Indíca que queremos el borde cerrando el QR
    - (0, 255, 0): Tupla que determina el color de linea del borde, azul en formato BGR
    - 3: Anchura de linea del borde
    """
    framed_qr = cv2.polylines(processed_img, points.astype(int), True, (255, 0, 0), 3)
    """
    Iteramos por cada QR tanto por información decodificada como por cada punto de las esquinas del QR para añadirles texto
    Variables del loop:
    - s: Strings decodificados del QR
    - p: Coordenadas de la primera esquina del QR, se busca colocar el texto al inicio de esta
    - processed_img: Imagen del QR donde se colocará el texto
    Variables de configuración del texto
    - cv.FONT_HERSHEY_SIMPLEX: Fuente del texto
    - 1: escala de la fuente
    - (0, 0, 255): Color del texto, rojo, en formato BGR
    - 2: Anchura de las lineas
    - cv.LINE_AA: Tipo de linea del texto, con anti-aliasing para verse más suaves
    """
    text_conf = cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA
    for s, p in zip(decoded_info, points) : 
        processed_img = cv.putText(processed_img, s, p[0].astype(int)), text)
    #Guardamos el QR sobreescribiendo el contenido de la imagen procesada
    cv.imwrite(img_path, processed_img)

def proccess_qr_from_video() :
    """
    Para leer QR's hasta que se presione la tecla:
    Variables:
    ret: Booleano, indica si se leyo un frame de la cámara (True) o no (False)
    frame: Frame de video
    ret_qr, decoded_info, points, _, s, p, frame: Similares a la implementación para imagenes 
    cv.waitkey...: Detiene la ejecución de la función al presionar la letra q
    """
    while True:
    ret, frame = CAP.read()

    if ret:
        ret_qr, decoded_info, points, _ = QR_D.detectAndDecodeMulti(frame)
        if ret_qr:
            for s, p in zip(decoded_info, points):
                if s:
                    print(s)
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                frame = cv.polylines(frame, [p.astype(int)], True, color, 8)
        cv.imshow(window_name, frame)

    if cv.waitKey(delay) & 0xFF == ord('q'):
        break

cv2.destroyWindow(WINDOW_NAME)