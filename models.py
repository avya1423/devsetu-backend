import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Table, Enum, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RoleEnum(enum.Enum):
    student = "student"
    mentor = "mentor"
    admin = "admin"

class DifficultyEnum(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class TeamStatusEnum(enum.Enum):
    recruiting = "recruiting"
    building = "building"
    completed = "completed"

class TeamRoleEnum(enum.Enum):
    leader = "leader"
    developer = "developer"

team_members = Table(
    'team_members',
    Base.metadata,
    Column('team_id', UUID(as_uuid=True), ForeignKey('teams.team_id'), primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True),
    Column('team_role', Enum(TeamRoleEnum), default=TeamRoleEnum.developer),
    Column('joined_at', DateTime, default=datetime.utcnow)
)

class User(Base):
    __tablename__ = 'users'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_handle = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.student)
    graduation_year = Column(Integer)
    academic_path = Column(String) 
    primary_skills = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)
    teams = relationship("Team", secondary=team_members, back_populates="members")

class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(Text)
    difficulty = Column(Enum(DifficultyEnum), nullable=False)
    required_stack = Column(ARRAY(String))
    github_template_url = Column(String)
    estimated_hours = Column(Integer)
    teams = relationship("Team", back_populates="project")

class Team(Base):
    __tablename__ = 'teams'
    team_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.project_id'), nullable=False)
    team_name = Column(String, nullable=False)
    status = Column(Enum(TeamStatusEnum), default=TeamStatusEnum.recruiting)
    repo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="teams")
    members = relationship("User", secondary=team_members, back_populates="teams")