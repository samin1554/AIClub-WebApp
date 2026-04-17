from datetime import datetime, timezone
from math import ceil
from typing import Any


def success_response(data: Any, meta: dict | None = None) -> dict:
    result: dict[str, Any] = {"data": data}
    result["meta"] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **(meta or {}),
    }
    return result


def paginated_response(items: list[Any], total: int, page: int, limit: int) -> dict:
    total_pages = ceil(total / limit) if limit > 0 else 0
    return success_response(
        data=items,
        meta={
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "totalPages": total_pages,
                "hasNext": page < total_pages,
                "hasPrev": page > 1,
            }
        },
    )
