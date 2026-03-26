from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import sqlite3
from app.models import User, UserCreate, UserUpdate
from app.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("", response_model=List[User])
async def list_users(
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("id"),
    order: Optional[str] = Query("asc")
):
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM users WHERE 1=1"
        params = []
        
        if search:
            query += " AND (name LIKE ? OR email LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])
        
        valid_sorts = ["id", "name", "email", "age", "created_at"]
        sort_col = sort if sort in valid_sorts else "id"
        order_dir = "DESC" if order.lower() == "desc" else "ASC"
        query += f" ORDER BY {sort_col} {order_dir}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="User not found")
        
        return dict(row)

@router.post("", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (user.name, user.email, user.age)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row)
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already exists")

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        updates = []
        params = []
        
        if user.name is not None:
            updates.append("name = ?")
            params.append(user.name)
        if user.email is not None:
            updates.append("email = ?")
            params.append(user.email)
        if user.age is not None:
            updates.append("age = ?")
            params.append(user.age)
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        
        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="User not found")
        
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
