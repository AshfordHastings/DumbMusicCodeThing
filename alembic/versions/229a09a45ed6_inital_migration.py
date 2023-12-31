"""inital migration

Revision ID: 229a09a45ed6
Revises: 
Create Date: 2023-08-13 13:41:23.063306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '229a09a45ed6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
    sa.Column('artistId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('artistId')
    )
    op.create_table('permissions',
    sa.Column('permissionId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('permissionName', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('permissionId')
    )
    op.create_table('playlists',
    sa.Column('playlistId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('playlistId')
    )
    op.create_table('roles',
    sa.Column('roleId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('roleName', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('roleId')
    )
    op.create_table('users',
    sa.Column('userId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('displayName', sa.String(), nullable=False),
    sa.Column('date_registered', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('userId')
    )
    op.create_table('permissions_to_roles',
    sa.Column('permissionId', sa.Integer(), nullable=False),
    sa.Column('roleId', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['permissionId'], ['permissions.permissionId'], ),
    sa.ForeignKeyConstraint(['roleId'], ['roles.roleId'], ),
    sa.PrimaryKeyConstraint('permissionId', 'roleId')
    )
    op.create_table('songs',
    sa.Column('songId', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('artistId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artistId'], ['artists.artistId'], ),
    sa.PrimaryKeyConstraint('songId')
    )
    op.create_table('users_to_roles',
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('roleId', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['roleId'], ['roles.roleId'], ),
    sa.ForeignKeyConstraint(['userId'], ['users.userId'], ),
    sa.PrimaryKeyConstraint('userId', 'roleId')
    )
    op.create_table('playlists_to_songs',
    sa.Column('playlistId', sa.Integer(), nullable=False),
    sa.Column('songId', sa.Integer(), nullable=False),
    sa.Column('date_added', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.ForeignKeyConstraint(['playlistId'], ['playlists.playlistId'], ),
    sa.ForeignKeyConstraint(['songId'], ['songs.songId'], ),
    sa.PrimaryKeyConstraint('playlistId', 'songId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('playlists_to_songs')
    op.drop_table('users_to_roles')
    op.drop_table('songs')
    op.drop_table('permissions_to_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('playlists')
    op.drop_table('permissions')
    op.drop_table('artists')
    # ### end Alembic commands ###
