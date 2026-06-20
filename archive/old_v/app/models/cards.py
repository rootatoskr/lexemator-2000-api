from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class WordCard(Base):
    __tablename__ = 'word_cards'
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    word: Mapped[str] = mapped_column(String(100), index=True)
    source_lang: Mapped[str] = mapped_column(String(50))
    target_lang: Mapped[str] = mapped_column(String(50))
    card_text: Mapped[str] = mapped_column(Text)
