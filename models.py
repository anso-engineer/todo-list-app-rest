from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

from app import db


class Spaces(db.Model):
    __tablename__ = 'Spaces'

    ID = mapped_column(Integer, primary_key=True)
    Name = mapped_column(Text)

    Contexts: Mapped[List['Contexts']] = relationship('Contexts', uselist=True, back_populates='Spaces_')

    def to_dict(self) -> dict:
        return {
            "id": self.ID,
            "name": self.Name
        }

class Tasks(db.Model):
    __tablename__ = 'Tasks'

    ID = mapped_column(Integer, primary_key=True)
    Name = mapped_column(Text)
    Description = mapped_column(Text)
    PostponedStatus = mapped_column(Integer)
    Priority = mapped_column(Text)
    Complexity = mapped_column(Text)
    CreationDate = mapped_column(Text)
    CompletionDate = mapped_column(Text)
    Completed = mapped_column(Integer)
    IsTemplate = mapped_column(Integer)
    Repeated = mapped_column(Integer)

    Contexts: Mapped[List['Contexts']] = relationship('Contexts', uselist=True, back_populates='Tasks_')

    def to_dict(self) -> dict:
        return {
            "id": self.ID,
            "name": self.Name,
            "description": self.Description,
            "PostponedStatus": self.PostponedStatus,
            "Priority": self.Priority,
            "Complexity": self.Complexity,
            "CreationDate": self.CreationDate,
            "Completed": self.Completed,
            "IsTemplate": self.IsTemplate,
            "Repeated": self.Repeated
        }


class Contexts(db.Model):
    __tablename__ = 'Contexts'

    ID = mapped_column(Integer, primary_key=True)
    TaskID = mapped_column(ForeignKey('Tasks.ID'))
    SpaceID = mapped_column(ForeignKey('Spaces.ID'))
    ActualDate = mapped_column(Text)

    Spaces_: Mapped[Optional['Spaces']] = relationship('Spaces', back_populates='Contexts')
    Tasks_: Mapped[Optional['Tasks']] = relationship('Tasks', back_populates='Contexts')

    def to_dict(self) -> dict:
        return {
            "id": self.ID,
            "task_id": self.TaskID,
            "space_id": self.SpaceID,
            "actual_date": self.ActualDate,
        }
