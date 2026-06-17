from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.cards import WordCard
from app.schemas.cards import CardCreate, CardResponse

router = APIRouter(prefix='/cards', tags=['Cards'])


# Ідемпотентний ендпоінт: повертає існуючу картку або створює нову
@router.post('/', response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def create_or_get_card(card_data: CardCreate, db: AsyncSession = Depends(get_db)) -> WordCard:  # noqa: B008
    query = select(WordCard).where(
        WordCard.word == card_data.word,
        WordCard.source_lang == card_data.source_lang,
        WordCard.target_lang == card_data.target_lang,
    )
    result = await db.execute(query)
    existing_card = result.scalar_one_or_none()

    if existing_card:
        return existing_card

    mock_card_text = f'Слово: {card_data.word}. Переклад: test'  # тимчасова заглушка до інтеграції LLM

    new_card = WordCard(
        word=card_data.word,
        source_lang=card_data.source_lang,
        target_lang=card_data.target_lang,
        card_text=mock_card_text,
    )
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return new_card
