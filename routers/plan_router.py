from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db  
from models.plan import Plan
from schemas.plan_schema import PlanCreate, PlanResponse, PlanUpdate
from models.user import User
from dependencies import  require_admin
from dependencies.auth import get_current_user

router = APIRouter(
    prefix="/plans",
    tags=["Plans"]
)


# Create a plan (Admin only)
@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(plan: PlanCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    db_plan = Plan(
        name=plan.name,
        price=plan.price,
        billing_cycle=plan.billing_cycle,
        stripe_price_id=plan.stripe_price_id,
        description=plan.description
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


# Get all plans
@router.get("/", response_model=List[PlanResponse])
def get_plans(db: Session = Depends(get_db)):
    plans = db.query(Plan).all()
    return plans


#Update The Plan
@router.put("/{plan_id}")
def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    plan = db.query(Plan).filter(Plan.id == plan_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.name = plan_data.name
    plan.price = plan_data.price
    plan.billing_cycle = plan_data.billing_cycle

    db.commit()
    db.refresh(plan)

    return plan


# Get plan by ID
@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


# Delete plan by ID (Admin only)
@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(plan)
    db.commit()
    return