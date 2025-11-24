import os
from werkzeug.utils import secure_filename
import math
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from functools import wraps
from form import LoginAuthencation, FormEditKaryawan, FormAddKaryawan
from models import Karyawan, AdminAuth, ProfileKami

app = Flask(__name__, static_folder='static', static_url_path='/')
app.config['SECRET_KEY'] = 'aifhe80qry4yefhncnvauhqer7yfdhdj'


def login_first(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    form = LoginAuthencation()
    model = AdminAuth()
    if request.method == 'POST':
        if form.validate_on_submit():
            username_input = form.username.data
            password_input = form.password.data

            auth = model.cek_login(username_input, password_input)

            if auth == True:
                session['username'] = username_input
                flash("Login berhasil", 'success')
                return redirect(url_for('index'))
            else:
                flash("Username atau password salah", 'danger')
        else:
            errors = form.errors.items()
            return render_template('auth/login.html', form=form, errors=errors)

    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/dashboard/home')
@login_first
def index():
    model = Karyawan()
    page = int(request.args.get('page', 1))
    pageout = int(request.args.get('pageout', 1))
    limit = 10

    data_masuk, total = model.getKaryawanJoinThisMonth(page, limit)
    data_keluar, total_out = model.getKaryawanOut(pageout, limit)

    total_pages = math.ceil(total / limit)
    total_pages_out = math.ceil(total_out / limit)
    departemen = ["Engineering", "Product", "Marketing"]

    return render_template(
        'dashboard/index.html',
        departemen=departemen,
        data_masuk=data_masuk,
        data_keluar=data_keluar,
        titleTopBar="Dashboard",
        username='Admin',
        page=page,
        pageout=pageout,
        total_pages=total_pages,
        total_pages_out=total_pages_out
    )


@app.route('/dashboard/profile/staphsec')
def profile():
    model = ProfileKami()
    data = model.getAllProfile()
    print(data)
    return render_template(
        '/dashboard/profile.html',
        data=data, 
        titleTopBar="Profile Kami",
        username="StaphSec"
    )


@app.route('/dashboard/home/search_join')
@login_first
def search_join():
    model = Karyawan()
    page = int(request.args.get('page', 1))
    pageout = int(request.args.get('pageout', 1))
    limit = 10
    keyword = request.args.get('join', '')

    data_masuk, total = model.searchJoin(keyword, page, limit)
    data_keluar, total_out = model.getKaryawanOut(pageout, limit)

    total_pages = math.ceil(total/limit)
    total_pages_out = math.ceil(total_out/limit)
    return render_template(
        'dashboard/index.html',
        data_masuk=data_masuk,
        data_keluar=data_keluar,
        titleTopBar='Dashboard',
        page=page,
        pageout=pageout,
        total_pages=total_pages,
        total_pages_out=total_pages_out
    )


@app.route('/dashboard/home/search_out')
@login_first
def search_out():
    model = Karyawan()
    page = int(request.args.get('page', 1))
    pageout = int(request.args.get('pageout', 1))
    limit = 10
    keyword = request.args.get('out', '')

    data_masuk, total = model.getKaryawanJoinThisMonth(page, limit)
    data_keluar, total_out = model.searchOut(keyword, pageout, limit)
    total_pages = math.ceil(total/limit)
    total_pages_out = math.ceil(total_out/limit)

    return render_template(
        'dashboard/index.html',
        data_masuk=data_masuk,
        data_keluar=data_keluar,
        titleTopBar='Dashboard',
        page=page,
        pageout=pageout,
        total_pages=total_pages,
        total_pages_out=total_pages_out
    )


@app.route('/dashboard/data_karyawan')
@login_first
def data_karyawan():
    model = Karyawan()

    page = int(request.args.get('page', 1))
    limit = 15

    data, total = model.getAllKaryawan(page, limit)
    total_pages = math.ceil(total/limit)
    return render_template(
        'dashboard/karyawan.html',
        titleTopBar="Karyawan",
        username="Admin",
        data=data,
        page=page,
        total_pages=total_pages
    )


@app.route('/dashboard/data_karyawan/search_karyawan')
@login_first
def search_karyawan():
    model = Karyawan()
    page = int(request.args.get('page', 1))

    limit = 15
    keyword = request.args.get('karyawan', '')

    data, total = model.searchKaryawan(keyword, page, limit)
    total_pages = math.ceil(total/limit)
    return render_template(
        'dashboard/karyawan.html',
        titleTopBar="Karyawan",
        username="Admin",
        data=data,
        page=page,
        total_pages=total_pages
    )


@app.route('/dashboard/data_karyawan/detail/<nip>')
@login_first
def detail(nip):
    model = Karyawan()
    data = model.getKaryawanByNip(nip)
    if not data:
        flash('Data tidak ditemukan', 'info')
        return redirect(url_for('index'))

    nama = data[1]

    if data:
        return render_template(
            'dashboard/detailKaryawan.html',
            titleTopBar=f"Detail {nama}",
            username="Admin",
            data=data
        )
    flash("Data tidak ditemukan!", 'danger')
    return redirect(url_for('data_karyawan'))


@app.route('/dashboard/data_karyawan/detail_keluar/<nip>')
@login_first
def detail_karyawan_keluar(nip):
    model = Karyawan()
    data = model.getDetailKaryawanOut(nip)

    if not data:
        flash("Data tidak ditemukan", "info")
        return redirect(url_for('data_karyawan'))

    nama = data[1]
    keluar = True

    if data:
        return render_template(
            'dashboard/detailKaryawan.html',
            titleTopBar=f"Detail Keluar - {nama}",
            username="Admin",
            data=data,
            keluar=keluar
        )
    flash("Data tidak ditemukan!", 'danger')
    return redirect(url_for('data_karyawan'))


@app.route('/dashboard/data_karyawan/detail/hapus/<nip>', methods=['POST'])
def delete(nip):
    model = Karyawan()

    tanggal_keluar = request.form.get('tanggal_keluar')
    status = request.form.get('status')
    status_valid = ["Resign", "PHK"]

    if status not in status_valid:
        flash("Status tidak valid, Anda jangan macam-macam!", 'warning')
        return redirect(url_for('detail', nip=nip))

    if not tanggal_keluar or not status:
        flash('Silahkan masukan tanggal', 'danger')
        return redirect(url_for('detail', nip=nip))

    if model.soft_delete_karyawan(nip, status, tanggal_keluar):
        flash(f"karyawan berhasil di {status}", 'success')
        return redirect(url_for('data_karyawan'))
    else:
        flash("Gagal menghapus data karyawan!", 'warning')
        return redirect(url_for('detail', nip=nip))


@app.route('/manajemen_karyawan', methods=['GET', 'POST'])
@login_first
def manajemen_karyawan():
    model = Karyawan()
    form = FormAddKaryawan()

    total_karyawan_aktif = model.karyawanAktif()
    total_karyawan_keluar = model.KaryawanKeluar()

    # 1. ISI DROPDOWN DEPARTEMEN (Wajib di awal)
    list_dept = model.getAllDepartemen()
    form.departemen.choices = [(row[0], row[1]) for row in list_dept]

    # 2. LOGIKA DEPENDENT DROPDOWN JABATAN
    if request.method == 'POST':
        # Kalau Submit: Ambil ID Dept dari inputan user
        dept_id = form.departemen.data
        list_jabatan = model.getJabatanByDept(dept_id)
        form.jabatan.choices = [(j['id'], j['nama']) for j in list_jabatan]
    else:
        # Kalau GET: Kosongin aja atau default (opsional)
        form.jabatan.choices = []

    # 3. PROSES SUBMIT
    if request.method == 'POST':
        if form.validate_on_submit():

            nama_foto_db = 'default.jpg'  # Default kalau gak upload
            file_path_sementara = None   # Penanda buat rollback

            # --- PROSES UPLOAD FOTO ---
            if form.foto_profil.data:
                file_gambar = form.foto_profil.data
                filename = secure_filename(file_gambar.filename)

                nama_unik = f"{form.nip.data}_{filename}"

                save_path = os.path.join(
                    app.root_path, 'static/uploads', nama_unik)
                file_gambar.save(save_path)

                nama_foto_db = nama_unik
                file_path_sementara = save_path

            # --- INSERT KE DATABASE ---
            berhasil = model.add_karyawan(
                nip=form.nip.data,
                nama=form.nama.data,
                jenis_kelamin=form.jenis_kelamin.data,
                id_jabatan=form.jabatan.data,
                alamat=form.alamat.data,
                email=form.email.data,
                no_hp=form.no_hp.data,
                foto=nama_foto_db,
                tgl_gabung=form.tanggal_bergabung.data
            )

            if berhasil:
                # SUKSES: Redirect ke Data Karyawan
                flash("Data karyawan berhasil ditambahkan!", "success")
                return redirect(url_for('data_karyawan'))
            else:
                # GAGAL: ROLLBACK FILE (Hapus Foto Sampah)
                if file_path_sementara and os.path.exists(file_path_sementara):
                    os.remove(file_path_sementara)
                    print(
                        f"Rollback: File {nama_foto_db} berhasil dihapus karena DB gagal.")

                flash("Gagal menyimpan ke database (Cek NIP kembar?)", "danger")

        else:
            errors = form.errors.items()
            return render_template(
                'dashboard/manajemen.html',
                username="Admin",
                titleTopBar="Manajemen Data",
                form=form,
                errors=errors,
                total_aktif=total_karyawan_aktif[0],
                total_keluar=total_karyawan_keluar[0]
            )

    return render_template(
        'dashboard/manajemen.html',
        username="Admin",
        titleTopBar="Manajemen Data",
        form=form,
        total_aktif=total_karyawan_aktif[0],
        total_keluar=total_karyawan_keluar[0]
    )


@app.route('/manajemen_karyawan/edit/<nip>', methods=['POST', 'GET'])
@login_first
def edit_data(nip):
    model = Karyawan()
    form = FormEditKaryawan()
    data_lama = model.getKaryawanByNip(nip)

    if not data_lama:
        flash("Data tidak ditemukan!", 'warning')
        return redirect(url_for('index'))

    list_dept = model.getAllDepartemen()
    form.departemen.choices = [(row[0], row[1]) for row in list_dept]

    if request.method == 'POST':
        dept_id = form.departemen.data
    else:
        dept_id = data_lama[12]

    list_jabatan = model.getJabatanByDept(dept_id)
    form.jabatan.choices = [(j['id'], j['nama']) for j in list_jabatan]

    nama = data_lama[1]

    if request.method == 'GET':
        form.alamat.data = data_lama[5]
        form.jabatan.data = data_lama[13]
        form.departemen.data = data_lama[12]
        form.email.data = data_lama[6]
        form.no_hp.data = data_lama[7]

    if request.method == 'POST':
        if form.validate_on_submit():
            cek_jab = form.jabatan.data == data_lama[13]
            cek_dept = form.departemen.data == data_lama[12]
            cek_email = form.email.data == data_lama[6]
            cek_hp = form.no_hp.data == data_lama[7]
            cek_alamat = form.alamat.data == data_lama[5]

            if cek_jab and cek_dept and cek_email and cek_hp and cek_alamat:
                flash("Tidak ada data yang berubah.", 'info')
                return redirect(url_for('detail', nip=nip))

            berhasil = model.update_data_karyawan(
                nip=nip,
                jabatan=form.jabatan.data,
                email=form.email.data,
                no_hp=form.no_hp.data,
                alamat=form.alamat.data,
            )

            if berhasil:
                flash("Data berhasil diupdate!", 'success')
                return redirect(url_for('detail', nip=nip))
            else:
                flash("Gagal mengupdate database!", 'danger')
                return redirect(url_for('edit_data', nip=nip))

        else:
            errors = form.errors.items()
            return render_template(
                'dashboard/edit.html',
                form=form, errors=errors,
                data=data_lama, username='Admin',
                titleTopBar=f"Edit Data - {nama}"
            )

    return render_template(
        'dashboard/edit.html',
        titleTopBar=f"Edit Data - {nama}",
        username="Admin",
        data=data_lama,
        form=form
    )


@app.route('/api/jabatan/<int:id_dept>')
def get_jabatan_by_dept(id_dept):
    model = Karyawan()

    data_jabatan = model.getJabatanByDept(id_dept)
    return jsonify(data_jabatan)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404/404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
