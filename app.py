import math
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session
from functools import wraps

from form import LoginAuthencation
from models import Karyawan, AdminAuth

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


@app.route('/data_jabatan/<dept>')
def get_data(dept):
    data = {
        "Engineering": ["Backend Engineer", "Frontend Engineer", "DevOps Engineer"],
        "Product": ["Product Manager", "UI/UX Designer", "UX Researcher"],
        "Marketing": ["Digital Marketer", "SEO Specialist"],
    }

    if dept in data:
        return jsonify(data[dept])

    return redirect(url_for('index'))


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
    data = model.details(nip)

    if data:
        return render_template(
            'dashboard/detailKaryawan.html',
            titleTopBar="Detail",
            username="Admin",
            data=data
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


@app.route('/manajemen_karyawan')
@login_first
def manajemen_karyawan():
    return 'hello'


@app.route('/manajemen_karyawan/edit/<nip>')
@login_first
def edit_data(nip):
    return "hai"


if __name__ == '__main__':
    app.run(debug=True)
