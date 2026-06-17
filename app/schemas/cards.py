from pydantic import BaseModel, ConfigDict, Field


class CardCreate(BaseModel):
    word: str = Field(..., max_length=100, description='Слово для перекладу')
    source_lang: str = Field('no', max_length=50, description='Вихідна мова')
    target_lang: str = Field('uk', max_length=50, description='Мова перекладу')


class CardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # дозволяє серіалізацію з ORM-об'єктів SQLAlchemy

    id: int
    word: str
    source_lang: str
    target_lang: str
    card_text: str
