import logging
from fastapi import FastAPI
from app.models.user import User
from app.logger import setup_logging
from app.database import engine, Base, SessionLocal
from app.routers.user_router import router as user_router

setup_logging()
logger = logging.getLogger("main")

app = FastAPI(title="FastAPI and Oracle (SQLAlchemy) Example")

app.include_router(user_router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        count = db.query(User).count()
        if count == 0:
            logger.info("Initialize some values into USER table")
            initial = [
                User(id=1, name="Alice Johnson", age=28, gender="Female", phone="+91-9000000001", email="alice@example.com", city="Bengaluru", country="India"),
                User(id=2, name="Bob Kumar", age=35, gender="Male", phone="+91-9000000002", email="bob@example.com", city="Chennai", country="India"),
                User(id=3, name="Cathy Lee", age=22, gender="Female", phone="+91-9000000003", email="cathy@example.com", city="Mumbai", country="India"),
                User(id=4, name="Daniel Smith", age=41, gender="Male", phone="+91-9000000004", email="daniel@example.com", city="Delhi", country="India"),
                User(id=5, name="Eva Green", age=30, gender="Female", phone="+91-9000000005", email="eva@example.com", city="Hyderabad", country="India"),
            ]
            db.add_all(initial)
            db.commit()
    finally:
        db.close()
