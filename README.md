# Geliştirilen Gemi Tespit Yöntemi

Önerilen yöntem ile Hessian matrisi ve öz değerlerden yararlanarak SAR görüntülerinde gemi tespiti yapmak amaçlanmaktadır. Hessian matrisi, gemi bulunan bölgelerin görüntüdeki anahtar noktalara (key-point) karşılık geldiğini gösteren bir belirteç görevi görür. Ancak eşikleme gibi temel yöntemler, gürültü, resifler ve kara bölgeleri nedeniyle istenen doğruluğu sağlayamamaktadır. Bu zorluklar, Hessian matrisi ve öz değerlerle tensör temelli bir gemi tespiti için yeni bir kara/deniz ayrımı yapan yöntemin geliştirilmesini gerektirmiştir.

Geliştirilen bu yöntem, yalnızca deniz bölgelerinde gemi tespiti yaparak daha gerçekçi sonuçlar sunmaktadır. Özellikle `Datasetv1.0.1` ve `Datasetv2.0.0` üzerinde test edilen bu yöntem, kara bölgesi içermeyen SAR görüntülerinde doğrudan gemi tespiti için etkili sonuçlar vermektedir. Kara/deniz içeren bir SAR görüntüsü aşağıda görülebilir.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2d95257f-2377-4e30-a9c4-19b34c6ded29" alt="SAR Görüntüsü">
</p>

**Şekil 1.** Kara ve deniz bölgesi içeren SAR görüntüsü.

- **Kara bölgesindeki parlak nesneler:** Kara bölgesinde görülen parlak noktalar, yanlış tespitlere neden olabilmektedir.
- **Gemi:** Deniz bölgesindeki nesneler gemiler olarak tespit edilmektedir.

### a) SAR Görüntülerinde Kara/Deniz Ayrımının Yapılması

Bu adımda yapılan Hessian temelli gemi tespit yöntemi temel olarak 3 aşamadan oluşmaktadır:

1. **Görüntünün Hessian matrisinin ve öz değer bilgilerinin hesaplanması**
2. **Gauss fonksiyonu ile kara/deniz ayrımının yapılması** (Datasetv2.0.0’daki kara içeren görüntülerde)
3. **Morfolojik işlemler ve bağlantılı bileşenler ile gemilerin tespit edilmesi**

#### 1. Görüntünün Hessian Matrisinin ve Öz Değer Bilgilerinin Hesaplanması
Bu aşamada, gri seviye giriş SAR görüntüsünün Denklem 1’de verilen formül ile Hessian matrisi elde edilir (continuous rot makale). Böylece, görüntünün yatay, dikey ve diagonal yönlerdeki ikinci mertebe türev bilgileri (matrisleri) elde edilir. Görüntünün öz değerleri ise hesaplanan Hessian matrisleri kullanılarak hesaplanmıştır.

#### 2. Gauss Fonksiyonu ile Kara/Deniz Ayrımının Yapılması (Kara İçeren Görüntülerde)
Bu çalışmada SAR görüntülerinde kara/deniz ayrımı ve gemi tespiti için Hessian matrisinden hesaplanan ikinci öz değer matrisi kullanılmıştır. İkinci öz değer matrisi, sahil çizgisinin doğru bir şekilde belirlenmesini sağlayan ayırt edici karakterizasyonu sunmaktadır. Bu matris, $\sigma=k$ (genellikle $k=2$) değeri ile Gauss filtresinden geçirilerek ortalama görüntü elde edilmiştir. Ardından, standart sapma görüntüsü, ikinci öz değer matrisinden ortalama görüntünün çıkarılması, karesinin alınması ve tekrar Gauss filtresinden geçirilmesiyle hesaplanmıştır. Yöntemde kullanılan Gauss fonksiyonu aşağıdaki gibidir:

<p align="center">
  <img src="https://github.com/user-attachments/assets/1aa9f29a-4686-40e3-a3fd-b92d9c591ab2" alt="gauss">
</p>

Bu işlemler sonucunda, ortalama görüntü ve standart sapma görüntüsü ile bu görüntülerin 2 standart sapma değerleri Gauss denkleminde kullanılarak iki ayrı Gauss fonksiyonu temelli görüntü oluşturulmuştur. Nihai aşamada, bu görüntüler 0.7 eşik değeri ile eşiklenmiş ve kara/deniz ayrımı en iyi şekilde gerçekleştirilmiştir. Elde edilen eşiklenmiş görüntüler, kara ve deniz ayrımını sağlamak ve sahil çizgisini belirlemek için birleştirilmiştir. Eşikleme ve sonrasında elde edilen eşiklenmiş görüntülerin birleştirilmesinde aşağıdaki ifade kullanılmıştır:

<p align="center">
  <img src="https://github.com/user-attachments/assets/384ad8d6-676f-439c-8435-70d39e4675d0" alt="image3">
</p>

### Ortalama ve Standart Sapma Görüntüleri ile Kara/Deniz Ayrımı

Burada, $P_{\mu}$ ve $P_{\sigma}$ sırasıyla ortalama görüntü ve standart sapma görüntüleridir. Eşikleme sonrasında, bu iki görüntü mantıksal VE (`and`) işlemi ile birleştirilmiştir. Elde edilen görüntü, normalizasyon işlemi ile sadece 0 ve 255 değerlerinden oluşan bir siyah-beyaz görüntüye dönüştürülmüştür.

#### Kontur Bulma İşlemi

Bir sonraki adımda, görüntüdeki en büyük nesneyi tutmak için kontur bulma işlemi yapılmıştır. Bu işlem için OpenCV kütüphanesinin `findContours` metodu kullanılmıştır. SAR görüntüsündeki en büyük nesne olabilecek gemi veya deniz bölgesinin kontur çizgilerini elde etmek ve diğer tüm küçük konturları elemek gerekmektedir. Bunun için elde edilen konturlarda en büyük alana sahip kontur tespit edilmiştir.

#### Kara/Deniz Ayrım Yöntemi ile Elde Edilen Sonuçlar

**Şekil 2:** Kara bölgesi içeren bir SAR görüntüsünde kara/deniz ayrım yöntemi ile elde edilen sonuçlar aşağıda görülebilir.

<p align="center">
  <img src="https://github.com/user-attachments/assets/2e0e877c-2dbe-45b9-9b7a-ffa7a996ee9d" alt="image4">
</p>

### 3) Morfolojik İşlemler ve Bağlantılı Bileşenler ile Gemilerin Tespit Edilmesi

Bu adımda, gri seviye giriş görüntüsü ile bir önceki adımda elde edilen ikilik (Şekil 2-b: kara bölgesi siyah, deniz bölgesi beyaz) görüntü çarpılmıştır. Bu çarpım neticesinde, giriş görüntüsünün kara bölgesi siyaha boyanır ve deniz bölgesinde gemi pikselleri vurgulanmış olur (Şekil 3-c).

#### Morfolojik İşlemler

Morfolojik işlemler, görüntüdeki istenmeyen küçük nesneleri temizlemek ve gemi piksellerini daha belirgin hale getirmek için kullanılmıştır. Bu işlemler sayesinde deniz bölgesinde yer alan gemiler daha kolay tespit edilebilir hale gelmiştir.

**Şekil 3-c:** İkilik görüntü ile giriş görüntüsünün çarpılması sonucu elde edilen ve deniz bölgesindeki gemi piksellerinin vurgulandığı sonuç.

<p align="center">
  <img src="https://github.com/user-attachments/assets/63a087db-0a1b-43ac-9baa-4801c78640e9" alt="image5">
</p>

Önerilen gemi tespit yönteminde, deniz bölgelerindeki gemileri tespit etmek için kara bölgeleri, Gauss temelli tensör ve Hessian/öz değer hesaplamaları ile tamamen yok edilmiştir. Proje önerisindeki gemi bulma tensörü yerine, kara bölgeleri içeren görüntülerde daha etkili olan yeni bir formülasyon geliştirilmiştir. Yöntemin son aşamasında, Şekil 3-c'de elde edilen görüntüler 140 piksel yoğunluk değerinde eşiklenerek gemi pikselleri beyaz olarak ikilik görüntülerde ayrıştırılmıştır.

<p align="center">
  <img src="https://github.com/user-attachments/assets/ba8ad206-ac2f-4ab4-8517-76adbaae98aa" alt="image6">
  <img src="https://github.com/user-attachments/assets/4f9ce398-7c4a-4490-8fc0-0bd4f95cdae8" alt="image7">
</p>

Şekil 5’te, kara bölgelerini de içeren Datasetv2.0.0 veri tabanındaki bazı SAR görüntülerine ait gemi tespit sonuçları sunulmuştur. Geliştirilen yöntem, yapılan deneysel çalışmalarda yaklaşık %85 başarıyla gemi tespiti sağlamıştır. Ancak, girintili sahil yapılarında bazı gemilerin tespit edilemediği ve geminin ön/arka su izlerinden kaynaklanan beyaz piksellerin fazladan gemi olarak algılandığı durumlar görülmüştür. (Örneğin, Şekil 5’te üçüncü ve beşinci satırlar). Bu eksiklikleri gidermek için hassas morfolojik işlemler ve gürültü temizleme üzerine çalışmalar devam etmekte olup yöntemin doğruluğunu artırmaya yönelik iyileştirmelere devam edilmektedir.

<p align="center">
  <img src="https://github.com/user-attachments/assets/87dd9f05-a552-4ba4-b530-76e135e0f122" alt="image8">
  <img src="https://github.com/user-attachments/assets/e0f52918-4583-4ce1-8225-0a961b788481" alt="image9">
  <img src="https://github.com/user-attachments/assets/a9bc9290-12ef-4132-bbd8-d94f15214d9c" alt="image10">
  <img src="https://github.com/user-attachments/assets/8aa16f3e-d657-4ffc-a56b-050f73738ba2" alt="image11">
</p>
