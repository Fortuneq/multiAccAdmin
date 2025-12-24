"""
API router for proxy management.
Handles CRUD operations and testing for proxy servers.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import httpx
import asyncio

from app.database import get_db
from app.models import Proxy
from app.schemas import ProxyCreate, ProxyUpdate, ProxyResponse, ProxyTestResult

router = APIRouter(prefix="/api/proxies", tags=["Proxies"])


@router.get("/", response_model=List[ProxyResponse])
async def get_proxies(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Max number of records to return"),
    active_only: bool = Query(False, description="Return only active proxies"),
    db: Session = Depends(get_db)
):
    """
    Get list of all proxies.

    Args:
        skip: Pagination offset
        limit: Maximum number of results
        active_only: Filter for active proxies only
        db: Database session

    Returns:
        List of proxies
    """
    query = db.query(Proxy)

    if active_only:
        query = query.filter(Proxy.is_active == True)

    proxies = query.offset(skip).limit(limit).all()
    return proxies


@router.post("/", response_model=ProxyResponse, status_code=201)
async def create_proxy(
    proxy_data: ProxyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new proxy.

    Args:
        proxy_data: Proxy creation data
        db: Database session

    Returns:
        Created proxy
    """
    new_proxy = Proxy(**proxy_data.model_dump())
    db.add(new_proxy)
    db.commit()
    db.refresh(new_proxy)

    return new_proxy


@router.get("/{proxy_id}", response_model=ProxyResponse)
async def get_proxy(
    proxy_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific proxy by ID.

    Args:
        proxy_id: Proxy ID
        db: Database session

    Returns:
        Proxy details

    Raises:
        HTTPException: If proxy not found
    """
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail=f"Proxy with ID {proxy_id} not found")

    return proxy


@router.put("/{proxy_id}", response_model=ProxyResponse)
async def update_proxy(
    proxy_id: int,
    proxy_data: ProxyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing proxy.

    Args:
        proxy_id: Proxy ID
        proxy_data: Updated proxy data
        db: Database session

    Returns:
        Updated proxy

    Raises:
        HTTPException: If proxy not found
    """
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail=f"Proxy with ID {proxy_id} not found")

    # Update fields
    update_data = proxy_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(proxy, field, value)

    db.commit()
    db.refresh(proxy)

    return proxy


@router.delete("/{proxy_id}", status_code=204)
async def delete_proxy(
    proxy_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a proxy.

    Args:
        proxy_id: Proxy ID
        db: Database session

    Raises:
        HTTPException: If proxy not found or is in use
    """
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail=f"Proxy with ID {proxy_id} not found")

    # Check if proxy is used by any accounts
    if proxy.accounts:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete proxy. It is used by {len(proxy.accounts)} account(s)"
        )

    db.delete(proxy)
    db.commit()

    return None


@router.post("/{proxy_id}/test", response_model=ProxyTestResult)
async def test_proxy(
    proxy_id: int,
    db: Session = Depends(get_db)
):
    """
    Test proxy connection.

    Args:
        proxy_id: Proxy ID
        db: Database session

    Returns:
        Test result with success status and response time

    Raises:
        HTTPException: If proxy not found
    """
    proxy = db.query(Proxy).filter(Proxy.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail=f"Proxy with ID {proxy_id} not found")

    # Test proxy connection
    test_url = "https://httpbin.org/ip"
    start_time = datetime.now()

    try:
        async with httpx.AsyncClient(
            proxies=proxy.full_address,
            timeout=10.0
        ) as client:
            response = await client.get(test_url)
            response.raise_for_status()

        end_time = datetime.now()
        response_time = (end_time - start_time).total_seconds()

        # Update last_tested timestamp
        proxy.last_tested = datetime.now()
        proxy.is_active = True
        db.commit()

        return ProxyTestResult(
            success=True,
            message="Proxy connection successful",
            response_time=response_time,
            tested_at=proxy.last_tested
        )

    except Exception as e:
        # Update status to inactive
        proxy.last_tested = datetime.now()
        proxy.is_active = False
        db.commit()

        return ProxyTestResult(
            success=False,
            message=f"Proxy connection failed: {str(e)}",
            response_time=None,
            tested_at=proxy.last_tested
        )
