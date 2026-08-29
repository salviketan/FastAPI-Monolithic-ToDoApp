import re
from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    id: Any

    # Generate __tablename__ automatically in snake_case + pluralized
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Inserts an underscore before any capital letter preceded by a lowercase letter
        snake_name: str = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

        # Simple pluralization (adds 's')
        return f"{snake_name}s"
