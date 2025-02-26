import asyncpg

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
