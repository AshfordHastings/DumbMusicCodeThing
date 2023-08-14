from factory import SubFactory, Faker, post_generation
from werkzeug.security import generate_password_hash
from factory.alchemy import SQLAlchemyModelFactory
from factory_boy.db import Session
from MetadataService.domain.model import (
    Role, UserRoleAssociation, Permission, PermissionRoleAssociation, User
)

#session = Session()

class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        #sqlalchemy_session = session

    name = Faker('sentence', nb_words=1)

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = 'flush'
    
    class Params:
        _session = None

    username = Faker('user_name')
    password = "testpassword123"
    email = Faker('email')
    displayName = Faker('name')

    @post_generation
    def hash_password(self, create, extracted, **kwargs):
        self.password = generate_password_hash(self.password)
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

class UserRoleAssociationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserRoleAssociation
        sqlalchemy_session_persistence = 'flush'

    class Params:
        _session = None

    user = SubFactory(UserFactory)
    role = SubFactory(RoleFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        session = kwargs.pop('_session', None)
        if session:
            cls._meta.sqlalchemy_session = session
        return super()._create(model_class, *args, **kwargs)

class PermissionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Permission
        #sqlalchemy_session = session

    permissionName = Faker('sentence', nb_words=1)

class PermissionRoleAssociationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PermissionRoleAssociation
        #sqlalchemy_session = session

    permission = SubFactory(PermissionFactory)
    role = SubFactory(RoleFactory)