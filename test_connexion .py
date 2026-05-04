import pymysql

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',   # laissez vide si pas de mot de passe sous Wamp
        database='esatic'
    )
    print("✅ Connexion réussie à MySQL / base esatic")
    conn.close()
except Exception as e:
    print(f"❌ Échec de connexion : {e}")