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

**/kullanici/goruntule/hepsi (Tamamlandı)**
- erisimKodu => durum, mesaj, id, kullaniciAdi; (Tüm kullanıcılar.)\

**/kullanici/goruntule/tek (Tamamlandı)**
- erisimKodu, kullaniciId => durum, mesaj, id, kullaniciAdi, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule; (Tek kullanıcı.)\

**/kullanici/guncelle/ (Tamamlandı)**
- erisim-kodu, kullaniciId, sifre, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule => durum, mesaj;