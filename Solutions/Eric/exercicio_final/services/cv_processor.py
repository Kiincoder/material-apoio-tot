import cv2 as cv
import numpy as np

def binarize_image(file):
  image_array = np.frombuffer(file, dtype=np.uint8)
  img = cv.imdecode(image_array, cv.IMREAD_GRAYSCALE)
  img = cv.medianBlur(img,5)

  if img is None:
    raise ValueError("Falha ao decodificar imagem!")

  ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)


  success, encoded_image = cv.imencode('.png', th1)
  if not success:
    raise ValueError("Falha ao encodar imagem!")    
      
  return encoded_image.tobytes()
