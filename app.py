import flask
from flask import request, jsonify, g
from flask_cors import CORS, cross_origin
import sqlite3
import uuid
import shutil
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DATABASE = 'sigorta.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    return db

def oturumKontrol(erisimKodu):
    im = get_db().cursor()
    im.execute("""SELECT * FROM oturumlar WHERE erisimKodu='%s'"""%(erisimKodu))
    oturum = im.fetchone()
    if(oturum):
        return oturum['kullaniciId']
    else:
        return False

def yetkiKontrol(kullaniciId, yetki):
    im = get_db().cursor()
    im.execute("""SELECT * FROM kullaniciYetkileri WHERE kullaniciId = '%s'"""%(kullaniciId))
    yetkiler = im.fetchone()
    if(yetkiler):
        return yetkiler[yetki]
    return False

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/kullanici/giris/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciGiris():
    im = get_db().cursor()
    kullaniciAdi = request.form["kullaniciAdi"]
    sifre = request.form["sifre"]
    im.execute("""SELECT id, kullaniciAdi FROM kullanicilar WHERE kullaniciAdi='%s' AND sifre='%s'"""%(kullaniciAdi, sifre))
    veriler = im.fetchone()
    if(veriler):
        im.execute("""SELECT * FROM oturumlar WHERE kullaniciId='%s'"""%(veriler["id"]))
        oturumlar = im.fetchone()
        if(oturumlar):
            veriler = {}
            veriler['durum'] = "false"
            veriler['mesaj'] = "Baska bir oturum acik!"
        else:
            veriler['durum'] = "true"
            veriler['mesaj'] = "Giris yapma islemi basarili!"
            ekod = uuid.uuid4()
            veriler['erisimKodu'] = ekod
            im.execute("""INSERT INTO oturumlar (kullaniciId, erisimKodu, bitisTarihi) VALUES ('%s', '%s', '%s')"""%(veriler["id"], ekod, 'deneme'))
            get_db().commit()
    else:
        veriler = {}
        veriler['durum'] = "false"
        veriler['mesaj'] = "Kullanici adi veya sifre hatali!"
    return jsonify(veriler)

@app.route('/kullanici/cikis/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciCikis():
    erisimKodu = request.form["erisimKodu"]
    im = get_db().cursor()
    im.execute("""SELECT * FROM oturumlar WHERE erisimKodu = '%s'"""%(erisimKodu))
    oturum = im.fetchone()
    if(oturum):
        im.execute("""DELETE FROM oturumlar WHERE erisimKodu='%s'"""%(erisimKodu))
        veriler = {}
        veriler["durum"] = "true"
        veriler["mesaj"] = "Cikis islemi basarili!"
        get_db().commit()
        return jsonify(veriler)
    else:
        veriler = {}
        veriler = {}
        veriler["durum"] = "false"
        veriler["mesaj"] = "Oturum bulunamadi!"
        return jsonify(veriler)

@app.route('/kullanici/ekle/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciEkle():
    erisimKodu = request.form["erisimKodu"]
    kullaniciAdi = request.form["kullaniciAdi"]
    sifre = request.form["sifre"]
    firmalarDuzenle = request.form["firmalarDuzenle"]
    musterilerDuzenle = request.form["musterilerDuzenle"]
    arsivKlasorleriDuzenle = request.form["arsivKlasorleriDuzenle"]
    branslarDuzenle = request.form["branslarDuzenle"]
    sigortaSirketleriDuzenle = request.form["sigortaSirketleriDuzenle"]
    bireyselIslerDuzenle = request.form["bireyselIslerDuzenle"]
    ortakIslerDuzenle = request.form["ortakIslerDuzenle"]
    alacaklarDuzenle = request.form["alacaklarDuzenle"]
    verilenlerDuzenle = request.form["verilenlerDuzenle"]
    kullanicilarDuzenle = request.form["kullanicilarDuzenle"]
    kayitlarGoruntule = request.form["kayitlarGoruntule"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "kullanicilarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM kullanicilar WHERE kullaniciAdi = '%s'"""%(kullaniciAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Kullanici adi baska bir kullanici tarafindan kullanilmakta!"
            else:
                im.execute("""INSERT INTO kullanicilar (kullaniciAdi, sifre) VALUES ('%s','%s')"""%(kullaniciAdi, sifre))
                get_db().commit()
                im.execute("""SELECT id FROM kullanicilar WHERE kullaniciAdi = '%s'"""%(kullaniciAdi))
                kullaniciId = im.fetchone()
                im.execute("""INSERT INTO kullaniciYetkileri (kullaniciId, firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""%(kullaniciId['id'], firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde kullanici eklendi!"
                veriler["kullaniciId"] = kullaniciId["id"]
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Kullanici eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/kullanici/sil/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciSil():
    erisimKodu = request.form["erisimKodu"]
    kullaniciId = request.form["kullaniciId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "kullanicilarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM kullanicilar WHERE id = '%s'"""%(kullaniciId))
            if(im.fetchone()):
                im.execute("""DELETE FROM kullanicilar WHERE id = '%s'"""%(kullaniciId))
                im.execute("""DELETE FROM kullaniciYetkileri WHERE kullaniciId = '%s'"""%(kullaniciId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Kullanici basarili bir sekilde silindi!"
            else:
                veriler["durum"] = False
                veriler["mesaj"] = "Boyle bir kullanici yok!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/kullanici/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "kullanicilarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT id, kullaniciAdi FROM kullanicilar""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/kullanici/goster/tek/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciGosterTek():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "kullanicilarDuzenle")
        if(yetki):
            kullaniciId = request.form["kullaniciId"]
            im = get_db().cursor()
            im.execute("""SELECT kullaniciAdi FROM kullanicilar WHERE id = '%s'"""%(kullaniciId))
            veriler = im.fetchone()
            im.execute("""SELECT * FROM kullaniciYetkileri WHERE kullaniciId = '%s'"""%(kullaniciId))
            yetkiler = im.fetchone()
            veriler = veriler | yetkiler
            veriler["durum"] = True
            veriler["mesaj"] = "Islem basarili!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/kullanici/guncelle/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def kullaniciGuncelle():
    erisimKodu = request.form["erisimKodu"]
    kullaniciId = request.form["kullaniciId"]
    sifre = request.form["sifre"]
    firmalarDuzenle = request.form["firmalarDuzenle"]
    musterilerDuzenle = request.form["musterilerDuzenle"]
    arsivKlasorleriDuzenle = request.form["arsivKlasorleriDuzenle"]
    branslarDuzenle = request.form["branslarDuzenle"]
    sigortaSirketleriDuzenle = request.form["sigortaSirketleriDuzenle"]
    bireyselIslerDuzenle = request.form["bireyselIslerDuzenle"]
    ortakIslerDuzenle = request.form["ortakIslerDuzenle"]
    alacaklarDuzenle = request.form["alacaklarDuzenle"]
    verilenlerDuzenle = request.form["verilenlerDuzenle"]
    kullanicilarDuzenle = request.form["kullanicilarDuzenle"]
    kayitlarGoruntule = request.form["kayitlarGoruntule"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "kullanicilarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM kullanicilar WHERE id = '%s'"""%(kullaniciId))
            if(im.fetchone()):
                im.execute("""UPDATE kullanicilar SET sifre = '%s' WHERE id='%s'"""%(sifre, kullaniciId))
                im.execute("""UPDATE kullaniciYetkileri SET firmalarDuzenle = '%s', musterilerDuzenle = '%s', arsivKlasorleriDuzenle = '%s', branslarDuzenle = '%s', sigortaSirketleriDuzenle = '%s', bireyselIslerDuzenle = '%s', ortakIslerDuzenle = '%s', alacaklarDuzenle = '%s', verilenlerDuzenle = '%s', kullanicilarDuzenle = '%s', kayitlarGoruntule = '%s' WHERE kullaniciId = '%s'"""%(firmalarDuzenle, musterilerDuzenle, arsivKlasorleriDuzenle, branslarDuzenle, sigortaSirketleriDuzenle, bireyselIslerDuzenle, ortakIslerDuzenle, alacaklarDuzenle, verilenlerDuzenle, kullanicilarDuzenle, kayitlarGoruntule, kullaniciId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde kullanici guncellendi!"
            else:
                veriler["durum"] = False
                veriler["mesaj"] = "Kullanici bulunamadi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Kullanici guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/firma/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def firmaEkle():
    erisimKodu = request.form["erisimKodu"]
    firmaAdi = request.form["firmaAdi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "firmalarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM firmalar WHERE ad = '%s'"""%(firmaAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Firma adi baska bir firma tarafindan kullanilmakta!"
            else:
                im.execute("""INSERT INTO firmalar (ad) VALUES ('%s')"""%(firmaAdi))
                get_db().commit()
                im.execute("""SELECT id FROM firmalar WHERE ad = '%s'"""%(firmaAdi))
                firmaId = im.fetchone()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde firma eklendi!"
                veriler["firmaId"] = firmaId["id"]
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Firma eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/firma/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def firmaGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "firmalarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM firmalar""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/firma/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def firmaGuncelle():
    erisimKodu = request.form["erisimKodu"]
    firmaAdi = request.form["firmaAdi"]
    firmaId = request.form["firmaId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "firmalarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM firmalar WHERE ad = '%s'"""%(firmaAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Firma adi baska bir firma tarafindan kullanilmakta!"
            else:
                im.execute("""UPDATE firmalar SET ad = '%s' WHERE id='%s'"""%(firmaAdi, firmaId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde firma guncellendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Firma guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/firma/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def firmaSil():
    erisimKodu = request.form["erisimKodu"]
    firmaId = request.form["firmaId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "firmalarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM firmalar WHERE id = '%s'"""%(firmaId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Firma bulunamadi!"
            else:
                im.execute("""DELETE FROM firmalar WHERE id = '%s'"""%(firmaId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde firma silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Firma silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/arsiv/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def arsivKlasoruEkle():
    erisimKodu = request.form["erisimKodu"]
    arsivKlasoruAdi = request.form["arsivKlasoruAdi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "arsivKlasorleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM arsivKlasorleri WHERE ad = '%s'"""%(arsivKlasoruAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Arsiv klasoru adi baska bir klasor tarafindan kullanilmakta!"
            else:
                im.execute("""INSERT INTO arsivKlasorleri (ad) VALUES ('%s')"""%(arsivKlasoruAdi))
                get_db().commit()
                im.execute("""SELECT id FROM arsivKlasorleri WHERE ad = '%s'"""%(arsivKlasoruAdi))
                arsivKlasoruId = im.fetchone()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde klasor eklendi!"
                veriler["arsivKlasoruId"] = arsivKlasoruId["id"]
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Klasor eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/arsiv/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def arsivGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "arsivKlasorleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM arsivKlasorleri""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/arsiv/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def arsivGuncelle():
    erisimKodu = request.form["erisimKodu"]
    arsivKlasoruId = request.form["arsivKlasoruId"]
    arsivKlasoruAdi = request.form["arsivKlasoruAdi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "arsivKlasorleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM arsivKlasorleri WHERE ad = '%s'"""%(arsivKlasoruAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Klasor adi baska bir klasor tarafindan kullanilmakta!"
            else:
                im.execute("""UPDATE arsivKlasorleri SET ad = '%s' WHERE id= '%s'"""%(arsivKlasoruAdi, arsivKlasoruId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde klasor guncellendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Klasor guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/arsiv/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def arsivSil():
    erisimKodu = request.form["erisimKodu"]
    arsivKlasoruId = request.form["arsivKlasoruId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "arsivKlasorleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM arsivKlasorleri WHERE id = '%s'"""%(arsivKlasoruId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Klasor bulunamadi!"
            else:
                im.execute("""DELETE FROM arsivKlasorleri WHERE id = '%s'"""%(arsivKlasoruId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde klasor silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Klasor silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/brans/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def bransEkle():
    erisimKodu = request.form["erisimKodu"]
    bransAdi = request.form["bransAdi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "branslarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM branslar WHERE ad = '%s'"""%(bransAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Brans adi baska bir brans tarafindan kullanilmakta!"
            else:
                im.execute("""INSERT INTO branslar (ad) VALUES ('%s')"""%(bransAdi))
                get_db().commit()
                im.execute("""SELECT id FROM branslar WHERE ad = '%s'"""%(bransAdi))
                bransId = im.fetchone()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde brans eklendi!"
                veriler["bransId"] = bransId["id"]
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Brans eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/brans/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def bransGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "branslarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM branslar""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/brans/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def bransGuncelle():
    erisimKodu = request.form["erisimKodu"]
    bransId = request.form["bransId"]
    bransAdi = request.form["bransAdi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "branslarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM branslar WHERE ad = '%s'"""%(bransAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Brans adi baska bir klasor tarafindan kullanilmakta!"
            else:
                im.execute("""UPDATE branslar SET ad = '%s' WHERE id= '%s'"""%(bransAdi, bransId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde brans guncellendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "brans guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/brans/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def bransSil():
    erisimKodu = request.form["erisimKodu"]
    bransId = request.form["bransId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "branslarDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM branslar WHERE id = '%s'"""%(bransId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Brans bulunamadi!"
            else:
                im.execute("""DELETE FROM branslar WHERE id = '%s'"""%(bransId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde brans silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Brans silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/sirket/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def sirketEkle():
    erisimKodu = request.form["erisimKodu"]
    sigortaSirketiAdi = request.form["sigortaSirketiAdi"]
    fotografYolu = request.form["fotografYolu"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "sigortaSirketleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM sigortaSirketleri WHERE ad = '%s'"""%(sigortaSirketiAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Sirket adi baska bir sirket tarafindan kullanilmakta!"
            else:
                dosyaTuru = os.path.splitext(fotografYolu)[1]
                if(dosyaTuru == ".png" or dosyaTuru == ".jpeg" or dosyaTuru == ".jpg"):
                    yeniDosyaAdi = str(uuid.uuid4()) + dosyaTuru
                    shutil.copyfile(fotografYolu, './fotograflar/' + yeniDosyaAdi)
                    im.execute("""INSERT INTO sigortaSirketleri (ad, fotografYolu) VALUES ('%s', '%s')"""%(sigortaSirketiAdi, yeniDosyaAdi))
                    get_db().commit()
                    im.execute("""SELECT id FROM sigortaSirketleri WHERE ad = '%s'"""%(sigortaSirketiAdi))
                    sigortaSirketiId = im.fetchone()
                    veriler["durum"] = True
                    veriler["mesaj"] = "Basarili sekilde sirket eklendi!"
                    veriler["sigortaSirketiId"] = sigortaSirketiId["id"]
                else:
                    veriler["durum"] = False
                    veriler["mesaj"] = "Dosya turu gecersiz!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Sirket eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/sirket/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def sirketGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "sigortaSirketleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM sigortaSirketleri""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/sirket/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def sirketGuncelle():
    erisimKodu = request.form["erisimKodu"]
    sigortaSirketiId = request.form["sigortaSirketiId"]
    sigortaSirketiAdi = request.form["sigortaSirketiAdi"]
    fotografYolu = request.form["fotografYolu"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "sigortaSirketleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM sigortaSirketleri WHERE ad = '%s'"""%(sigortaSirketiAdi))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Sirket adi baska bir sirket tarafindan kullanilmakta!"
            else:
                dosyaTuru = os.path.splitext(fotografYolu)[1]
                if(dosyaTuru == ".png" or dosyaTuru == ".jpeg" or dosyaTuru == ".jpg"):
                    yeniDosyaAdi = str(uuid.uuid4()) + dosyaTuru
                    shutil.copyfile(fotografYolu, './fotograflar/' + yeniDosyaAdi)
                    im.execute("""SELECT * FROM sigortaSirketleri WHERE id = '%s'"""%(sigortaSirketiId))
                    bilgi = im.fetchone()
                    os.remove("./fotograflar/" + bilgi["fotografYolu"])
                    im.execute("""UPDATE sigortaSirketleri SET ad = '%s', fotografYolu = '%s' WHERE id = '%s'"""%(sigortaSirketiAdi, yeniDosyaAdi, sigortaSirketiId))
                    get_db().commit()
                    veriler["durum"] = True
                    veriler["mesaj"] = "Basarili sekilde sirket guncellendi!"
                else:
                    veriler["durum"] = False
                    veriler["mesaj"] = "Dosya turu gecersiz!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Sirket guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/sirket/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def sirketSil():
    erisimKodu = request.form["erisimKodu"]
    sigortaSirketiId = request.form["sigortaSirketiId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "sigortaSirketleriDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM sigortaSirketleri WHERE id = '%s'"""%(sigortaSirketiId))
            bilgiler = im.fetchone()
            if(not bilgiler):
                veriler["durum"] = False
                veriler["mesaj"] = "Sirket bulunamadi!"
            else:
                os.remove("./fotograflar/" + bilgiler["fotografYolu"])
                im.execute("""DELETE FROM sigortaSirketleri WHERE id = '%s'"""%(sigortaSirketiId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde sirket silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Sirket silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/musteri/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def musteriEkle():
    erisimKodu = request.form["erisimKodu"]
    musteriAdi = request.form["musteriAdi"]
    musteriSoyadi = request.form["musteriSoyadi"]
    musteriTc = request.form["musteriTc"]
    musteriDogumTarihi = request.form["musteriDogumTarihi"]
    musteriTelefon = request.form["musteriTelefon"]
    musteriMailAdresi = request.form["musteriMailAdresi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "musterilerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM musteriler WHERE tc = '%s'"""%(musteriTc))
            if(im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Musteri Tc baska bir musteri tarafindan kullanilmakta!"
            else:
                im.execute("""INSERT INTO musteriler (ad, soyad, tc, dogumTarihi, telefon, mailAdresi) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"""%(musteriAdi, musteriSoyadi, musteriTc, musteriDogumTarihi, musteriTelefon, musteriMailAdresi))
                get_db().commit()
                im.execute("""SELECT id FROM musteriler WHERE tc = '%s'"""%(musteriTc))
                musteriId = im.fetchone()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde musteri eklendi!"
                veriler["musteriId"] = musteriId["id"]
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Musteri eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/musteri/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def musteriGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "musterilerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT id, ad, soyad, telefon, tc FROM musteriler""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/musteri/goster/tek/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def musteriGosterTek():
    erisimKodu = request.form["erisimKodu"]
    musteriId = request.form["musteriId"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "musterilerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM musteriler WHERE id = '%s'"""%(musteriId))
            veriler = im.fetchone()
            veriler["durum"] = True
            veriler["mesaj"] = "Islem basarili!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/musteri/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def musteriGuncelle():
    erisimKodu = request.form["erisimKodu"]
    musteriId = request.form["musteriId"]
    musteriAdi = request.form["musteriAdi"]
    musteriSoyadi = request.form["musteriSoyadi"]
    musteriTc = request.form["musteriTc"]
    musteriDogumTarihi = request.form["musteriDogumTarihi"]
    musteriTelefon = request.form["musteriTelefon"]
    musteriMailAdresi = request.form["musteriMailAdresi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "musterilerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM musteriler WHERE id = '%s'"""%(musteriId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Musteri bulunamadi!"
            else:
                im.execute("""UPDATE musteriler SET ad = '%s', soyad = '%s', tc = '%s', dogumTarihi = '%s', telefon = '%s', mailAdresi = '%s' WHERE id= '%s'"""%(musteriAdi, musteriSoyadi, musteriTc, musteriDogumTarihi, musteriTelefon, musteriMailAdresi, musteriId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde musteri guncellendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Musteri guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/musteri/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def musteriSil():
    erisimKodu = request.form["erisimKodu"]
    musteriId = request.form["musteriId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "musterilerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM musteriler WHERE id = '%s'"""%(musteriId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Musteri bulunamadi!"
            else:
                im.execute("""DELETE FROM musteriler WHERE id = '%s'"""%(musteriId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde musteri silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Musteri silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/is/bireysel/ekle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def isBireyselEkle():
    erisimKodu = request.form["erisimKodu"]
    musteriId = request.form["musteriId"]
    bransId = request.form["bransId"]
    sigortaSirketiId = request.form["sigortaSirketiId"]
    arsivId = request.form["arsivId"]
    plaka = request.form["plaka"]
    ruhsatSeriNo = request.form["ruhsatSeriNo"]
    policeNo = request.form["policeNo"]
    policeBitisTarihi = request.form["policeBitisTarihi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "bireyselIslerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""INSERT INTO islerBireysel (musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""%(musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi))
            get_db().commit()
            veriler["durum"] = True
            veriler["mesaj"] = "Basarili sekilde is eklendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Is eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/is/bireysel/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def isBireyselGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "bireyselIslerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM islerBireysel""")
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/is/bireysel/musteri/goster/hepsi/', methods = ['POST'])
@cross_origin(supports_credentials = True)
def isBireyselMusteriGosterHepsi():
    erisimKodu = request.form["erisimKodu"]
    musteriId = request.form["musteriId"]
    kid = oturumKontrol(erisimKodu)
    veriler = {}

    if(kid):
        yetki = yetkiKontrol(kid, "bireyselIslerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM islerBireysel WHERE musteriId = '%s'"""%(musteriId))
            veriler = im.fetchall()
            veri = {}
            veri["durum"] = True
            veri["mesaj"] = "Islem basarili!"
            veriler.insert(0, veri)
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Bu islem icin yetkiniz yok!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"

    return jsonify(veriler)

@app.route('/is/bireysel/guncelle/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def isBireyselGuncelle():
    erisimKodu = request.form["erisimKodu"]
    isId = request.form["isId"]
    musteriId = request.form["musteriId"]
    bransId = request.form["bransId"]
    sigortaSirketiId = request.form["sigortaSirketiId"]
    arsivId = request.form["arsivId"]
    plaka = request.form["plaka"]
    ruhsatSeriNo = request.form["ruhsatSeriNo"]
    policeNo = request.form["policeNo"]
    policeBitisTarihi = request.form["policeBitisTarihi"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "bireyselIslerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM islerBireysel WHERE id = '%s'"""%(isId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Is bulunamadi!"
            else:
                im.execute("""UPDATE islerBireysel SET musteriId = '%s', bransId = '%s', sigortaSirketiId = '%s', arsivId = '%s', plaka = '%s', ruhsatSeriNo = '%s', policeNo = '%s', policeBitisTarihi = '%s' WHERE id = '%s'"""%(musteriId, bransId, sigortaSirketiId, arsivId, plaka, ruhsatSeriNo, policeNo, policeBitisTarihi, isId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde is guncellendi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Is guncellemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/is/bireysel/sil/', methods = ["POST"])
@cross_origin(supports_credentials = True)
def isBireyselSil():
    erisimKodu = request.form["erisimKodu"]
    isId = request.form["musteriId"]

    kid = oturumKontrol(erisimKodu)
    veriler = {}
    if(kid):
        yetki = yetkiKontrol(kid, "bireyselIslerDuzenle")
        if(yetki):
            im = get_db().cursor()
            im.execute("""SELECT * FROM islerBireysel WHERE id = '%s'"""%(isId))
            if(not im.fetchone()):
                veriler["durum"] = False
                veriler["mesaj"] = "Is bulunamadi!"
            else:
                im.execute("""DELETE FROM islerBireysel WHERE id = '%s'"""%(isId))
                get_db().commit()
                veriler["durum"] = True
                veriler["mesaj"] = "Basarili sekilde is silindi!"
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Is silmek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)


app.run()