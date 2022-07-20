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

**sigortaSirketleri**
- id (int)
- ad (text)
- fotograf (blob)

**musteriler**
- id (int)
- ad (text)
- soyad (text)
- tc (text)
- dogumTarihi (text)
- telefon (text)
- mailAdresi (text)

**islerBireysel**
- id (int)
- musteriId (int)
- bransId (int)
- sigortaSirketiId (int)
- arsivId (int)
- plaka (text)
- ruhsatSeriNo (text)
- policeNo (text)
- policeBitisTarihi (text)

**islerOrtak**
- id (int)
- musteriId (int)
- bransId (int)
- sigortaSirketiId (int)
- arsivId (int)
- firmaId (int)
- komisyonOraniKendisi (int)
- komisyonOraniFirma (int)
- plaka (text)
- ruhsatSeriNo (text)
- policeNo (text)
- policeBitisTarihi (text)

**alacaklar**
- id (int)
- isId (int)
- miktar (int)
- aciklama (text)
- tarih (text)
- isTuru(0 = Bireysel, 1 = Ortak) (int)

**verecekler**
- id (int)
- isId (int)
- miktar (int)
- aciklama (text)
- tarih (text)
- isTuru(0 = Bireysel, 1 = Ortak) (int)

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

**/firma/ekle/**
- erisimKodu, firmaAdi => durum, mesaj, firmaId;

**/firma/goster/hepsi**
- erisimKodu => durum, mesaj, firmaId, firmaAdi;

**/firma/guncelle/**
- erisimKodu, firmaId, firmaAdi => durum, mesaj;

**/firma/sil/**
- erisimKodu, firmaId => durum, mesaj;

**/arsiv/ekle/**
- erisimKodu, arsivKlasoruAdi => durum, mesaj, arsivKlasoruId;

**/arsiv/goster/hepsi**
- erisimKodu => durum, mesaj, arsivKlasoruId, arsivKlasoruAdi;

**/arsiv/guncelle/**
- erisimKodu, arsivKlasoruId, arsivKlasoruAdi => durum, mesaj;

**/arsiv/sil/**
- erisimKodu, arsivKlasoruId => durum, mesaj;

**/brans/ekle/**
- erisimKodu, bransAdi => durum, mesaj, bransId;

**/brans/goster/hepsi**
- erisimKodu => durum, mesaj, bransId, bransAdi;

**/brans/guncelle/**
- erisimKodu, bransId, bransAdi => durum, mesaj;

**/brans/sil/**
- erisimKodu, bransId => durum, mesaj;

**/sirket/ekle/**
- erisimKodu, sigortaSirketiAdi, fotograf => durum, mesaj, sigortaSirketiId;

**/sirket/goster/hepsi/**
- erisimKodu => durum, mesaj, sigortaSirketiId, sigortaSirketiAdi, fotograf;

**/sirket/guncelle/**
- erisimKodu, sigortaSirketiAdi, sigortaSirketiId, fotograf => durum, mesaj;

**/sirket/sil/**
- erisimKodu, sigortaSirketiId => durum, mesaj;

**/musteri/ekle/**
- erisimKodu, musteriAdi, musteriSoyadi, musteriTc, musteriDogumTarihi, musteriTelefon, musteriMailAdresi => durum, mesaj, musteriId;

**/musteri/goster/hepsi/**
- erisimKodu => durum, mesaj, musteriId, musteriAdi, musteriSoyadi, musteriTelefon, musteriTc;

**/musteri/goster/tek/**
- erisimKodu => durum, mesaj, musteriId,musteriAdi, musteriSoyadi, musteriTc, musteriDogumTarihi, musteriTelefon, musteriMailAdresi;

**/musteri/guncelle/**
- erisimKodu, musteriId,musteriAdi, musteriSoyadi, musteriTc, musteriDogumTarihi, musteriTelefon, musteriMailAdresi => durum, mesaj;

**/musteri/sil/**
- erisimKodu, musteriId => durum, mesaj;

**/is/bireysel/ekle/**
- erisimKodu, musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi => durum, mesaj, isId;

**/is/bireysel/goster/hepsi/**
- erisimKodu => durum, mesaj, musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, musteriAdi;

**/is/bireysel/musteri/goster/hepsi/**
- erisimKodu, musteriId => durum, mesaj, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, musteriAdi;

**/is/bireysel/arsiv/goster/hepsi/**
- erisimKodu, arsivId => durum, mesaj, bransId, sigortaSirketiId, musteriId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, musteriAdi;

**/is/bireysel/guncelle/**
- erisimKodu, isId, musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi => durum, mesaj;

**/is/bireysel/sil/**
- erisimKodu, isId => durum, mesaj;

**/is/ortak/ekle/**
- erisimKodu, musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi => durum, mesaj, isId;

**/is/ortak/goster/hepsi/**
- erisimKodu => durum, mesaj, musteriId, bransId, sigortaSirketiId, arsivId, plaka, firmaId, komisyonOraniKendisi, komisyonOraniFirma, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, firmaAdi, musteriAdi;

**/is/ortak/musteri/goster/hepsi/**
- erisimKodu, musteriId => durum, mesaj, bransId, sigortaSirketiId, arsivId, firmaId, komisyonOraniKendisi, komisyonOraniFirma, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, firmaAdi, musteriAdi;

**/is/ortak/arsiv/goster/hepsi/**
- erisimKodu, arsivId => durum, mesaj, bransId, sigortaSirketiId, musteriId, firmaId, komisyonOraniKendisi, komisyonOraniFirma, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, firmaAdi, musteriAdi;

**/is/ortak/firma/goster/hepsi/**
- erisimKodu, firmaId => durum, mesaj, bransId, sigortaSirketiId, arsivId, musteriId, komisyonOraniKendisi, komisyonOraniFirma, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, bransAdi, sigortaSirketiAdi, arsivKlasoruAdi, firmaAdi, musteriAdi;

**/is/ortak/guncelle/**
- erisimKodu, isId, musteriId, bransId, sigortaSirketiId, arsivId, firmaId, komisyonOraniKendisi, komisyonOraniFirma, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi => durum, mesaj;

**/is/ortak/sil/**
- erisimKodu, isId => durum, mesaj;

**/isler/bireysel/yaklasan/**
-erisimKodu => (Tarihi yaklaşan bireysel işler + kalanGun)

**/isler/ortak/yaklasan/**
- erisimKodu => (Tarihi yaklaşan ortak işler + kalanGun)

**/isler/yaklasan/**
- erisimKodu => (Tarihi yaklaşan tüm işler + kalanGun)

**/alacaklar/ekle/**
- erisimKodu, isId, miktar, aciklama, tarih, isTuru(0 = Bireysel, 1 = Ortak) => durum, mesaj;

**/alacaklar/goster/**
- erisimKodu, isId, isTuru(0 = Bireysel, 1 = Ortak) => durum, mesaj, miktar, aciklama, tarih;

**/alacaklar/guncelle/**
- erisimKodu, alacakId, miktar, aciklama, tarih => durum, mesaj;

**/alacaklar/sil/**
- erisimKodu, alacakId = durum, mesaj;

**/verecekler/ekle/**
- erisimKodu, isId, miktar, aciklama, tarih, isTuru(0 = Bireysel, 1 = Ortak) => durum, mesaj;

**/verecekler/goster/**
- erisimKodu, isId, isTuru(0 = Bireysel, 1 = Ortak) => durum, mesaj, miktar, aciklama, tarih;

**/verecekler/guncelle/**
- erisimKodu, alacakId, miktar, aciklama, tarih => durum, mesaj;

**/verecekler/sil/**
- erisimKodu, alacakId => durum, mesaj;

**/borc/ (Müşterinin işte kalan borcunu hesaplar.)**
- erisimKodu, isId, isTuru(0 = Bireysel, 1 = Ortak)(0 = Bireysel, 1 = Ortak) => toplamTutar;

**/pay/ (Sadece ortak işler üzerinde, alacak payları hesaplar.)**
- erisimKodu, isId => bireyselAlacak, firmaAlacak; 

**/goster/hepsi/**
- erisimKodu => (Tüm veriler.)

**/teklif/ (GET)**
- erisimKodu, bransId, ad, soyad, ustBilgi, altBilgi, sigortaSirketleri, fiyatBilgileri => url;