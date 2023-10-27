#!/usr/bin/env python

# builtin imports
import json
import datetime

# pip imports
from sqlalchemy import MetaData, Table, Column, ForeignKey, Boolean, Float, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy.sql import func

# TODO: asset tags

class Base(DeclarativeBase):
    pass


class Systems(Base):
    __tablename__ = 'system_values'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value_bool: Mapped[bool] = mapped_column(Boolean)
    value_data: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    value_int: Mapped[int] = mapped_column(Integer)
    value_string: Mapped[str] = mapped_column(String)
    value_float: Mapped[float] = mapped_column(Float)


class Roles(Base):
    """
    The class that defines the Roles table

    Args:
        id: The column that holds an auto-incremented ID value
        name: The column that holds the name of the role
        created: The column that holds a datetime of when this role was first created
    """
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'id': self.id,
                     'name': self.name,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)


class Users(Base):
    """
    The class that defines the Users table

    Args:
        id: The column that holds an auto-incremented ID value
        username: The column that holds the username
        first_name: The column that holds the user's first name
        last_name: The column that holds the user's last name
        password: The column that holds a hash of the user's password
        email_address: The column that holds the user's email address
        role_id: The column that holds a ForeignKey pointing to the role assigned to this user
        created: The column that holds a datetime of when this role was first created
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    last_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    email_address: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'id': self.id,
                     'name': self.username,
                     'first_name': self.first_name,
                     'last_name': self.last_name,
                     'email_address': self.email_address,
                     'role_id': self.role_id,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)


class Assets(Base):
    """
    The class that defines the Assets table

    Args:
        id: The column that holds an auto-incremented ID value
        name: The column that holds this asset's name
        path: The column that holds this asset's storage path
        source_path: The column that holds this asset's original path
        size: The column that holds the size of the submitted asset file
        hash: The column that holds a hash of the asset file
        thumbnail: The column that holds this asset's thumbnail storage path
        catalog: The column that holds a ForeignKey pointing to the catalog to which this asset belongs
        created_by: The column that holds a ForeignKey pointing to the user who created this asset
        created: The column that holds a datetime of when this role was first created
    """
    __tablename__ = 'assets'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    version: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
    path: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    source_path: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    size: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    hash: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    thumbnail: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    catalog = Column(Integer, ForeignKey('catalogs.id'), nullable=False)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'id': self.id,
                     'name': self.name,
                     'version': self.version,
                     'path': self.path,
                     'source_path': self.source_path,
                     'size': self.size,
                     'hash': self.hash,
                     'thumbnail': self.thumbnail,
                     'catalog': self.catalog,
                     'created_by': self.created_by,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)

class AccessRecords(Base):
    __tablename__ = 'access_record'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset = Column(Integer, ForeignKey('assets.id'), nullable=False)
    accessed_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'asset_name': self.asset.name,
                     'accessed_by': self.accessed_by.name,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)

class Catalogs(Base):
    __tablename__ = 'catalogs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    config: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'id': self.id,
                     'name': self.name,
                     'config': self.config,
                     'created_by': self.created_by,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)

class BeanLog(Base):
    __tablename__ = 'bean_log'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    level: Mapped[int] = mapped_column(String, unique=False, nullable=True)
    app_name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    user: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    hostname: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    ipaddress: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    platform: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    message: Mapped[str] = mapped_column(String, unique=False, nullable=True)
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        json_dict = {'id': self.id,
                     'user': self.user,
                     'level': self.level,
                     'app_name': self.app_name,
                     'hostname': self.hostname,
                     'ipaddress': self.ipaddress,
                     'platform': self.platform,
                     'message': self.message,
                     'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")}
        return json.dumps(json_dict, indent=4)
