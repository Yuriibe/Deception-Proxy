import asyncpg
from typing import Dict, Any

DB_CONFIG = {
    "host": "localhost",  # Use container name if in Docker
    "port": "5432",
    "database": "malicious_requests",
    "user": "proxy_admin",
    "password": "Zt8#5xPqT$kN!3dY"
}

class RequestRepository:
    async def get_request_by_id(self, request_id: int):
        conn = await asyncpg.connect(**DB_CONFIG)
        result = await conn.fetch("SELECT * FROM request_header WHERE attacker_id = $1", request_id)
        await conn.close()
        return [dict(row) for row in result] if result else []


    async def write_to_table(self, table_name: str, data: Dict[str, Any]) -> bool:
        if not data:
            raise ValueError("Data dictionary cannot be empty")

        columns = ', '.join(data.keys())  # Convert dict keys to column names
        placeholders = ', '.join(f'${i + 1}' for i in range(len(data)))  # Create $1, $2, ... placeholders
        values = list(data.values())  # Convert dict values to a list for parameterized query

        print(f"📝 SQL INSERT: INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        print(f"🔍 Values: {values}")  # Debugging print
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        async with asyncpg.create_pool(**DB_CONFIG) as pool:
            async with pool.acquire() as conn:
                async with conn.transaction():
                    try:
                        await conn.execute(query, *values)
                        print(f"✅ Data inserted into {table_name}: {data}")
                    except Exception as e:
                        print(f"❌ SQL Error: {e}")
                        raise ValueError(f"SQL error: {e}")

        return True
