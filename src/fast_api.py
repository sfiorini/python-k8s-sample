from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from decouple import config
from routes.main import router as main_router
from routes.user import router as user_router
from utils.exceptions import CustomException

app = FastAPI()

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message},
    )


# Get environment variables.
DEBUG = config('DEBUG', default=False, cast=bool)
PORT = config('PORT', default=3000, cast=int)
ENVIRONMENT=config('ENVIRONMENT', default='PROD', cast=str).upper()

if (ENVIRONMENT != 'PROD' and ENVIRONMENT != 'TEST' and ENVIRONMENT != 'DEV'):
    ENVIRONMENT='PROD'

ROUTERS = (user_router, main_router,)

for r in ROUTERS:
    app.include_router(r)

if __name__ == '__main__':
    import uvicorn
    
    print('ENVIRONMENT: ',ENVIRONMENT)
    logLevel = 'info' if DEBUG else 'info'
    uvicorn.run("__main__:app", host="0.0.0.0", port=PORT, log_level=logLevel, reload=DEBUG)