import uuid

from sqlalchemy import Column, DateTime, String, Integer, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import UUID
from DB.connection import Base
from datetime import datetime, timezone

class BorrowStatus:
    ACTIVE   = "active"
    RETURNED = "returned"
    OVERDUE  = "overdue"
    RENEWED  = "renewed"


class Borrow(Base):
    __tablename__ = "borrows"

    # ── Primary key ───────────────────────────────────────────────────────────
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)

    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    book_id = Column(UUID(as_uuid=True), nullable=False, index=True)

    # ── Loan lifecycle ────────────────────────────────────────────────────────
    borrowed_at   = Column(DateTime(timezone=True), nullable=False)
    due_date      = Column(DateTime(timezone=True), nullable=False)
    returned_at   = Column(DateTime(timezone=True), nullable=True)
    status        = Column(String(20), nullable=False, default=BorrowStatus.ACTIVE, index=True)
    renewal_count = Column(Integer,  nullable=False, default=0)

    # ── Fine ──────────────────────────────────────────────────────────────────
    fine_amount = Column(Float,   nullable=False, default=0.0)
    fine_paid   = Column(Boolean, nullable=False, default=False)

    # ── Timestamps ────────────────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))

    @property
    def is_overdue(self) -> bool:
        return (
            self.status == BorrowStatus.ACTIVE
            and datetime.now(timezone.utc) > self.due_date
        )

    def __repr__(self):
        return f"<Borrow id={self.id} user_id={self.user_id} book_id={self.book_id} status={self.status}>"