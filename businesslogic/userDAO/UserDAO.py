from user.models import CustomerUser

class UserDAO():
    def getAllUser():
        userList = CustomerUser.objects.filter(is_active=True)
        return userList