
# Bu kod kara içermeyen SAR görüntülerinde daha optimal gemi tespit işlemi yapmaktadır.
# Kara içeren görüntülerde parametre ayarlamaları gerekebilmektedir.

import cv2
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, binary_fill_holes, generate_binary_structure, binary_erosion, binary_dilation

def select_image():
    Tk().withdraw()  # Tkinter penceresini gizle
    image_path = askopenfilename(initialdir=r"C:\Users\KH\Downloads\LINK\Dataset v1.0.0 (with REAL-ESRGAN)\Ship-Result",
                                 title="Bir görüntü seçin",
                                 filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return image_path

# Görüntü seçme
image_path = select_image()

if image_path:  # Kullanıcı bir görüntü seçtiyse
    # Görüntüyü yükleme
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Görüntüyü normalize ederek parlak nesneleri daha iyi tespit edebilmek için eşikleme işlemi
    _, thresholded = cv2.threshold(image, 80, 255, cv2.THRESH_BINARY)

    # plt.imshow(image, cmap='gray')
    # Küçük parlak pikselleri temizleme - Morfolojik açma ve kapama işlemleri
    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(thresholded, kernel, iterations=1)
    cleaned_image = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT,(2,2)),iterations=2)  # Morfolojik kapama

    plt.figure(figsize=(18, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title("Giriş  Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(cleaned_image, cmap='gray')
    plt.title("Morfolojik Binary Image")
    plt.axis('off')

    # Temizlenmiş görüntünün Hessian matrisini hesaplama
    ddepth = cv2.CV_64F  # Derinlik
    # İkinci türevleri hesaplama (Hessian bileşenleri)
    hessian_xx = cv2.Sobel(cleaned_image, ddepth, 2, 0, ksize=5)
    hessian_xy = cv2.Sobel(cleaned_image, ddepth, 1, 1, ksize=5)
    hessian_yy = cv2.Sobel(cleaned_image, ddepth, 0, 2, ksize=5)

    # Hessian matrisinin ikinci özdeğerini hesapla
    trace = hessian_xx + hessian_yy
    determinant = hessian_xx * hessian_yy - hessian_xy ** 2
    eigenvalue2 = (trace - np.sqrt(trace ** 2 - 4 * determinant)) / 2

    # İkinci özdeğer matrisini normalize et ve kenar tespiti yap
    eigenvalue2_normalized = cv2.normalize(eigenvalue2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Canny kenar tespiti uygulama
    edges = cv2.Canny(eigenvalue2_normalized, 50, 150)

    # Bağlantılı bileşenleri bulma (kenarların oluşturduğu gemi bölgelerini tespit etme)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # plt.imshow(contours, cmap='gray')
    # Orijinal görüntüyü renkli olarak yeniden yükleyelim ki dikdörtgenleri ekleyebilelim
    image_with_boxes = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Minimum alanı belirle (örneğin 50 pikselden küçük nesneleri görmezden geleceğiz)
    min_area = 5



    # Her bir tespit edilen parlak nesne için dikdörtgen çizme
    label_counter = 1
    drawn_positions = []

    for contour in contours:
        if cv2.contourArea(contour) > min_area:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image_with_boxes, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Gemi etiketini oluştur
            label = f"Gemi {label_counter}"
            label_counter += 1

            # Yazının çakışmasını önlemek için kontrol et
            text_x, text_y = x, y - 10  # Yazıyı dikdörtgenin biraz üstüne yerleştir

            # Eğer metin çakışıyorsa yazıyı biraz yukarıya kaydır
            for prev_text_x, prev_text_y, prev_w, prev_h in drawn_positions:
                if abs(text_x - prev_text_x) < prev_w and abs(text_y - prev_text_y) < prev_h:
                    text_y -= 15  # Çakışmayı önlemek için yazıyı yukarı kaydır

            # Yazının konumunu kaydet
            drawn_positions.append((text_x, text_y, w, 15))

            # Yazıyı görüntüye ekle
            cv2.putText(image_with_boxes, label, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                        cv2.LINE_AA)

    # Sonuç görüntüsünü gösterme
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB))
    plt.title('Detected Ships with Bounding Boxes and Labels')
    plt.axis('off')
    plt.show()
else:
    print("Herhangi bir görüntü seçilmedi.")