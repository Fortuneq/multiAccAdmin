"""
API router for account management.
Handles CRUD operations for social media accounts.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import Account, Platform
from app.schemas import AccountCreate, AccountUpdate, AccountResponse

router = APIRouter(prefix="/api/accounts", tags=["Accounts"])


@router.get("/", response_model=List[AccountResponse])
async def get_accounts(
    platform: Optional[Platform] = Query(None, description="Filter by platform"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    db: Session = Depends(get_db)
):
    """
    Get list of all accounts with optional filtering.

    Args:
        platform: Filter by platform type (TikTok/Reels/Shorts)
        skip: Pagination offset
        limit: Maximum number of results
        db: Database session

    Returns:
        List of accounts
    """
    query = db.query(Account)

    if platform:
        query = query.filter(Account.platform == platform)

    accounts = query.offset(skip).limit(limit).all()
    return accounts


@router.post("/", response_model=AccountResponse, status_code=201)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new account.

    Args:
        account_data: Account creation data
        db: Database session

    Returns:
        Created account

    Raises:
        HTTPException: If username already exists
    """
    # Check if username already exists
    existing = db.query(Account).filter(Account.username == account_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Username {account_data.username} already exists")

    # Validate proxy_id if provided
    if account_data.proxy_id:
        from app.models import Proxy
        proxy = db.query(Proxy).filter(Proxy.id == account_data.proxy_id).first()
        if not proxy:
            raise HTTPException(status_code=404, detail=f"Proxy with ID {account_data.proxy_id} not found")

    # Create new account
    new_account = Account(**account_data.model_dump())
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific account by ID.

    Args:
        account_id: Account ID
        db: Database session

    Returns:
        Account details

    Raises:
        HTTPException: If account not found
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found")

    return account


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing account.

    Args:
        account_id: Account ID
        account_data: Updated account data
        db: Database session

    Returns:
        Updated account

    Raises:
        HTTPException: If account not found
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found")

    # Update fields
    update_data = account_data.model_dump(exclude_unset=True)

    # Check username uniqueness if updating username
    if "username" in update_data:
        existing = db.query(Account).filter(
            Account.username == update_data["username"],
            Account.id != account_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail=f"Username {update_data['username']} already exists")

    # Validate proxy_id if updating
    if "proxy_id" in update_data and update_data["proxy_id"]:
        from app.models import Proxy
        proxy = db.query(Proxy).filter(Proxy.id == update_data["proxy_id"]).first()
        if not proxy:
            raise HTTPException(status_code=404, detail=f"Proxy with ID {update_data['proxy_id']} not found")

    for field, value in update_data.items():
        setattr(account, field, value)

    db.commit()
    db.refresh(account)

    return account


@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an account.

    Args:
        account_id: Account ID
        db: Database session

    Raises:
        HTTPException: If account not found
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail=f"Account with ID {account_id} not found")

    db.delete(account)
    db.commit()

    return None
