from factory_boy.auth.auth_factories import (
    RoleFactory, UserFactory, UserRoleAssociationFactory
)
from MetadataService.domain.model import Role
#from auth_factories import session
from factory_boy.db import Session
from auth_seeder_scripts import seed_from_csv

# def seed_auth_db():
#     #admin_role = RoleFactory(name="admin")
#     #user_role = RoleFactory(name="user")

def seed_auth_permission_roles(session):
    seed_from_csv(session)

def generate_users_and_associate_with_roles(session, num_users=50, role_name="user"):
    users = [UserFactory(_session=session) for _ in range(num_users)]
    session.bulk_save_objects(users)
    print("hello")
    session.flush()

    role = session.query(Role).filter(Role.roleName == role_name).first()
    print(len(users))
    for user in users:
        UserRoleAssociationFactory(_session=session, user=user, role=role)



if __name__ == "__main__":
    try:
        session = Session()
        seed_auth_permission_roles(session)
        generate_users_and_associate_with_roles(session)
    except Exception as e:
        print(e)
        session.rollback()
    session.commit()