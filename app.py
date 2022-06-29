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

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/kullanici/giris/', methods = ['POST'])
def giris():
    im = get_db().cursor()
    kullaniciAdi = request.form["kullaniciAdi"]
    sifre = request.form["sifre"]
    im.execute("""SELECT * FROM kullancilar WHERE kullaniciAdi='%s' AND sifre='%s'"""%(kullaniciAdi, sifre))
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
def cikis():
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

app.run()