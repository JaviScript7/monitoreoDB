import asyncio
import aiomysql
import telegram
from telegram import Bot

# Configuración del bot de Telegram
bot_token = '7235994071:AAHwepFa-FvVmz7Me4j9v4S399j_ERq-3I0'
chat_id = '6045970195'
bot = Bot(token=bot_token)

# Variable para almacenar el último timestamp verificado
last_timestamp = None

async def check_for_changes(pool):
    global last_timestamp
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM equipos ORDER BY updated_at DESC LIMIT 1")
            row = await cursor.fetchone()
            if row:
                current_timestamp = row[-1]  # Suponiendo que el updated_at está en la última columna
                if last_timestamp is None or current_timestamp > last_timestamp:
                    last_timestamp = current_timestamp
                    await send_alert(row)

async def send_alert(row):
    message = f"🚨 Se ha detectado una modificación en la base de datos:🚨\n\n {row}"
    await bot.send_message(chat_id=chat_id, text=message)

async def main():
    pool = await aiomysql.create_pool(
        host='localhost',
        user='root',
        password='P455W0RD',
        db='reparaciones'
    )

    while True:
        await check_for_changes(pool)
        await asyncio.sleep(10)  # Esperar 10 segundos antes de revisar nuevamente

if __name__ == "__main__":
    asyncio.run(main())
