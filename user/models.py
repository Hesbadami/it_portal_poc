from django.db import models, connection
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=150)
    employee_count = models.IntegerField()
    primary_contact_name = models.CharField(max_length=150)
    primary_contact_email = models.CharField(max_length=150)
    secondary_contact_name = models.CharField(max_length=150)
    secondary_contact_email = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Office(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=150)


class user(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)
    full_name = models.CharField(max_length=150)
    permissions = models.TextField()
    office = models.ForeignKey(Office, on_delete=models.DO_NOTHING, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, null=True, blank=True)
    max_tokens = models.IntegerField(null=True)
    max_cost = models.IntegerField(null=True)
    max_chats = models.IntegerField(null=True)
    
    class Meta:
        db_table = "users"
        get_latest_by = "user_id"

    def __str__(self):
        return self.full_name

def get_user(username):
    
    cursor = connection.cursor()
    query = "SELECT * FROM users where username = %s"
    cursor.execute(query, [username])
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    cursor.close()
   
def get_user_by_id(user_id):
    
    cursor = connection.cursor()
    query = "SELECT * FROM users where user_id = %s"
    cursor.execute(query, [user_id])
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    cursor.close()
   
def get_company_by_user_id(user_id):
    
    cursor = connection.cursor()
    query = "SELECT * FROM user_company WHERE id = (SELECT company_id FROM users where user_id = %s)"
    cursor.execute(query, [user_id])
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    cursor.close()