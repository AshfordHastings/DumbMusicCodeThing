import csv
from MetadataService.domain.model import Role, Permission, PermissionRoleAssociation

CSV_PATH = 'data/roles_permissions.csv'

def seed_from_csv(session):
    roles = {}  # To store roles and avoid duplicates
    permissions = {}  # To store permissions and avoid duplicates

    with open(CSV_PATH, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            role_name = row['role']
            permission_name = row['permission']

            # Create or get role
            if role_name not in roles:
                role = session.query(Role).filter_by(roleName=role_name).first()
                if not role:
                    role = Role(roleName=role_name)
                    session.add(role)
                roles[role_name] = role
            else:
                role = roles[role_name]

            # Create or get permission
            if permission_name not in permissions:
                permission = session.query(Permission).filter_by(permissionName=permission_name).first()
                if not permission:
                    permission = Permission(permissionName=permission_name)
                    session.add(permission)
                permissions[permission_name] = permission
            else:
                permission = permissions[permission_name]

            # Create association
            association = session.query(PermissionRoleAssociation).filter_by(role=role, permission=permission).first()
            if not association:
                association = PermissionRoleAssociation(role=role, permission=permission)
                session.add(association)

        
