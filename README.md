# Dockerized Multi-Service Reliability Monitoring System

## Project Overview
A production-ready container orchestration system demonstrating SRE best practices for **self-healing infrastructure**, **observability**, and **automated reliability**. Monitors nginx, redis, Flask app, and self-heals failures.

**Live Demo**: `docker compose up -d` → Watch terminal alerts → `docker stop nginx` → Auto-restart!

## Architecture Diagram
```
┌─────────────────┐    ┌──────────────────┐
│   docker-compose │    │   Bridge Network │
│     orchestrate  │────│ reliability-net  │
└─────────────────┘    └──────────────────┘
         │                       │
         ├── nginx ─── /health   │
         ├── redis ─── ping      │
         └── flask ─── /health   │
                               │
         │                     │
         └── monitor-agent ─── Docker API ─── Checks/Restarts
                            ┌──────────────┐
                            │ logs/*.json  │── Reports
                            │ reports/*.txt│
                            └──────────────┘
```

## Features
- ✅ **Container Health Monitoring** (status + HTTP endpoints)
- ✅ **Auto-Restart Failed Services** (max 3 attempts)
- ✅ **Structured JSON Logging** (timestamps, events, metrics)
- ✅ **Uptime Tracking & Availability %**
- ✅ **Terminal Alerts** (CRITICAL/WARNING)
- ✅ **Reliability Reports** (summary.txt)
- ✅ **Production Logging Module**
- ✅ **Configurable Thresholds** (JSON)

## Tech Stack
- Docker Compose v3.8
- Python 3.12 + Docker SDK
- Flask (demo app)
- nginx:latest, redis:alpine
- JSON structured logging

## Folder Structure
```
docker-reliability-monitor/
├── docker-compose.yml
├── monitor-agent/
│   ├── monitor.py          # Main monitoring loop
│   ├── logger.py           # JSON logger
│   ├── config.json         # Thresholds
│   ├── requirements.txt
│   └── Dockerfile
├── flask-app/
│   ├── app.py             # /health endpoint
│   ├── requirements.txt
│   └── Dockerfile
├── logs/                  # container_events.json
├── reports/               # reliability_summary.txt
└── README.md
```

## Deployment (2 mins)
1. `git clone <repo> && cd docker-reliability-monitor`
2. `docker compose up -d`
3. Watch logs: `docker logs -f monitor-agent`
4. Test failure: `docker stop nginx`
5. Check recovery: `docker ps`, `cat logs/container_events.json`, `cat reports/reliability_summary.txt`

## Sample Alerts
```
[CRITICAL] nginx container stopped at 2024-10-01T10:00:00
Restart attempt 1 successful
[WARNING] flask-app unhealthy response at 2024-10-01T10:01:30
Uptime: nginx 99.8%, redis 100%, flask-app 99.5%
```

## SRE Concepts Demonstrated
- **Self-Healing**: Auto-restart reduces MTTR
- **Observability**: Logs + metrics + alerts
- **SLIs/SLOs**: Uptime %, availability
- **Error Budgets**: Restart limits prevent restart loops
- **Golden Signals**: Latency (health checks), Errors, Saturation

## Resume Value (Freshers)
| Skill Demonstrated | Interview Questions Answered |
|--------------------|-----------------------------|
| Docker SDK/Python | "Build container monitor?" |
| Self-Healing Infra | "Handle production failures?" |
| Observability | "Implement logging/alerts?" |
| SRE Metrics | "Define uptime SLI?" |
| Automation | "Orchestrate multi-service?" |

**Stars this repo! Deploy in 2 mins 🚀**

