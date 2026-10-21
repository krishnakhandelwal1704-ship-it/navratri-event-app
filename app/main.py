import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.database import Base, engine, SessionLocal
from app.models import User, Pass, RoleEnum, GenderEnum
from app.auth import get_password_hash
from app.routers import auth_router, passes_router, bookings_router, admin_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NAVRATRI 2026 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include All Routers
app.include_router(auth_router.router)
app.include_router(passes_router.router)
app.include_router(bookings_router.router)
app.include_router(admin_router.router)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

@app.on_event("startup")
def startup_db():
    db = SessionLocal()
    # Create Seed Admin if not exists
    if not db.query(User).filter(User.email == "admin@navratri.com").first():
        admin = User(
            name="Navratri Admin",
            email="admin@navratri.com",
            phone="9999999999",
            gender=GenderEnum.MALE,
            password_hash=get_password_hash("admin123"),
            role=RoleEnum.ADMIN
        )
        db.add(admin)

    # Seed 4 Passes if database is empty for passes
    if db.query(Pass).count() == 0:
        sample_passes = [
            Pass(
                title="VIP Garba Pass 2026",
                price=1500.0,
                date="15 Oct 2026",
                venue="Grand Garba Ground, Mumbai",
                total_quantity=500,
                remaining_quantity=490
            ),
            Pass(
                title="Gold Couple Dandiya Night",
                price=2200.0,
                date="16 Oct 2026",
                venue="Royal Heritage Lawn, Mumbai",
                total_quantity=300,
                remaining_quantity=280
            ),
            Pass(
                title="Student Special Garba Pass",
                price=799.0,
                date="17 Oct 2026",
                venue="Navratri Celebration Arena, Mumbai",
                total_quantity=400,
                remaining_quantity=350
            ),
            Pass(
                title="Family Festive Season Pass (4 Nights)",
                price=4999.0,
                date="15-18 Oct 2026",
                venue="Mega Garba Stadium, Mumbai",
                total_quantity=150,
                remaining_quantity=120
            )
        ]
        db.add_all(sample_passes)
        db.commit()
    db.close()

@app.get("/health")
def health_check():
    return {"status": "ok", "app": "NAVRATRI 2026 API"}