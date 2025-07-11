# Bu kod Hessian matrisini kullanmadan sadece Gauss fonksiyonu ile kara/deniz ayrımını yapmaktadır. Her iki yöntem benzer sonuçar getirir

# Yeniden gerekli kütüphaneleri içe aktarıyorum
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, binary_fill_holes, generate_binary_structure, binary_erosion, binary_dilation

# Görüntüyü yükleme (şimdilik yer tutucu olarak önceki kodu kullanıyorum)
img_path = "C:/Users/KH/PycharmProjects/sar_1/Sea-Land-Ship/BangkokNew2024_V1_0_4000_out.jpg"  # Yer tutucu yol
img = Image.open(img_path)
img = img.convert("L")  # Gri tonlamaya dönüştür
img_array = np.array(img)

# Komşuluk boyutunu (k x k) tanımlayın
k = 2

# Ortalama (MU) ve standart sapma (SS) görüntülerini hesaplayın
MU = gaussian_filter(img_array, k)
SS = np.sqrt(gaussian_filter((img_array - MU)**2, k))

# Gauss fonksiyonları için standart sapmaları tanımlayın
sMu = 5  # Örnek değer, ayarlanabilir
sSS = 8   # Örnek değer, ayarlanabilir

# Gauss fonksiyonlarını kullanarak olasılık görüntülerini hesaplayın
Pmu = np.exp(-(MU**2) / (2 * sMu**2))
Pss = np.exp(-(SS**2) / (2 * sSS**2))

# Eşik değerleri tanımlayın
thr1 = 0.7  # Örnek değer, ayarlanabilir
thr2 = 0.7  # Örnek değer, ayarlanabilir

# Olasılık görüntülerini birleştirin
result = (Pmu > thr1) & (Pss > thr2)

# İkili görüntüde bağlı bileşenleri etiketleyin
labeled_array, num_features = label(result)

# En büyük bağlı bileşeni bulun
sizes = np.bincount(labeled_array.ravel())
sizes[0] = 0  # Arka planı yoksayın
max_label = sizes.argmax()

# Yalnızca en büyük bağlı bileşeni tutun
largest_component = (labeled_array == max_label)

# En büyük bileşen içindeki delikleri doldurun
filled_component = binary_fill_holes(largest_component)

# İnce bağlantıları kaldırmak için bileşeni eritin ve ardından genişletin
structure = generate_binary_structure(2, 1)
eroded_component = binary_erosion(filled_component, structure=structure)
cleaned_component = binary_dilation(eroded_component, structure=structure)

# Küçük bağlı bileşenleri kaldırın (belirli bir eşik değerinden daha küçük olanlar)
min_size = 400  # Örnek değer, ayarlanabilir
labels, num_labels = label(cleaned_component)
sizes = np.bincount(labels.ravel())
mask_sizes = sizes >= min_size
mask_sizes[0] = 0  # Arka planı dahil etmeyin
cleaned_final = mask_sizes[labels]

result_array = cleaned_final.astype(np.float32) * img_array.astype(np.float32)
result_normalized = (result_array / np.max(result_array)) * 255
result_normalized = result_normalized.astype(np.uint8)
# plt.imshow(result_normalized, cmap='gray')
# plt.show()

# Orijinal ve işlenmiş görüntüleri yan yana gösterin
plt.figure(figsize=(12, 6))

# Orijinal görüntü
plt.subplot(1, 2, 1)
plt.imshow(img_array, cmap='gray')
plt.title("Original Image")
plt.axis('off')

# Temizlenmiş en büyük bileşen
plt.subplot(1, 2, 2)
plt.imshow(cleaned_final, cmap='gray')
plt.title("Cleaned Largest Component")
plt.axis('off')

plt.show()
