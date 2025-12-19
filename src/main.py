from fastapi import FastAPI

app=FastAPI(
    title="FastAPI tutorial",
    debug=True,
    description="Learning how to build backend systems using FastAPI",
    version="0.1.0",
    license_info={
        "license":"GPL v3"
    },
    contact={
        "name":"Priyatam",
        "email":"spriyatam28.work@gmail.com",
        "twitter":"https://x.com/vnp268"
    }
)

@app.get("/")
async def root():
    return "Hello, World!!!"