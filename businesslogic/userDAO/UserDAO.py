from user.models import CustomerUser

class UserDAO():
    def getAllUser():
        userList = CustomerUser.objects.filter(is_active=True)
        return userList

    def getUserByID(user_id):
        user = CustomerUser.objects.get(pk=user_id, is_active=True)
        return user