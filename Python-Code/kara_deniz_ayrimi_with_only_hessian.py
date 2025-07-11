# Bu kod kara/deniz içeren SAR görüntülerinde kara/deniz ayrımını ve sahil çizgisi tespitini sadece Hessian matrisi ve öz değerler ile yapar.
#Bazı SAR görüntülerinde parametrik ayarlamalar gerekmektedir. 

import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from PIL import Image


# Kullanıcıya bir dosya seçme penceresi aç
root = tk.Tk()
root.withdraw()  # Ana pencereyi gizle
file_path = filedialog.askopenfilename(
    title="Bir görüntü seçin",
    initialdir="C:/neo4j",  # Varsayılan olarak C:\neo4j klasörünü aç
    filetypes=[("Görüntü Dosyaları", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
)

# Eğer bir dosya seçildiyse
if file_path:
    # Seçilen görüntüyü oku
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        print("Görüntü yüklenemedi. Lütfen geçerli bir dosya seçin.")
    else:


        # Hessian matrisini hesapla
        hessian_xx = cv2.Sobel(img, cv2.CV_64F, 2, 0, ksize=5)
        hessian_xy = cv2.Sobel(img, cv2.CV_64F, 1, 1, ksize=5)
        hessian_yy = cv2.Sobel(img, cv2.CV_64F, 0, 2, ksize=5)

        # Hessian matrisinin öz değerlerini hesapla
        trace = hessian_xx + hessian_yy
        determinant = hessian_xx * hessian_yy - hessian_xy**2
        eigenval1 = (trace + np.sqrt(trace**2 - 4*determinant)) / 2
        eigenval2 = (trace - np.sqrt(trace**2 - 4*determinant)) / 2
        eigenval22 = np.array(eigenval2, dtype = np.uint8)

        # Her pikselin kxk komşuluğundaki ortalama ve standart sapma görüntülerini hesapla
        k = 3  # Komşuluk boyutu
        MU = gaussian_filter(eigenval2, k)
        SS = np.sqrt(gaussian_filter((eigenval2 - MU)**2, k))

        # MU = cv2.blur(eigenval2, (k, k))
        # SS = cv2.GaussianBlur(eigenval2, (k, k), sigmaX=1)

        # MU ve SS görüntülerini Gauss fonksiyonuna sokarak Pmu ve Pss görüntülerini oluştur
        sMu = np.std(MU)
        sSS = np.std(SS)

        Pmu = np.exp(-MU**2 / (2 * sMu**2))
        Pss = np.exp(-SS**2 / (2 * sSS**2))

        # İki görüntüyü eşikleme ve birleştirme
        thr1 = 0.7  # İlk eşik değeri
        thr2 = 0.7  # İkinci eşik değeri

        sonuc = (Pmu > thr1) & (Pss > thr2)

        # Sonucu görsel olarak çiz
        sonuc = sonuc.astype(np.uint8) * 255

        # En büyük nesneyi tutmak için kontur bul
        contours, _ = cv2.findContours(sonuc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # En büyük konturu bul
        largest_contour = max(contours, key=cv2.contourArea)

        # Yeni bir maske oluştur ve sadece en büyük konturu çiz
        mask = np.zeros_like(sonuc)
        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
        # cv2.drawContours(mask, [largest_contour], -1, 255, thickness=2)  #bu satır konturun sadece sınır çizgisini çizer

        # Orijinal görüntü ve filtrelenmiş sonuç görüntüsünü yan yana göster
        fig, axes = plt.subplots(1, 2, figsize=(12, 6))

        axes[0].imshow(img, cmap='gray')
        axes[0].set_title("Orijinal Görüntü")
        axes[0].axis('off')

        axes[1].imshow(mask, cmap='gray')
        axes[1].set_title("Filtrelenmiş Sonuç")
        axes[1].axis('off')

        plt.show()
else:
    print("Dosya seçimi iptal edildi.")
