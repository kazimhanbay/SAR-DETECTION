# General Code Folder for SAR Ship Detection


This script describes .... .

<p align="center">
  <img src="https://github.com/user-attachments/assets/a7581d82-68b8-4574-a58e-c0d9bd49c8b3" style="border-radius: 50px;">
</p>

### Dependencies



The script requires the following packages to be installed:



* `PIL (Python Imaging Library)`: This package is used for reading, writing, and manipulating various image formats. It is commonly used for image processing and graphical manipulation tasks. While it can support some geospatial data formats, its primary function is image processing.

* `cv2`: This package is a part of the OpenCV library and provides support for image processing tasks such as reading, writing, and displaying images.

* `numpy`: This package is used for numerical computing and data analysis. It simplifies working with multi-dimensional arrays and matrices, and includes functions for linear algebra, statistical analysis, and other scientific computations.

* `matplotlib`: This package is used for creating plots and visualizations. It provides the ability to generate time series plots, line graphs, histograms, and various other visual representations.
 
* `scipy`: This package is designed for scientific and technical computing. It offers extensive tools for optimization, integration, interpolation, eigenvalue problems, linear algebra, and more.

![Python Version](https://img.shields.io/badge/Python-3.11-blue)


### Image Conversion Options 📸✨

Elevate your TIFF images to beautiful JPEGs with these fine-tuned options:

  * 🔍 Data Type - -ot Byte
     - Embrace precision with 8-bit unsigned integers. This choice ensures your images are stored in a compact and efficient format, perfect for both quality and practicality.


  * 🌟 Output Format - -of JPEG
     - Opt for JPEG, a format renowned for its balance between high-quality imaging and manageable file sizes. Ideal for web use and easy sharing!


   * 🔵🟢 Color Bands - -b 1, -b 2, -b 3
    Capture the full depth of your images by including:
       * -b 1: The grayscale band, adding depth and detail.
       * -b 2: The green band, highlighting nature's vibrant hues.
       * -b 3: The blue band, bringing in the cool and calm tones.


  * 💎 Pristine Quality - -co QUALITY=100
    - Ensure top-notch clarity by setting the JPEG quality to a perfect 100%. Ideal for when every detail matters and quality cannot be compromised.

  * 📐 Custom Size - -outsize 24000 16000
    - Define your canvas with custom dimensions of 24000x16000 pixels. This setting is perfect for capturing intricate details and expansive landscapes alike.

  * 🌓 Scale Adjustment - scale
    - Fine-tune your images with scale adjustments. Modify the brightness and contrast to suit your artistic vision, bringing a personalized touch to every pixel.

### 🚀 Usage

Unleash the power of image conversion right from your terminal! Here’s how to get started:
🖥️ Running the Script

Fire up the magic with a simple command:

 ``` python main.py ``` 

### 🧩 User Inputs

* The script will playfully ask you for:

   * TIFF Picture Name: Whisper the name of your TIFF image, ready to be transformed.
   * 3 Band TIFF Image Name: Dream up a name for your soon-to-be-created 3-band TIFF masterpiece.
   * JPEG Name: Conjure a name for the final JPEG image, your digital canvas.

### 🎨 The Transformation Journey

* Watch as your images undergo a magical metamorphosis:

    * Three-Band Conversion: Using convert_tiff_to_three_band, your TIFF is reborn with three bands (-b 1, -b 1, -b 1), shining in 16-bit unsigned integer glory (-ot UInt16).
    * JPEG Genesis: With convert_tiff_to_jpg, your image leaps into the JPEG realm. We talk 8-bit finesse (-ot Byte), a trio of bands (-b 1, -b 2, -b 3), impeccable quality (-co QUALITY=100), and a scaling adventure (scale factor 65535).
    * Folder Creation: Like a wizard, create_folder summons a new home for your TIFF, a cozy folder bearing its name.
    * Cropping Magic: The crop spell slices your JPEG into perfect 800x800 squares, each finding its place in the newly conjured folder.
    * Timekeeper's Tale: As the dust settles, you’ll see the time, in seconds, it took for this enchanting journey.

### 🌟 Glorious Output

* Behold the treasures you’ll uncover:

   * A 3-band TIFF image, proudly wearing the name you chose.
   * A JPEG image, radiant and crisp, also named by you.
   * A folder, echoing the name of your TIFF, filled with neatly cropped JPEG squares.



### Note



The script expects the TIFF image to be located in the current working directory. The output files will also be created in the current working directory.


### Referance 

For setup GDAL with wheel

* https://github.com/cgohlke/geospatial-wheels/releases
* https://opensourceoptions.com/how-to-install-gdal-for-python-with-pip-on-windows/
