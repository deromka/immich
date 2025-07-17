@echo off
cd /d D:\immich


:retry
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker not ready, retrying in 10 seconds...
    timeout /t 10
    goto retry
)

docker compose -f immich.workers.yml --env-file .env up -d --scale immich-microservices=3