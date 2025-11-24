from werkzeug.security import check_password_hash
import pymysql
import config


class Karyawan:
    def __init__(self, nip=None, jabatan=None, dept=None, nama=None, alamat=None, email=None, no_hp=None, foto_profil=None, bergabung=None, keluar=None):
        self.nip = nip
        self.jabatan = jabatan
        self.dept = dept
        self.nama = nama
        self.alamat = alamat
        self.email = email
        self.no_hp = no_hp,
        self.foto_profil = foto_profil
        self.bergabung = bergabung
        self.keluar = keluar
        self.db = None
        self.cursor = None

    def openDB(self):
        self.db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            database=config.DB_NAME,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )

        self.cursor = self.db.cursor()

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def getAllKaryawan(self, page, limit):
        self.openDB()
        offset = (page - 1) * limit
        query = """
            SELECT  k.nip,
                    k.nama,
                    k.jenis_kelamin,
                    j.jabatan,
                    d.departemen,
                    k.alamat,
                    k.email,
                    k.no_hp,
                    k.foto_profil,
                    k.tanggal_bergabung,
                    k.id_jabatan
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE k.status = "Active"
            ORDER BY k.nip ASC
            LIMIT %s OFFSET %s
        """
        self.cursor.execute(query, (limit, offset))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
        """
        self.cursor.execute(count)
        total = self.cursor.fetchone()[0]

        self.closeDB()
        return data, total

    def getKaryawanJoinThisMonth(self, page, limit):
        self.openDB()
        offset = (page-1) * limit
        query = """
            SELECT  k.nama,
                    k.status,
                    k.foto_profil,
                    k.tanggal_bergabung,
                    k.nip
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d
                    ON j.id_dept = d.id_dept
            WHERE   MONTH(k.tanggal_bergabung) = MONTH(CURDATE())
                    AND YEAR(k.tanggal_bergabung) = YEAR(CURDATE())
                    AND k.status = 'Active'
            ORDER BY k.tanggal_bergabung DESC
            LIMIT %s OFFSET %s
        """
        self.cursor.execute(query, (limit, offset))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE MONTH(k.tanggal_bergabung) = MONTH(CURDATE())
              AND YEAR(k.tanggal_bergabung) = YEAR(CURDATE())
        """
        self.cursor.execute(count)
        total = self.cursor.fetchone()[0]

        self.closeDB()
        return data, total

    def getKaryawanOut(self, page, limit):
        self.openDB()
        offset = (page - 1) * limit
        query = """
            SELECT  k.nama,
                    k.status,
                    k.tanggal_keluar,
                    k.foto_profil,
                    k.nip
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            WHERE   k.tanggal_keluar IS NOT NULL
            ORDER BY k.tanggal_keluar DESC
            LIMIT %s OFFSET %s
        """

        self.cursor.execute(query, (limit, offset))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            WHERE   k.tanggal_keluar IS NOT NULL
        """

        self.cursor.execute(count)
        total_keluar = self.cursor.fetchone()[0]
        self.closeDB()
        return data, total_keluar

    def searchJoin(self, keyword, page, limit):
        self.openDB()
        offset = (page - 1) * limit
        query = """
            SELECT  k.nama,
                    j.jabatan,
                    k.tanggal_bergabung,
                    k.foto_profil,
                    d.departemen
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d
                    ON j.id_dept = d.id_dept
            WHERE   MONTH(k.tanggal_bergabung) = MONTH(CURDATE())
                    AND YEAR(k.tanggal_bergabung) = YEAR(CURDATE())
            AND (k.nama LIKE %s OR j.jabatan LIKE %s)
            ORDER BY tanggal_bergabung DESC
            LIMIT %s OFFSET %s
        """

        like_keyword = f"%{keyword}%"
        self.cursor.execute(
            query, (like_keyword, like_keyword, limit, offset,))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d
                    ON j.id_dept = d.id_dept
            WHERE   MONTH(k.tanggal_bergabung) = MONTH(CURDATE())
                    AND YEAR(k.tanggal_bergabung) = YEAR(CURDATE())
            AND (k.nama LIKE %s OR j.jabatan LIKE %s)
        """

        self.cursor.execute(count, (like_keyword,) * 2)
        total = self.cursor.fetchone()[0]
        self.closeDB()
        return data, total

    def searchOut(self, keyword, page, limit):
        self.openDB()
        offset = (page - 1) * limit
        query = """
            SELECT  k.nama,
                    k.status,
                    k.tanggal_keluar,
                    k.foto_profil
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            WHERE   k.tanggal_keluar IS NOT NULL
            AND     k.nama LIKE %s
            ORDER BY tanggal_keluar DESC
            LIMIT %s OFFSET %s
        """

        like_keyword = f"%{keyword}%"
        self.cursor.execute(query, (like_keyword, limit, offset))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j 
                    ON k.id_jabatan = j.id_jabatan
            WHERE   k.tanggal_keluar IS NOT NULL
            AND     k.nama LIKE %s
        """

        self.cursor.execute(count, (like_keyword))
        total = self.cursor.fetchone()[0]
        self.closeDB()
        return data, total

    def searchKaryawan(self, keyword, page, limit):
        self.openDB()
        offset = (page - 1) * limit
        query = """
            SELECT  k.nip,
                    k.nama,
                    k.jenis_kelamin,
                    j.jabatan,
                    d.departemen,
                    k.alamat,
                    k.email,
                    k.no_hp,
                    k.foto_profil,
                    k.tanggal_bergabung
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE k.status = 'Active' 
            AND (
                k.nama LIKE %s
                OR k.nip LIKE %s
                OR j.jabatan LIKE %s
                OR d.departemen LIKE %s
            )
            ORDER BY k.nip ASC
            LIMIT %s OFFSET %s
        """

        like_keyword = f"%{keyword}%"
        self.cursor.execute(
            query, (like_keyword, like_keyword, like_keyword, like_keyword, limit, offset))
        data = self.cursor.fetchall()

        count = """
            SELECT COUNT(*)
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE k.status = 'Active' 
            AND (
                k.nama LIKE %s
                OR k.nip LIKE %s
                OR j.jabatan LIKE %s
                OR d.departemen LIKE %s
            )
        """

        self.cursor.execute(count, (like_keyword,) * 4)
        total = self.cursor.fetchone()[0]

        self.closeDB()
        return data, total

    def getKaryawanByNip(self, nip):
        self.openDB()
        query = """
            SELECT  k.nip,
                    k.nama,
                    k.jenis_kelamin,
                    j.jabatan,
                    d.departemen,
                    k.alamat,
                    k.email,
                    k.no_hp,
                    k.foto_profil,
                    k.tanggal_bergabung,
                    k.tanggal_keluar,
                    k.status,
                    d.id_dept,
                    k.id_jabatan
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE %s = k.nip AND k.status = 'Active'
        """

        self.cursor.execute(query, (nip,))
        data = self.cursor.fetchone()
        return data

    def getDetailKaryawanOut(self, nip):
        self.openDB()
        query = """
            SELECT  k.nip,
                    k.nama,
                    k.jenis_kelamin,
                    j.jabatan,
                    d.departemen,
                    k.alamat,
                    k.email,
                    k.no_hp,
                    k.foto_profil,
                    k.tanggal_bergabung,
                    k.tanggal_keluar,
                    k.status
            FROM table_karyawan k
            JOIN table_jabatan j ON k.id_jabatan = j.id_jabatan
            JOIN table_departemen d ON j.id_dept = d.id_dept
            WHERE k.nip = %s AND k.status != 'Active'
        """

        self.cursor.execute(query, (nip,))
        data = self.cursor.fetchone()
        print(data)
        return data

    def soft_delete_karyawan(self, nip, status, tanggal_keluar):
        self.openDB()

        try:
            query = "UPDATE table_karyawan SET status = %s, tanggal_keluar = %s WHERE nip = %s"
            self.cursor.execute(query, (status, tanggal_keluar, nip))

            self.db.commit()

            if self.cursor.rowcount > 0:
                return True
            else:
                return False

        except Exception as e:
            print(f"Error: {e}")
            self.db.rollback()
            return False

        finally:
            self.closeDB()

    def update_data_karyawan(self, nip, jabatan, email, no_hp, alamat):
        self.openDB()
        query = """
            UPDATE table_karyawan
            SET id_jabatan  = %s,
                email       = %s,
                no_hp       = %s,
                alamat      = %s
            WHERE nip       = %s
        """

        value = (jabatan, email, no_hp, alamat, nip)

        self.cursor.execute(query, value)
        self.db.commit()
        return True

    def getAllDepartemen(self):
        self.openDB()
        self.cursor.execute("SELECT id_dept, departemen FROM table_departemen")
        res = self.cursor.fetchall()
        self.closeDB()
        return res

    def getJabatanByDept(self, id_dept):
        self.openDB()
        self.cursor.execute(
            "SELECT id_jabatan, jabatan FROM table_jabatan WHERE id_dept = %s", (id_dept,))
        res = [{'id': row[0], 'nama': row[1]}
               for row in self.cursor.fetchall()]
        self.closeDB()
        return res

    def add_karyawan(self, nip, nama, jenis_kelamin, id_jabatan, alamat, email, no_hp, foto, tgl_gabung):
        self.openDB()
        try:
            sql = """
                INSERT INTO table_karyawan 
                (nip, nama, jenis_kelamin, id_jabatan, alamat, email, no_hp, foto_profil, tanggal_bergabung)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            val = (nip, nama, jenis_kelamin, id_jabatan,
                   alamat, email, no_hp, foto, tgl_gabung)

            self.cursor.execute(sql, val)
            self.db.commit()
            return True

        except Exception as e:
            print(f"Error Add Karyawan: {e}")
            self.db.rollback()
            return False

        finally:
            self.closeDB()

    def karyawanAktif(self):
        self.openDB()
        query = """
            SELECT COUNT(*) FROM table_karyawan WHERE status = 'Active'
        """
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.closeDB()
        return data
    
    def KaryawanKeluar(self):
        self.openDB()
        query = """
            SELECT COUNT(*) FROM table_karyawan WHERE status != 'Active'
        """
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.closeDB()
        return data

class ProfileKami:
    def __init__(self):
        self.db = None
        self.cursor = None
    
    def openDB(self):
        self.db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            database=config.DB_NAME,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )

        self.cursor = self.db.cursor()

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            
    def getAllProfile(self):
        self.openDB()
        query = """
            SELECT * FROM profile_kami
        """
        
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        return data

class AdminAuth():
    def __init__(self):
        self.db = None
        self.cursor = None

    def openDB(self):
        self.db = pymysql.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            database=config.DB_NAME,
            password=config.DB_PASSWORD,
            port=config.DB_PORT
        )

        self.cursor = self.db.cursor()

    def closeDB(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()

    def cek_login(self, username_input, password_input):
        self.openDB()
        query = "SELECT password FROM users WHERE username = %s"
        self.cursor.execute(query, (username_input,))
        data = self.cursor.fetchone()

        self.closeDB()

        if data:
            hash_from_db = data[0]

            if check_password_hash(hash_from_db, password_input):
                return True

        return False
