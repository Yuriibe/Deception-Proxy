import asyncpg
from typing import Dict, Any

DB_CONFIG = {
    "host": "localhost",
    "database": "malicious_requests",
    "user": "postgres",
    "password": "root"
}


class RequestRepository:
    async def get_request_by_id(self, request_id: int):
        conn = await asyncpg.connect(**DB_CONFIG)
        result = await conn.fetchrow("SELECT * FROM request_header WHERE id = $1", request_id)
        await conn.close()
        return dict(result) if result else None

    async def write_to_table(self, table_name: str, data: Dict[str, Any]) -> bool:
        if not data:
            raise ValueError("Data dictionary cannot be empty")

        columns = ', '.join(data.keys())  # Convert dict keys to column names
        placeholders = ', '.join(f'${i + 1}' for i in range(len(data)))  # Create $1, $2, ... placeholders
        values = list(data.values())  # Convert dict values to a list for parameterized query

        try:
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        except:
            print("Sql error")
            return False
        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    await conn.execute(query, *values)
        return True
