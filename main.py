import random
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arkademy.db'
db = SQLAlchemy(app)

class Produk(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nama_produk = db.Column(db.String(100), nullable=False)
  keterangan = db.Column(db.String(500), nullable=False)
  harga = db.Column(db.Integer, nullable=False)
  jumlah = db.Column(db.Integer, nullable=False)
  tanggal_input = db.Column(db.DateTime, default=datetime.utcnow)

  def __repr__(self):
    return 'Produk ' + str(self.id)
# from main import db
# db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
  
  if request.method == 'POST':
    tambah_nama_produk = request.form['nama_produk']
    tambah_keterangan = request.form['keterangan']
    tambah_harga = request.form['harga']
    tambah_jumlah = request.form['jumlah']
    produk_baru = Produk(nama_produk=tambah_nama_produk, keterangan=tambah_keterangan, harga=tambah_harga, jumlah=tambah_jumlah)
    db.session.add(produk_baru)
    db.session.commit()
    return redirect('/lihat')
  else:
    return render_template('index.html')


@app.route('/lihat', methods=['GET', 'POST'])
def lihat():

  semua_produk = Produk.query.order_by(Produk.id).all()
  return render_template('lihat.html', daftar_produk=semua_produk)

@app.route('/delete/<int:id>')
def delete(id):

  produk = Produk.query.get_or_404(id)
  db.session.delete(produk)
  db.session.commit()
  return redirect('/lihat')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
  
  produk = Produk.query.get_or_404(id)
  if request.method == 'POST':
    produk.nama_produk = request.form['nama_produk']
    produk.keterangan = request.form['keterangan']
    produk.harga = request.form['harga']
    produk.jumlah = request.form['jumlah']
    db.session.commit()
    return redirect('/lihat')
  else:
    return render_template('edit.html', produk=produk)

if __name__ == "__main__":
    app.run(
      debug=False, 
      host='0.0.0.0', 
      port=random.randint(2000, 9000)
    )

# db.session.add(Produk(nama_produk='Produk 1', keterangan='Ini Produk Pertama', harga=5000, jumlah=5))