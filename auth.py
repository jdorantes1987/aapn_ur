import bcrypt


class AuthManager:
    MAX_INTENTOS = 5

    def __init__(self, db_conn):
        self.connection = db_conn

    def _get_user(self, username):
        cur = self.connection.get_cursor()
        cur.execute(
            "SELECT username, password, intentos_fallidos, bloqueado FROM users WHERE username = %s",
            (username,),
        )
        return cur.fetchone()

    def autenticar(self, username, password):
        user = self._get_user(username)
        if not user:
            return False, "Usuario no encontrado"

        idlogin, hash_pass, intentos, bloqueado = user

        if bloqueado:
            return False, "Usuario bloqueado por demasiados intentos fallidos"

        if bcrypt.checkpw(password.encode(), hash_pass.encode()):
            self._reset_intentos(idlogin)
            return True, "Autenticación exitosa"
        else:
            self._incrementar_intentos(idlogin, intentos)
            if intentos + 1 >= self.MAX_INTENTOS:
                self._bloquear_usuario(idlogin)
                return False, "Usuario bloqueado por demasiados intentos fallidos"
            return (
                False,
                f"Contraseña incorrecta. Intentos restantes: {self.MAX_INTENTOS - (intentos + 1)}",
            )

    def _reset_intentos(self, username):
        self.connection.execute(
            "UPDATE users SET intentos_fallidos = 0 WHERE username = %s",
            (username,),
        )

    def _incrementar_intentos(self, username, intentos):
        self.connection.execute(
            "UPDATE users SET intentos_fallidos = %s WHERE username = %s",
            (intentos + 1, username),
        )

    def _bloquear_usuario(self, username):
        self.connection.execute(
            "UPDATE users SET bloqueado = 1 WHERE username = %s", (username,)
        )

    def registrar_usuario(self, iduser, nombre, password):
        hash_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.connection.execute(
            "INSERT INTO users (username, nombre, password) VALUES (%s, %s, %s)",
            (iduser, nombre, hash_pass),
        )


if __name__ == "__main__":
    import os
    import sys

    from dotenv import load_dotenv

    sys.path.append("..\\profit")
    from conn.database_connector import DatabaseConnector
    from conn.mysql_connector import MySQLConnector

    load_dotenv(override=True)

    mysql_connector = MySQLConnector(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER_ADMIN"],
        password=os.environ["DB_PASSWORD"],
    )
    mysql_connector.connect()
    db = DatabaseConnector(mysql_connector)
    auth = AuthManager(db)
    # print("=== Prueba de registro de usuario ===")
    # iduser = input("Usuario: ")
    # nombre = input("Nombre: ")
    # password = input("Contraseña: ")
    # auth.registrar_usuario(iduser, nombre, password)
    # print("Usuario registrado.\n")

    print("=== Prueba de autenticación ===")
    iduser_login = input("Usuario para login: ")
    password_login = input("Contraseña: ")
    ok, msg = auth.autenticar(iduser_login, password_login)
    print(msg)
