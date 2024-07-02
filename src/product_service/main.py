import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'infrastructure.entrypoints.rest_api:fastapi_app',
        reload=True,
    )
