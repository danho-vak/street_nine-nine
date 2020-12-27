from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

'''
    class UserManager
     - BaseUserManager를 상속받아 구현한 클래스

     - class methods
        create_user         : 넘겨받은 파라미터로 user 인스턴스 생성
        create_superuser    : 넘겨받은 파라미터로 super user 인스턴스 생성
'''
class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email or not username or not password:
            raise ValueError('모든 필드값을 입력해주세요!')

        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


'''
    class UserManager
     - AbstractBaseUser를 상속받아 구현한 클래스

     - class methods
        __str__             : 해당 object를 문자열로 설명하는 함수 (return str)
        has_perm            : 사용자에게 특정 권한이 있는지 (return bool)
        has_module_perms    : 사용자에게 앱 'app_label'을 볼 수 있는 권한이 있는지 (return bool)
        is_staff            : 해당 유저가 어드민 유저인지 (return bool)
'''
class User(AbstractBaseUser):
    objects = UserManager

    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20)
    date_of_birth = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIEDL = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    def __str__(self):
        return '{} : {}'.format(self.email, self.username)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin