from db import *
db = DB()

user_id = db.get_user_id('Adnan')
for i in db.get_data('Adnan'):
    print(i)
z = []
for i in db.get_bmi_date(user_id):
    x = float(i[0])
    z.append(x)
print("Z is ", z)
print(type(z[0]))