import asyncio
import json
from os import environ

from databases import Database
import tornado.web

from sqlalchemy import select




class MainHandler(tornado.web.RequestHandler):
    async def get(self):
        database = Database(f'postgresql+asyncpg://{environ.get("DBUSER")}:{environ.get("DBPASSWD")}@{environ.get("DBHOST")}/{environ.get("DBNAME")}?charset=utf8')

        await database.connect()
        test_db_instance = await database.fetch_all('SELECT * FROM test')
        await database.disconnect()

        response_json = list()

        for value in test_db_instance:
            response_json.append(
                {
                    'id': value.field1,
                    'text': value.filed2,
                }
            )

        self.set_header("Content-Type", 'application/json')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(response_json))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8000)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())