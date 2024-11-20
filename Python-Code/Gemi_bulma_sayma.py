# Bu kod kara bölgeleri de içeren SAR görüntülerin gemi tespiti yapmaktadır.
# Bazı görüntülerde parametrik ayarlamalar gerekebilir. Parametre optimizasyonu devam etmektedir.

import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from PIL import Image
from skimage.filters import threshold_otsu
from scipy.ndimage import label
from scipy.ndimage.morphology import binary_closing, binary_erosion

# Görüntüyü oku ve gri tonlamaya çevir
# Kullanıcıya bir dosya seçme penceresi aç
root = tk.Tk()
root.withdraw()  # Ana pencereyi gizle
file_path = filedialog.askopenfilename(
    title="Bir görüntü seçin",
    initialdir="C:/Users/KH\Downloads/LINK/Dataset v2.0.0 (REAL-ESRGAN version)/Sea-Land-Ship",  # Varsayılan olarak C:\neo4j klasörünü aç
    filetypes=[("Görüntü Dosyaları", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
)

# Eğer bir dosya seçildiyse
if file_path:
    # Seçilen görüntüyü oku
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    # plt.imshow(img, cmap='gray')
    # plt.show()
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


        # Her pikselin kxk komşuluğundaki ortalama ve standart sapma görüntülerini hesapla
        k = 3  # Komşuluk boyutu
        MU = gaussian_filter(eigenval2, sigma=k)

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

        sonuc = (Pmu > thr1) & (Pss > thr2)  #true false sonuç

        # Sonucu görsel olarak çiz
        sonuc = sonuc.astype(np.uint8) * 255  #uint8 sonuç (0 veya 255 var)
        # plt.imshow(sonuc, cmap='gray')
        # plt.show()
        # En büyük nesneyi tutmak için kontur bul
        contours, _ = cv2.findContours(sonuc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # En büyük konturu bul
        largest_contour = max(contours, key=cv2.contourArea)

        # Yeni bir maske oluştur ve sadece en büyük konturu çiz
        mask = np.zeros_like(sonuc)

        cv2.drawContours(mask, [largest_contour], -1, 255, thickness=cv2.FILLED)
        #cv2.drawContours(mask, [largest_contour], -1, 255, thickness=2)  #bu satır konturun sadece sınır çizgisini çizer
        # plt.imshow(mask, cmap='inferno')
        # plt.show()

        # Orijinal görüntü ve filtrelenmiş sonuç görüntüsünü yan yana göster
        # fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        #
        # axes[0].imshow(img, cmap='gray')
        # axes[0].set_title("Orijinal Görüntü")
        # axes[0].axis('off')
        #
        # axes[1].imshow(mask, cmap='gray')
        # axes[1].set_title("Filtrelenmiş Sonuç")
        # axes[1].axis('off')

        # plt.show()

        # Noktasal çarpma
        result_array = mask.astype(np.float32) * img.astype(np.float32)
        result_normalized = (result_array / np.max(result_array)) * 255
        result_normalized = result_normalized.astype(np.uint8)
        # plt.imshow(result_normalized, cmap='gray')
        # plt.show()


        thres = 140
        binary = result_normalized > thres
        binary_closed = binary_erosion(binary, structure=np.ones((2, 2)))
        labeled_image, num_features = label(binary_closed)
        # plt.imshow(labeled_image, cmap='gray')
        # plt.show()
        feature_areas = np.bincount(labeled_image.ravel())[1:]
        print(feature_areas)
        print(len(feature_areas))


        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        label_positions = []  # Etiket pozisyonlarını tutan liste

        # Her bir etiketli nesne için dikdörtgenleri çiz ve etiket adını yazdır
        for i in range(1, num_features + 1):
            mask_i = np.where(labeled_image == i, 255, 0).astype(np.uint8)
            contours_i, _ = cv2.findContours(mask_i, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours_i) > 0:
                x, y, w, h = cv2.boundingRect(contours_i[0])
                cv2.rectangle(img_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dikdörtgen çiz (yeşil renk)

                # Etiket adını yerleştir
                label_text = f"Gemi {i}"
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.6
                font_thickness = 2
                label_size, _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
                label_x = x
                label_y = y - 10  # Etiket, kutunun biraz yukarısında olacak

                # Etiket pozisyonunun çakışıp çakışmadığını kontrol et
                overlap = True
                while overlap:
                    overlap = False
                    for lx, ly, lw, lh in label_positions:
                        # Diğer etiketlerle çakışma olup olmadığını kontrol et
                        if abs(label_x - lx) < lw and abs(label_y - ly) < lh:
                            # Çakışmayı önlemek için etiketi biraz daha yukarıya kaydır
                            label_y -= 15
                            overlap = True
                            break

                # Etiketin yeni pozisyonunu kaydet
                label_positions.append((label_x, label_y, label_size[0], label_size[1]))

                # Etiketi çiz
                cv2.putText(img_bgr, label_text, (label_x, label_y), font, font_scale, (0, 255, 0), font_thickness,
                            cv2.LINE_AA)
        # Sonuç görüntüsünü göster
        plt.figure(figsize=(18, 6))
        plt.subplot(1, 3, 1)
        plt.imshow(binary, cmap='gray')
        plt.title("Input Binary Image")
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(binary_closed, cmap='gray')
        plt.title("Morfolojik Binary Image")
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))  # BGR'den RGB'ye çevirip göster
        plt.title("Labeled Ships with Bounding Boxes")
        plt.axis('off')
        plt.show()

else:
    print("Dosya seçimi iptal edildi.")


