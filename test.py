from loader import *
cursor.execute('select id_scheduler from users where id=(?)',(731866035,))
id_scheduler = cursor.fetchall()[0][0]
