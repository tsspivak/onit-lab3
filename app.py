import os
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
)
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class CatBreed(Base):
    __tablename__ = "cat_breeds"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    origin = Column(String(100))
    lifespan = Column(String(50))
    weight = Column(Float)
    coat = Column(String(100))
    temperament = Column(String(200))
    description = Column(Text)

def create_app():
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.route("/", methods=["GET", "POST"])
    def index():
        session = SessionLocal()
        if request.method == "POST":
            breed_id = request.form.get("id")
            if breed_id:
                breed = session.get(CatBreed, int(breed_id))
                if breed:
                    breed.name = request.form["name"]
                    breed.origin = request.form.get("origin")
                    breed.lifespan = request.form.get("lifespan")
                    breed.weight = float(request.form["weight"]) if request.form.get("weight") else None
                    breed.coat = request.form.get("coat")
                    breed.temperament = request.form.get("temperament")
                    breed.description = request.form.get("description")
                    session.commit()
            else:
                breed = CatBreed(
                    name=request.form["name"],
                    origin=request.form.get("origin"),
                    lifespan=request.form.get("lifespan"),
                    weight=float(request.form["weight"]) if request.form.get("weight") else None,
                    coat=request.form.get("coat"),
                    temperament=request.form.get("temperament"),
                    description=request.form.get("description"),
                )
                session.add(breed)
                session.commit()
            return redirect("/")
        breeds = session.query(CatBreed).all()
        session.close()
        return render_template("index.html", breeds=breeds)

    @app.route("/delete/<int:id>")
    def delete(id):
        session = SessionLocal()
        b = session.get(CatBreed, id)
        if b:
            session.delete(b)
            session.commit()
        session.close()
        return redirect("/")

    Base.metadata.create_all(engine)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)
