from typing import List

from sqlalchemy.types import Date, Integer, String, Boolean as Bool
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
from sqlalchemy import Identity, ForeignKey, Table, Column, PrimaryKeyConstraint, orm
from sqlalchemy.orm import relationship, Mapped, mapped_column
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

Base = declarative_base()


sessions_questions = Table(
    "sessions_questions_association",
    Base.metadata,
    Column("session_id", ForeignKey("session.session_id"), primary_key=True),
    Column("question_id", ForeignKey("question.question_id"), primary_key=True),
)


question_tags = Table(
    "question_tags_association",
    Base.metadata,
    Column("tag", ForeignKey("tag.tag_name"), primary_key=True),
    Column("question_id", ForeignKey("question.question_id"), primary_key=True),
)
#  UNNECESSARY - IT'S FOR MANY-MANY
# provider_models = Table(
#     "provider_models_association",
#     Base.metadata,
#     Column("provider_id", ForeignKey("ai_provider.provider_id"), primary_key=True),
#     Column("model_id", ForeignKey("ai_model.model_id"), primary_key=True),
# )

question_prompts = Table(
    "question_prompts_association",
    Base.metadata,
    Column("prompt_id", ForeignKey("prompt.prompt_id"), primary_key=True),
    Column("question_id", ForeignKey("question.question_id"), primary_key=True),
)


trash_questions = Table(
    "trash_questions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", onupdate="CASCADE",
                               ondelete="CASCADE"), primary_key=True),
    Column("question_id", ForeignKey("question.question_id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
)


question_sources = Table(
    "question_sources",
    Base.metadata,
    Column("source", ForeignKey("source.source_id"), primary_key=True),
    Column("question_id", ForeignKey("question.question_id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tag"
    tag_name = sa.Column(
        sa.String(60), nullable=False, unique=True, primary_key=True
    )
    created_by = sa.Column(Integer, ForeignKey("users.id"), nullable=True)

    questions = relationship(
        "Question", secondary=question_tags, back_populates="tags"
    )


class Prompt(Base):
    __tablename__= "prompt"
    prompt_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    created_by = sa.Column(Integer, ForeignKey("users.id"), nullable=False)
    prompt_text = sa.Column(
        sa.String(1500), primary_key=False, unique=False, nullable=False
    )


class AiModel(Base):
    __tablename__= "ai_model"
    model_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    model_name = sa.Column(
        sa.String(50), primary_key=False, unique=True, nullable=False
    )

    ai_provider: Mapped[List["AiProvider"]] = relationship(back_populates="ai_models",
                               cascade="all, delete")


class AiProvider(Base):
    __tablename__= "ai_provider"
    provider_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    provider_name = sa.Column(  
        sa.String(50), primary_key=False, unique=True, nullable=False
    )

    # api_key = sa.Column(
    #     sa.String(350), primary_key=False, unique=False, nullable=True
    # )                
    # project_id = sa.Column(
    #     sa.String(350), primary_key=False, unique=False, nullable=True
    # )  
    
    ai_models: Mapped[AiModel | None] = relationship(back_populates="ai_provider",
                             cascade="all, delete")
    
#  EVENTUALLY ADD THESE: 
#       "type": "service_account",
#   "project_id": "xxx",
#   "private_key_id": "xxx6",
#   "private_key": "-----BEGIN PRIVATE KEY-----xxxn-----END PRIVATE KEY-----\n",
#   "client_email": "xxx",
#   "client_id": "xxx",
#   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#   "token_uri": "https://oauth2.googleapis.com/token",
#   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/xxx.iam.gserviceaccount.com",
#   "universe_domain": "googleapis.com"

# favorate_links = Table(
#     'favorate_links',
#     Base.metadata,
#     Column('id', ForeignKey("users.id"), primary_key=True),
#     Column('favorate_id',ForeignKey("users.id"), primary_key=True),
# )
chained_question = Table(
    'chained_question', 
    Base.metadata,
    Column('question_id', ForeignKey("question.question_id"), primary_key=True),
    Column('chained_question_id',ForeignKey("question.question_id"), primary_key=True),
)   


class Question(Base):
    __tablename__ = "question"
    question_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    created_on = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    additional_text = sa.Column(
        sa.String(1500), primary_key=False, unique=False, nullable=True
    )
    gpt_answer = sa.Column(sa.String(4000), primary_key=False, unique=False, nullable=False)
    google_answer = sa.Column(sa.String(4000), primary_key=False, unique=False, nullable=False)
    created_by = sa.Column(Integer, ForeignKey("users.id"), nullable=False)

    prompts = relationship(
        "Prompt", secondary=question_prompts)

    tags = relationship(
        "Tag", secondary=question_tags, back_populates="questions"
    )

    sources = relationship(
        "Source", secondary=question_sources, back_populates="sources_questions"
    )

    pics = relationship("Pic", back_populates="question", cascade="all, delete")
    
    chained_questions = relationship(
        'Question',
        secondary=chained_question,
        primaryjoin=(chained_question.c.question_id == question_id),
        secondaryjoin=(chained_question.c.chained_question_id == question_id),
       # lazy='dynamic'
    )
    # favorates = relationship(
    #     'users',
    #     secondary=favorate_links,
    #     primaryjoin=(favorate_links.c.id == id),
    #     secondaryjoin=(favorate_links.c.favorate_id == id),
    #    # lazy='dynamic'
    # )

    # 2.0 many to one relationship mapping (one side)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("session.session_id"))
    session: Mapped["Session"] = relationship("Session",
                                               back_populates="questions")

    # maybe the right way:
    # session_id: Mapped[int] = mapped_column(
    #     ForeignKey("session.session_id"))
    # session: Mapped["Session"] = relationship(back_populates="questions")


class Session(Base):
    __tablename__ = "session"
    session_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    session_name = Column(sa.String(155))

    #     Maybe the right way:
    # questions: Mapped[List["Question"]] = relationship(
    #     back_populates="session")

    questions: Mapped[List["Question"]] = relationship("Question",
        back_populates="session")



class Source(Base):
    __tablename__ = "source"
    source_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    url_string = Column(sa.String(400), nullable=False, unique=True, primary_key=False)
    shortcut = sa.Column(
        sa.String(60), nullable=True, unique=False, primary_key=False
    )
    sources_questions = relationship(
        "Question", secondary=question_sources, back_populates="sources"
    )


class Users(UserMixin, Base):
    __tablename__ = "users" 
    id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    username = sa.Column(sa.String(255), nullable=False)
    last_login = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    email = sa.Column(sa.String(60), unique=True, nullable=False)
    created_on = sa.Column(sa.DateTime, index=False, unique=False, nullable=True)
    password = sa.Column(
        sa.String(200), primary_key=False, unique=False, nullable=False
    )
    role = sa.Column(sa.Integer, index=False, nullable=False, default=1)
    email_verified = sa.Column(sa.Boolean, index=False, nullable=False, default=False)
    token = sa.Column(sa.String(60), nullable=True)
        
    trash_questions = relationship(
        "Question",
        secondary=trash_questions,
        primaryjoin=(trash_questions.c.user_id == id),
        secondaryjoin=(trash_questions.c.question_id == Question.question_id),
        passive_deletes=True,
    )
    selected_gpt_prompt = sa.Column(Integer, ForeignKey("prompt.prompt_id"), nullable=True)
    selected_google_prompt = sa.Column(Integer, ForeignKey("prompt.prompt_id"), nullable=True)
    
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return (f"User(id={self.id!r}, username={self.username!r}, "
                f"pass={self.password}, created on={self.created_on}, email={self.email}, last_login={self.last_login})")
    
    def is_active(self):
        return True
    
    def is_authenticated(self):
        return True
   
         
class Pic(Base):
    __tablename__ = "pic"
    pic_id = sa.Column(
        sa.Integer, Identity(), primary_key=True, autoincrement=True
    )
    pic_string = Column(sa.String(600))
    pic_type = Column(sa.String(25))
    
    question = relationship("Question", back_populates="pics")

    
class Rating(Base):
    __tablename__ = "rating"
    user_id = sa.Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = sa.Column(Integer, ForeignKey("question.question_id", ondelete="CASCADE"), nullable=False)
    rating = sa.Column(sa.Integer, nullable=False)
    
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'question_id'),
        {},
    )


