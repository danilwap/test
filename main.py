import uvicorn
from fastapi import FastAPI
from sqlalchemy import text

from database import get_db


async def get_all_hierarchies():
    async with get_db() as db:
        try:
            query = text("SELECT * FROM endpoints")
            result = await db.execute(query)
            result = result.scalars().all()
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"

app = FastAPI(
    title="Trading App"
)

@app.get('/')
async def start_main():
    result = await get_all_hierarchies()
    print(result)
    return 'Работу работаем'


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)