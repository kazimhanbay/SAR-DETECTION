# Bu kod bolge_ayirma.py dosyasını kullanarak belirli klasördeki SAR görüntülerinde kara/deniz ayrımı yapıp belirlenen klasöre kaydediyor.
# Veri tabanı inşasında ve gemi tespiti uygulamalarında kullanılabilir.

from bolge_ayirma import process_and_save_images
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2


input_folder = "C:/Users/KH/PycharmProjects/sar_1/Sea-Land-Ship"
output_folder = "C:/Users/KH/PycharmProjects/sar_1/Sea-Land-Ship_islenmiş"

process_and_save_images(input_folder, output_folder,2, 5, 8, 0.7, 0.7, 500)


img_path_o = "C:/Users/KH/PycharmProjects/sar_1/Sea-Land-Ship/BangkokNew2024_V1_0_4000_out.jpg"  # Yer tutucu yol
img_o = Image.open(img_path_o)
img_o = img_o.convert("L")
img_array_o = np.array(img_o)


img_path_i = "C:/Users/KH/PycharmProjects/sar_1/Sea-Land-Ship_islenmiş/BangkokNew2024_V1_0_4000_out.jpg"  # Yer tutucu yol
img_i = Image.open(img_path_i)
img_i = img_i.convert("L")
img_array_i = np.array(img_i)

# print(img_array_i(400,400,:))
# Görüntüyü gri tonlamaya çevirme


# Deniz bölgelerini (koyu alanlar) tespit etmek için bir eşik değeri belirleme
# _, sea_mask = cv2.threshold(img_array_i, 50, 255, cv2.THRESH_BINARY_INV)



# result_image = img_array_o * img_array_i

# result_image2 = img_array_o * sea_mask

# Orijinal ve işlenmiş görüntüleri yan yana gösterin
plt.figure(figsize=(12, 6))

# Orijinal görüntü
# plt.subplot(1, 3, 1)
# plt.imshow(img_array_o, cmap='gray')
# plt.title("Original Image")
# plt.axis('off')
#
# # Temizlenmiş en büyük bileşen
# plt.subplot(1, 3, 2)
# plt.imshow(img_array_i, cmap='gray')
# plt.title("Cleaned Largest Component")
# plt.axis('off')
#
#
# # çarpım görüntüsü
# plt.subplot(1, 3, 3)
# plt.imshow(result_image, cmap='gray')
# plt.title("çarpım görüntüsü")
# plt.axis('off')
#
# plt.show()
