# Bu kod ile fare yardımıyla kara bölgelerini manule olarak seçip ayrı bir görüntü olarak kaydedebiliriz.
# Kara veya deniz bölgelerine özel çalışmalar için kullanılabilir

import cv2
import numpy as np

# Global değişkenler
points = []  # Seçilen noktalar
img = None  # Gerçek zamanlı çizim için görüntü

# Fare olayları için geri arama fonksiyonu
def draw_polygon(event, x, y, flags, param):
    global points, img, image

    if event == cv2.EVENT_LBUTTONDOWN:
        # Noktayı ekle
        points.append((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Sağ fare tuşu ile seçim tamamlanır
        if len(points) > 2:
            # Çokgenin son çizgisi
            cv2.line(img, points[-1], points[0], (0, 255, 0), 2)
            cv2.imshow("Selected ROI", img)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            cv2.fillPoly(mask, [np.array(points, dtype=np.int32)], 255)
            roi = cv2.bitwise_and(image, image, mask=mask)
            cv2.imshow("Cropped ROI", roi)
        points.clear()  # Noktaları temizle

    # Çizimi gerçek zamanlı olarak görüntüleme
    if len(points) > 0:
        img = image.copy()
        for i in range(len(points) - 1):
            cv2.line(img, points[i], points[i + 1], (0, 255, 0), 2)
        # Geçici çizgi
        cv2.line(img, points[-1], (x, y), (0, 255, 0), 2)

# Görüntüyü okuma
image_path = "C:/Users/KH/Downloads/sarkarma.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Görüntü yüklenemedi. Lütfen dosya yolunu kontrol edin.")
    exit(1)

# Görüntü kopyası
img = image.copy()

# Pencere ve fare geri arama fonksiyonunu ayarlama
cv2.namedWindow("Select ROI")
cv2.setMouseCallback("Select ROI", draw_polygon)

while True:
    cv2.imshow("Select ROI", img)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC tuşu ile çıkış
        break

cv2.destroyAllWindows()
