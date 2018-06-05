import sqlite3

conn = sqlite3.connect('pk_user.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE user_list(username text, password text, wallet real, plate text, in_time integer)")
cursor.execute("INSERT INTO user_list VALUES ('admin', 'password' , 999, '6LIK274', 0)")
cursor.execute("SELECT * FROM user_list WHERE plate = '6LIK274'")
print(cursor.fetchone())
conn.commit()
conn.close()
