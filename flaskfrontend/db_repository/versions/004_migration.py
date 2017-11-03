from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('password_hash', VARCHAR(length=128)),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
)

logs = Table('logs', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('filename', String),
    Column('internal_f_name', String(length=128)),
    Column('file_hash', String(length=64)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['nickname'].drop()
    post_meta.tables['logs'].columns['file_hash'].create()
    post_meta.tables['logs'].columns['internal_f_name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['nickname'].create()
    post_meta.tables['logs'].columns['file_hash'].drop()
    post_meta.tables['logs'].columns['internal_f_name'].drop()
