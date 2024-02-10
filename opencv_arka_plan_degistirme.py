# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 18:28:24 2024

@author: TUGCE
"""

import cv2
import numpy as np
import time

# Kamera bağlantısını başlat
cap = cv2.VideoCapture(0)

# Kamera bağlantısını kontrol et
if not cap.isOpened():
    print("Kamera bağlantısı başarısız!")
    exit()

# Arka plan için birkaç kare al
for i in range(30):
    ret, background = cap.read()

# Arka plan görüntüsünü çevir (yansıt)
background = np.flip(background, axis=1)

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()
    if not ret:
        print("Kare alınamadı!")
        break
    
    # Görüntüyü çevir (yansıt)
    img = np.flip(frame, axis=1)
    
    # HSV renk uzayına dönüştür
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Gaussian bulanıklaştırma uygula
    blurred = cv2.GaussianBlur(hsv, (35, 35), 0)

    # Maskeleme için renk aralığını belirle
    lower = np.array([0, 0, 0])
    upper = np.array([20, 255, 255])

    # Maske oluştur
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, np.ones((15, 15), np.uint8))
    mask = cv2.dilate(mask, np.ones((21, 21), np.uint8))

    # Maskelenmiş alanları arka planla değiştir
    img[np.where(mask == 255)] = background[np.where(mask == 255)]

    # Sonucu göster
    cv2.imshow('Gorunmezlik', img)
    
    # Çıkış için klavyeden 'ESC' tuşuna basın
    if cv2.waitKey(1) == 27:
        break

# Pencereyi kapat ve kamera bağlantısını serbest bırak
cv2.destroyAllWindows()
cap.release()
    

