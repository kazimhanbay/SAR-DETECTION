from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, binary_fill_holes, generate_binary_structure, binary_erosion, binary_dilation

# Görüntüyü yükleme
img_path = "C:/Users/KH/Downloads/sarkarma2.jpg"
img = Image.open(img_path)
img = img.convert("L")
img_array = np.array(img)

# Ortalama (MU) ve standart sapma (SS) görüntülerini hesaplayın
k = 2
MU = gaussian_filter(img_array, k)
SS = np.sqrt(gaussian_filter((img_array - MU)**2, k))

# Gauss fonksiyonları için standart sapmalar
sMu = 5
sSS = 8

# Olasılık görüntüleri
Pmu = np.exp(-(MU**2) / (2 * sMu**2))
Pss = np.exp(-(SS**2) / (2 * sSS**2))

# Eşik değerleri ve ikili görüntü oluşturma
thr1 = 0.7
thr2 = 0.7
result = (Pmu > thr1) & (Pss > thr2)

# Bağlı bileşenleri etiketleme ve en büyük bileşeni bulma
labeled_array, num_features = label(result)
sizes = np.bincount(labeled_array.ravel())
sizes[0] = 0
max_label = sizes.argmax()

# En büyük bileşen
largest_component = (labeled_array == max_label)
filled_component = binary_fill_holes(largest_component)
structure = generate_binary_structure(2, 1)
eroded_component = binary_erosion(filled_component, structure=structure)
cleaned_component = binary_dilation(eroded_component, structure=structure)

# Küçük bileşenleri kaldırma
min_size = 400
labels, num_labels = label(cleaned_component)
sizes = np.bincount(labels.ravel())
mask_sizes = sizes >= min_size
mask_sizes[0] = 0
cleaned_final = mask_sizes[labels]

# Noktasal çarpma
result_array = cleaned_final.astype(np.float32) * img_array.astype(np.float32)
result_normalized = (result_array / np.max(result_array)) * 255
result_normalized = result_normalized.astype(np.uint8)

# Görüntüleri gösterme
plt.figure(figsize=(18, 6))
plt.subplot(1, 3, 1)
plt.imshow(img_array, cmap='gray')
plt.title("Original Image")
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(cleaned_final, cmap='gray')
plt.title("Cleaned Largest Component")
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(result_normalized, cmap='gray')
plt.title("Resulting Image")
plt.axis('off')

plt.show()
