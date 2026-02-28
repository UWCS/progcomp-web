import sqlalchemy as sa

from progcomp.models.utils import auto_str

from ..database import Base


@auto_str
class AdminSession(Base):
    __tablename__ = "admin_sessions"

    id = sa.Column(sa.String, primary_key=True)
    addr = sa.Column(sa.String)
    user_agent = sa.Column(sa.String)
