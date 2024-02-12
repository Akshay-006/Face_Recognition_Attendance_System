import mysql.connector as db

employee_images=[]
emp=[]
conn=db.connect(
    host="localhost",
    user="root",
    database="face_recognition",
    password="password"
)

cursor=conn.cursor()

select_query ="Select image from employee;"

cursor.execute(select_query)

result=cursor.fetchall()

for i in result:
    employee_images.append(i)


print(employee_images)

for i in employee_images:
    str1=''.join(map(str,i))
    emp.append(str1)

print(emp)
conn.close()


