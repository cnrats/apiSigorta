import flask
from flask import request, jsonify, g
import sqlite3
import uuid

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
                veriler["kullaniciId"] = kullaniciId
        else:
            veriler["durum"] = False
            veriler["mesaj"] = "Kullanici eklemek icin yetkiniz bulunmuyor!"
    else:
        veriler["durum"] = False
        veriler["mesaj"] = "Oturum gecersiz!"
    return jsonify(veriler)

@app.route('/kullanici/sil/', methods = ['POST'])
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

@app.route('/kullanici/goruntule/hepsi/', methods = ['POST'])
def kullaniciGoruntuleHepsi():
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

@app.route('/kullanici/goruntule/tek/', methods = ['POST'])
def kullaniciGoruntuleTek():
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



app.run()