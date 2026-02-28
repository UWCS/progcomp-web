import sqlalchemy as sa

from progcomp.models.utils import auto_str

from ..database import Base


@auto_str
class LoginSession(Base):
    __tablename__ = "login_sessions"

    id = sa.Column(sa.String, primary_key=True)
    username = sa.Column(sa.String)
    passwd = sa.Column(sa.String)
    pc_name = sa.Column(sa.String)
