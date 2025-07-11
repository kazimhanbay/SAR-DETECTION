<h1 align="center">Geliştirilen Gemi Tespit Yöntemi</h1>

<p align="justify">
<strong>NOT:</strong> Önerilen gemi tespit yönteminin sadece ana hatları sunulmuştur. Hessian matrisi, öz değerler
ve morfolojik işlemlere ait detaylar verilmemiştir. Yöntemin parametre optimizasyonu ile ilgili çalışmalar genel olarak tamamlanmıştır. Ancak bazı görüntülerde parametreler ile ilgili değişiklikler gerekmetedir. 
</p>

<p align="justify">
Önerilen yöntem ile Hessian matrisi ve öz değerlerden yararlanarak SAR görüntülerinde gemi tespiti yapmak
amaçlanmaktadır. Hessian matrisi, gemi bulunan bölgelerin görüntüdeki anahtar noktalara (key-point) karşılık
geldiğini gösteren bir belirteç görevi görür. Ancak eşikleme gibi temel yöntemler, gürültü, resifler ve kara
bölgeleri nedeniyle istenen doğruluğu sağlayamamaktadır. Bu zorluklar, Hessian matrisi ve öz değerlerle tensör
temelli bir gemi tespiti için yeni bir kara/deniz ayrımı yapan yöntemin geliştirilmesini gerektirmiştir.
</p>

<p align="justify">
Geliştirilen bu yöntem, yalnızca deniz bölgelerinde gemi tespiti yaparak daha gerçekçi sonuçlar sunmaktadır.
Özellikle <code>Datasetv1.0.1</code> ve <code>Datasetv2.0.0</code> üzerinde test edilen bu yöntem, kara bölgesi
içermeyen SAR görüntülerinde doğrudan gemi tespiti için etkili sonuçlar vermektedir. Kara/deniz içeren bir SAR
görüntüsü aşağıda görülebilir.
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/2d95257f-2377-4e30-a9c4-19b34c6ded29" alt="SAR Görüntüsü">
</p>

<p align="center"><strong>Şekil 1.</strong> Kara ve deniz bölgesi içeren SAR görüntüsü.</p>

<ul align="justify">
  <li><strong>Kara bölgesindeki parlak nesneler:</strong> Kara bölgesinde görülen parlak noktalar, yanlış tespitlere neden olabilmektedir.</li>
  <li><strong>Gemi:</strong> Deniz bölgesindeki nesneler gemiler olarak tespit edilmektedir.</li>
</ul>

<h3>a) SAR Görüntülerinde Kara/Deniz Ayrımının Yapılması</h3>

<p align="justify">
Bu adımda yapılan Hessian temelli gemi tespit yöntemi temel olarak 3 aşamadan oluşmaktadır:
</p>

<ol align="justify">
  <li>Görüntünün Hessian matrisinin ve öz değer bilgilerinin hesaplanması</li>
  <li>Gauss fonksiyonu ile kara/deniz ayrımının yapılması (Datasetv2.0.0’daki kara içeren görüntülerde)</li>
  <li>Morfolojik işlemler ve bağlantılı bileşenler ile gemilerin tespit edilmesi</li>
</ol>

<h4>1. Görüntünün Hessian Matrisinin ve Öz Değer Bilgilerinin Hesaplanması</h4>
<p align="justify">
Bu aşamada, gri seviye giriş SAR görüntüsünün Denklem 1’de verilen formül ile Hessian matrisi elde edilir
(continuous rot makale). Böylece, görüntünün yatay, dikey ve diagonal yönlerdeki ikinci mertebe türev bilgileri
(matrisleri) elde edilir. Görüntünün öz değerleri ise hesaplanan Hessian matrisleri kullanılarak hesaplanmıştır.
</p>

<h4>2. Gauss Fonksiyonu ile Kara/Deniz Ayrımının Yapılması (Kara İçeren Görüntülerde)</h4>
<p align="justify">
Bu çalışmada SAR görüntülerinde kara/deniz ayrımı ve gemi tespiti için Hessian matrisinden hesaplanan ikinci öz
değer matrisi kullanılmıştır. İkinci öz değer matrisi, sahil çizgisinin doğru bir şekilde belirlenmesini
sağlayan ayırt edici karakterizasyonu sunmaktadır. Bu matris, <code>σ=k</code> (genellikle <code>k=2</code>)
değeri ile Gauss filtresinden geçirilerek ortalama görüntü elde edilmiştir. Ardından, standart sapma görüntüsü,
ikinci öz değer matrisinden ortalama görüntünün çıkarılması, karesinin alınması ve tekrar Gauss filtresinden
geçirilmesiyle hesaplanmıştır.
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/1aa9f29a-4686-40e3-a3fd-b92d9c591ab2" alt="Gauss Fonksiyonu">
</p>

<p align="justify">
Bu işlemler sonucunda, ortalama görüntü ve standart sapma görüntüsü ile bu görüntülerin 2 standart sapma
değerleri Gauss denkleminde kullanılarak iki ayrı Gauss fonksiyonu temelli görüntü oluşturulmuştur. Nihai
aşamada, bu görüntüler 0.7 eşik değeri ile eşiklenmiş ve kara/deniz ayrımı en iyi şekilde gerçekleştirilmiştir.
Elde edilen eşiklenmiş görüntüler, kara ve deniz ayrımını sağlamak ve sahil çizgisini belirlemek için
birleştirilmiştir.
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/384ad8d6-676f-439c-8435-70d39e4675d0" alt="Eşikleme Sonucu">
</p>

<h3>3) Morfolojik İşlemler ve Bağlantılı Bileşenler ile Gemilerin Tespit Edilmesi</h3>
<p align="justify">
Bu adımda, gri seviye giriş görüntüsü ile bir önceki adımda elde edilen ikilik (Şekil 2-b: kara bölgesi siyah,
deniz bölgesi beyaz) görüntü çarpılmıştır. Bu çarpım neticesinde, giriş görüntüsünün kara bölgesi siyaha
boyanır ve deniz bölgesinde gemi pikselleri vurgulanmış olur.
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/63a087db-0a1b-43ac-9baa-4801c78640e9" alt="Sonuç Görüntüsü">
</p>

<p align="justify">
Önerilen gemi tespit yönteminde, deniz bölgelerindeki gemileri tespit etmek için kara bölgeleri, Gauss temelli tensör ve Hessian/öz değer hesaplamaları ile tamamen yok edilmiştir. Proje önerisindeki gemi bulma tensörü yerine, kara bölgeleri içeren görüntülerde daha etkili olan yeni bir formülasyon geliştirilmiştir. Yöntemin son aşamasında, Şekil 3-c'de elde edilen görüntüler 140 piksel yoğunluk değerinde eşiklenerek gemi pikselleri beyaz olarak ikilik görüntülerde ayrıştırılmıştır.
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/ba8ad206-ac2f-4ab4-8517-76adbaae98aa" alt="image6">
  <img src="https://github.com/user-attachments/assets/4f9ce398-7c4a-4490-8fc0-0bd4f95cdae8" alt="image7">
</p>

<p align="justify">
Şekil 5’te, kara bölgelerini de içeren Datasetv2.0.0 veri tabanındaki bazı SAR görüntülerine ait gemi tespit sonuçları sunulmuştur. Geliştirilen yöntem, yapılan deneysel çalışmalarda yaklaşık %85 başarıyla gemi tespiti sağlamıştır. Ancak, girintili sahil yapılarında bazı gemilerin tespit edilemediği ve geminin ön/arka su izlerinden kaynaklanan beyaz piksellerin fazladan gemi olarak algılandığı durumlar görülmüştür. (Örneğin, Şekil 5’te üçüncü ve beşinci satırlar). Bu eksiklikleri gidermek için hassas morfolojik işlemler ve gürültü temizleme üzerine çalışmalar devam etmekte olup yöntemin doğruluğunu artırmaya yönelik iyileştirmelere devam edilmektedir.
</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/87dd9f05-a552-4ba4-b530-76e135e0f122" alt="image8">
  <img src="https://github.com/user-attachments/assets/e0f52918-4583-4ce1-8225-0a961b788481" alt="image9">
  <img src="https://github.com/user-attachments/assets/a9bc9290-12ef-4132-bbd8-d94f15214d9c" alt="image10">
  <img src="https://github.com/user-attachments/assets/8aa16f3e-d657-4ffc-a56b-050f73738ba2" alt="image11">
</p>
<p align="justify">
<h4>Yönteme ait makale : K. Hanbay, "SAR Ship Detection Based on Gaussian Probability and Eigenvalue Analysis," in IEEE Signal Processing Letters, vol. 32, pp. 2214-2218, 2025, doi: 10.1109/LSP.2025.3571640.</h4>

</p>
<p align="center">
</p>
