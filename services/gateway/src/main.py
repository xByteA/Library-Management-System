import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    host = os.getenv("HOST", "localhost")
    reload = os.getenv("RELOAD", "true").lower() == "true"

    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
    )
