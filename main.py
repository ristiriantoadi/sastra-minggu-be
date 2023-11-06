from os import getenv

import uvicorn

if __name__ == "__main__":
    port = int(getenv("PORT", 8000))
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
