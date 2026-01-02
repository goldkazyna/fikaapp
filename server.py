from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes.pages import router as pages_router
from routes.orders import router as orders_router

app = FastAPI(title="FIKA")

# Статика
app.mount("/static", StaticFiles(directory="static"), name="static")

# Роуты
app.include_router(pages_router)
app.include_router(orders_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)