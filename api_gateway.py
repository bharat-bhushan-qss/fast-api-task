from fastapi import FastAPI, Request, HTTPException, Response
import httpx

app = FastAPI()

# Define the backend services
SERVICES = {
    "v1": "http://localhost:8000",
    "v2": "http://localhost:8001"
}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response

@app.api_route("/{proxy_path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH", "TRACE"])
async def proxy(proxy_path: str, request: Request):
    # Extract the service name from the path
    service_name, *path_parts = proxy_path.split('/')
    path = '/'.join(path_parts)

    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    backend_url = f"{SERVICES[service_name]}/{path}"

    # Forward the request to the appropriate backend service
    async with httpx.AsyncClient() as client:
        try:
            # Read the request body
            content = await request.body()
            # Forwardable headers
            headers = {k: v for k, v in request.headers.items() if k.lower() != 'host'}
            headers['Content-Length'] = str(len(content))

            response = await client.request(
                method=request.method,
                url=backend_url,
                headers=headers,
                content=content,
            )
            # Create a new Response object to return to the client
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error connecting to {backend_url}") from exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
