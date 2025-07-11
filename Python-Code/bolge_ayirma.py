#bu kod Gauss fonksiyonu, Hessşan matria ve özdeğerler ile SAR görüntülerindeki kara ve deniz sınırını bulur
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter, label, binary_fill_holes, generate_binary_structure, binary_erosion, \
    binary_dilation


def process_and_save_images(input_folder, output_folder, k=2, sMu=5, sSS=8, thr1=0.7, thr2=0.7, min_size=500):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(input_folder, filename)

            # Load the image
            img = Image.open(img_path)
            img = img.convert("L")  # Convert to grayscale
            img_array = np.array(img)

            # Compute the mean (MU) and standard deviation (SS) images
            MU = gaussian_filter(img_array, k)
            SS = np.sqrt(gaussian_filter((img_array - MU) ** 2, k))

            # Compute the probability images Pmu and Pss using Gaussian functions
            Pmu = np.exp(-(MU ** 2) / (2 * sMu ** 2))
            Pss = np.exp(-(SS ** 2) / (2 * sSS ** 2))

            # Combine the probability images
            result = (Pmu > thr1) & (Pss > thr2)

            # Label connected components in the binary image
            labeled_array, num_features = label(result)

            # Find the largest connected component
            sizes = np.bincount(labeled_array.ravel())
            sizes[0] = 0  # Ignoring the background
            max_label = sizes.argmax()

            # Keep only the largest connected component
            largest_component = (labeled_array == max_label)

            # Fill holes within the largest component
            filled_component = binary_fill_holes(largest_component)

            # Remove thin connections by eroding and then dilating the component
            structure = generate_binary_structure(2, 1)
            eroded_component = binary_erosion(filled_component, structure=structure)
            cleaned_component = binary_dilation(eroded_component, structure=structure)

            # Remove small connected components (smaller than a certain threshold)
            labels, num_labels = label(cleaned_component)
            sizes = np.bincount(labels.ravel())
            mask_sizes = sizes >= min_size
            mask_sizes[0] = 0  # Exclude background
            cleaned_final = mask_sizes[labels]

            # Save the processed image
            output_path = os.path.join(output_folder, filename)
            plt.imsave(output_path, cleaned_final, cmap='gray')

# Example usage:
# process_and_save_images("C:/Users/KH/PycharmProjects/sar_1/sar", "C:/Users/KH/PycharmProjects/sar_1/output")
