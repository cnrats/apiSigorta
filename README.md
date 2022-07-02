# Sigorta Ofisi Yönetim Api
## Proje Hakkında
Temel amaç herhangi bir sigorta ofisinin tüm kayıtlarını sistem üzerinde tutup bunları yönetmesidir. Sistem üzerinde kullanıcı denetimi sağlanabilir, birden fazla kullanıcı aynı anda farklı yetkilerle çalışabilir, bireysel veya ortak ofislerle yapılan tüm işler ayrı şekilde kayıt tutulabilir, tutulan kayıtlarda ortak işler üzerinden komisyon payları ayarlanabilir, işler üzerinde müşterinin ödemeleri ve borçları görüntülebilir ve kullanıcıya fiyat teklif broşürü otomatik olarak hazırlanabilir.
## Veritabanı Görünümü
**kullancilar**
- id (int)
- kullaniciAdi (text)
- sifre (text)

**kullaniciYetkileri**
- id (int)
- kullaniciId (int)
- firmalarDuzenle (bool)
- musterilerDuzenle (bool)
- arsivKlasorleriDuzenle (bool)
- branslarDuzenle (bool)
- sigortaSirketleriDuzenle (bool)
- bireyselIslerDuzenle (bool)
- ortakIslerDuzenle (bool)
- alacaklarDuzenle (bool)
- verilenlerDuzenle (bool)
- kullanicilarDuzenle (bool)
- kayitlarGoruntule (bool)

**oturumlar**
- id (int)
- kullaniciId (int)
- erisimKodu (text)
- bitisTarihi (text)

**firmalar**
- id (int)
- ad (text)

**arsivKlasorleri**
- id (int)
- ad (text)

**branslar**
- id (int)
- ad (text)

## Api Kullanım Kılavuzu
### Kullanıcı Denetimi
**/kullanici/giris/ (Tamamlandı)**
- kullaniciAdi, sifre => durum, mesaj, erisimKodu;

**/kullanici/cikis/ (Tamamlandı)**
- erisimKodu => durum, mesaj;

**/kullanici/ekle/ (Tamamlandı)**
- erisimKodu, kullaniciAdi, sifre, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule => durum, mesaj, kullaniciId;\

**/kullanici/sil/ (Tamamlandı)**
- erisimKodu, kullaniciId => durum, mesaj;\

**/kullanici/goster/hepsi/ (Tamamlandı)**
- erisimKodu => durum, mesaj, id, kullaniciAdi; (Tüm kullanıcılar.)\

**/kullanici/goster/tek/ (Tamamlandı)**
- erisimKodu, kullaniciId => durum, mesaj, id, kullaniciAdi, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule; (Tek kullanıcı.)\

**/kullanici/guncelle/ (Tamamlandı)**
- erisimKodu, kullaniciId, sifre, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule => durum, mesaj;

**/firma/ekle/ (Tamamlandi)**
- erisimKodu, firmaAdi => durum, mesaj, firmaId;

**/firma/goster/hepsi (Tamamlandi)**
- erisimKodu => durum, mesaj, firmaId, firmaAdi;

**/firma/guncelle/ (Tamamlandi)**
- erisimKodu, firmaId, firmaAdi => durum, mesaj;

**/firma/sil/ (Tamamlandi)**
- erisimKodu, firmaId => durum, mesaj;

**/arsiv/ekle/ (Tamamlandi)**
- erisimKodu, arsivKlasoruAdi => durum, mesaj, arsivKlasoruId;

**/arsiv/goster/hepsi (Tamamlandi)**
- erisimKodu => durum, mesaj, arsivKlasoruId, arsivKlasoruAdi;

**/arsiv/guncelle/ (Tamamlandi)**
- erisimKodu, arsivKlasoruId, arsivKlasoruAdi => durum, mesaj;

**/arsiv/sil/ (Tamamlandi)**
- erisimKodu, arsivKlasoruId => durum, mesaj;

**/brans/ekle/ (Tamamlandi)**
- erisimKodu, bransAdi => durum, mesaj, bransId;

**/brans/goster/hepsi (Tamamlandi)**
- erisimKodu => durum, mesaj, bransId, bransAdi;

**/brans/guncelle/ (Tamamlandi)**
- erisimKodu, brandId, bransAdi => durum, mesaj;

**/brans/sil/ (Tamamlandi)**
- erisimKodu, bransId => durum, mesaj;