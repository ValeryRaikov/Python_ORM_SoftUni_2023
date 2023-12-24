from django.db import models
from sqlalchemy import Column, Integer, String, Text, Float, CheckConstraint, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from musicApp.settings import Base


# Create your models here.
class Album(Base):
    __tablename__ = 'albums'

    id = Column(
        Integer,
        primary_key=True,
    )

    album_name = Column(
        String(30),
        unique=True,
        nullable=False,
    )

    image_url = Column(
        Text,
        nullable=False,
    )

    price = Column(
        Float,
        nullable=False,
        info={'check_constraint': 'price > 0'},
    )

    songs = relationship(
        'Song',
        back_populates='album',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )


class Song(Base):
    __tablename__ = 'songs'

    id = Column(
        Integer,
        primary_key=True,
    )

    song_name = Column(
        String(30),
        unique=True,
        nullable=False,
    )

    album_id = Column(
        Integer,
        ForeignKey('albums.id'),
        nullable=False,
    )

    album = relationship(
        'Album',
        back_populates='songs',
    )

    music_file = Column(
        LargeBinary,
        unique=True,
        nullable=False,
    )
