## Getting Started

### Pull and run docker image

1.  First authenticate with your github credentials (if you haven't already)

```bash
docker login ghcr.io -u <username>
```

Replace < username > with your GitHub username and enter your personal access token (PAT) that has the read:packages scope.

2.  Pull the image

```bash
docker pull ghcr.io/salahdevp/easylaw-search-api:latest
```

3. Run the container

```bash
docker run -e ELASTIC_PASSWORD=<elastic password> -p 8000:5000 ghcr.io/salahdevp/easylaw-search-api:latest
```

Replace < elastic password > with your elastic search password.
