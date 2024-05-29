import cv2
import serial
import time

# Configuración del puerto serial
arduino = serial.Serial('COM8', 9600)  # Cambia 'COM5' al puerto correspondiente en tu sistema
time.sleep(2)

def enviarDato(dato):
    arduino.write(dato.encode())

# Ruta al archivo Haar Cascade para detección de rostros
pathCascade = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(pathCascade)

# Lista de nombres de archivos de las fotos
imagenes = ["foto2.jpg"]  # Cambia estos nombres por los nombres de tus archivos

for imagen_nombre in imagenes:
    image = cv2.imread(imagen_nombre)

    if image is None:
        print(f"Error al cargar la imagen {imagen_nombre}")
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        num_faces = len(faces)
        print(f"Se detectaron {num_faces} rostros en la imagen {imagen_nombre}")

        if num_faces > 0:
            enviarDato('G')
            print("Cara Detectada")
        else:
            enviarDato('R')
            print("Cara no Detectada")

        i = 0
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.putText(image, "Rostro"+str(i), (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 200, 0), 2)
            i += 1

        cv2.imshow(f"Rostros encontrados en {imagen_nombre}", image)
        cv2.waitKey(0)

arduino.close()