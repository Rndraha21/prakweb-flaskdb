from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField, SelectField, RadioField, DateField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, ValidationError
import re


class LoginAuthencation(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(message="Silahkan isi username"),
            Length(min=4, message="Username minimal 4 karakter")
        ],
        render_kw={"placeholder": "username"}
    )

    password = PasswordField(
        'password',
        validators=(
            DataRequired(message='Silahkan isi password'),
            Length(min=4, message='Password minimal 4 karakter')
        ),
        render_kw={"placeholder": "password"}
    )


class FormEditKaryawan(FlaskForm):
    departemen = SelectField(
        'Departemen',
        choices=[],
        coerce=int,
        validators=[DataRequired(message="Pilih departemen dulu!")]
    )

    jabatan = SelectField(
        'Jabatan',
        choices=[],
        validators=[DataRequired(message="Pilih jabatan!")]
    )

    alamat = TextAreaField(
        'alamat',
        validators=[
            DataRequired(message="Alamat wajib diisi!"),
            Length(min=4, message="Alamat minimal 4 karakter")
        ],
        render_kw={"placeholder": "Alamat"}
    )

    email = EmailField(
        'email',
        validators=[
            DataRequired(message="Departemen wajib diisi!"),
            Length(min=4, message="Jabatan minimal 4 karakter"),
            Email("Silahkan masukkan email yang valid")
        ],
        render_kw={"placeholder": "habib@gmail.com"}
    )

    no_hp = StringField(
        'nohp',
        validators=[
            DataRequired(message="No HP wajib diisi"),
        ],
        render_kw={"placeholder": "081234567890"}
    )

    def validate_no_hp(form, field):
        nomor = field.data
        pattern = r"^08[0-9]{8,13}$"

        if not re.match(pattern, nomor):
            raise ValidationError(
                "Nomor HP tidak valid! (13-15) digit, diawali dengan 08")


class FormAddKaryawan(FlaskForm):
    nip = StringField(
        'NIP',
        validators=[
            DataRequired(message="NIP wajib diisi"),
            Length(min=5, message="NIP harus 5 karakter"),

        ],
        render_kw={"placeholder": "Contoh: 12345"}
    )

    nama = StringField(
        'Nama Lengkap',
        validators=[
            DataRequired(message="Nama wajib diisi"),
            Length(min=4, message="Nama minimal 4 karakter")
        ],
        render_kw={"placeholder": "Nama Lengkap"}
    )

    jenis_kelamin = RadioField(
        'Jenis Kelamin',
        choices=[('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')],
        validators=[DataRequired(message="Pilih jenis kelamin!")],
        default='Laki-laki'
    )

    departemen = SelectField(
        'Departemen',
        choices=[],
        coerce=int,
        validators=[DataRequired(message="Pilih departemen dulu!")]
    )

    jabatan = SelectField(
        'Jabatan',
        choices=[],
        validators=[DataRequired(message="Pilih jabatan!")]
    )

    tanggal_bergabung = DateField(
        'Tanggal Bergabung',
        format='%Y-%m-%d',
        validators=[DataRequired(message="Tanggal wajib diisi")]
    )

    alamat = TextAreaField(
        'Alamat',
        validators=[
            DataRequired(message="Alamat wajib diisi!"),
            Length(min=10, message="Alamat terlalu pendek, mohon lengkapi.")
        ],
        render_kw={"placeholder": "Alamat Lengkap Domisili", "rows": 3}
    )

    email = EmailField(
        'Email',
        validators=[
            DataRequired(message="Email wajib diisi!"),
            Email(message="Format email salah (harus ada @ dan .com)")
        ],
        render_kw={"placeholder": "contoh@email.com"}
    )

    no_hp = StringField(
        'No. HP',
        validators=[DataRequired(message="No HP wajib diisi")],
        render_kw={"placeholder": "081234567890"}
    )

    foto_profil = FileField(
        'Foto Profil',
        validators=[
            FileAllowed(['jpg', 'png', 'jpeg'],
                        'Hanya boleh file gambar (jpg, png)!'),
            FileRequired(message="Wajib upload foto profil")
        ]
    )

    def validate_no_hp(self, field):
        nomor = field.data
        pattern = r"^08[0-9]{8,13}$"

        if not re.match(pattern, nomor):
            raise ValidationError(
                "Nomor HP tidak valid! (10-15) digit, diawali dengan 08")
