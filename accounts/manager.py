
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    
    def create_user(self , username, email, password , **extrafields):
        if not username:
            raise ValueError('Username must be Set')
        
        if not email:
            raise ValueError('Email must be Set')
        
        email = self.normalize_email(email)
        user = self.model(
           username = username,email = email, password=password, **extrafields
        )
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self , username, email,password, **extrafields):
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_active', True)

        if extrafields.get('is_staff') is not True:
            raise ValueError(('superuser is musthave  is_staff True' ))
        if extrafields.get('is_superuser') is not True:
            raise ValueError(('superuser is musthave is_superuser True' ))
        return self.create_user(username, email, password, **extrafields)
