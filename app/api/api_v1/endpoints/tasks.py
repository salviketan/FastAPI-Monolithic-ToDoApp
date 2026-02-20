from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app import crud, schemas
from app.api import deps
