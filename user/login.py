from user.models import get_user
from django.contrib.auth.hashers import make_password, check_password

def check_user(username, password):
    user_data = get_user(username)
    #return make_password(user_data[0]['password'])
    if user_data:
        validation_result = check_password(password, user_data[0]['password'])
        if validation_result == True:
            return user_data[0]['user_id']

    return False