import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable, default to 3003
    port = int(os.getenv("PORT", 3003))
    
    # Get host from environment variable, default to 0.0.0.0
    host = os.getenv("HOST", "localhost")
    
    # Get reload setting from environment variable, default to True for development
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload
    )
