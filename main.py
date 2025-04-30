from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/questions/")
def create_question(question: schemas.QuestionBase, db: Session = Depends(get_db)):
    db_question = models.Question(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choice(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id
        )
        db.add(db_choice)
    db.commit()
    return {"message": "Question created successfully"}

@app.get("/questions/")
def read_all_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    result = []
    for question in questions:
        choices = db.query(models.Choice).filter(models.Choice.question_id == question.id).all()
        result.append({
            "id": question.id,
            "title": question.question_text,
            "choices": [
                {"text": choice.choice_text, "is_correct": choice.is_correct}
                for choice in choices
            ]
        })
    return result
