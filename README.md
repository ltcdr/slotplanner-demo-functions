# Slotplanner Demo – Azure Functions Automation

This repository contains the serverless automation layer for the **slotplanner-demo** project.  
It uses **Azure Functions (Python)** with a **timer trigger** to perform weekly maintenance tasks:

### Generate next week's demo activities  
Every Friday morning, the function calls the backend endpoint  
`POST /admin/generate_next_week`  
to insert realistic demo activities for the upcoming week.

### Clean up old activities  
The function also calls  
`POST /admin/cleanup_old`  
to remove activities older than two weeks, keeping the demo database small and fresh.

---

## Purpose

This repo demonstrates:

- Cloud‑native automation  
- Serverless architecture  
- Integration between Azure Functions and FastAPI  
- Clean separation of concerns  
- Professional multi‑repo design

---

## System Components & Related Repositories
Slotplanner is structured as a multi‑repository system to reflect real‑world release and delivery workflows.
This repository (slotplanner-demo-functions) provides the serverless automation layer, while additional components are maintained separately:

[slotplanner-demo](https://github.com/ltcdr/slotplanner-demo)  
FastAPI backend and demo frontend providing the activity and booking workflow.
The automation functions in this repo call its administrative endpoints.

[slotplanner-meta](https://github.com/ltcdr/slotplanner-demo-meta)  
The orchestration repository coordinating cross‑service releases, unified versioning, environment configuration, and deployment sequencing.
It ensures consistent deployment order between the backend and this function app.

Together, these repositories illustrate a distributed architecture with independent deployment units and coordinated release processes — a core aspect of Slotplanner’s engineering and delivery design.

---


## Architecture Overview
	
```
Azure Function (Timer Trigger)
↓
FastAPI Backend (slotplanner-demo)
↓
SQLite Demo Database
```


The backend contains all business logic.  
This repo contains only the automation trigger and cloud integration.

---

## Timer Schedule

The function runs every Friday at **06:00 UTC**:

	0 0 6 * * FRI


---

## Environment Strategy

The function app supports multiple environments:

- **Local development** using the Azure Functions Core Tools
- **Staging** for validating weekly automation behavior
- **Production** for live demo data generation

Environment configuration (backend URL, secrets, identity) is managed through
Azure App Service settings and coordinated via the meta repository.


---

## Files

- `GenerateNextWeek/function.json` – Timer trigger definition  
- `GenerateNextWeek/__init__.py` – Python code calling the backend  
- `requirements.txt` – Python dependencies  
- `host.json` – Azure Functions host configuration  
- `.gitignore` – Ignore build artifacts and local settings  

---

## Related Repository

Backend + frontend demo:  
https://github.com/ltcdr/slotplanner-demo

---

## Deployment

This function can be deployed using:

- Azure Portal  
- Azure CLI  
- GitHub Actions (recommended)

A GitHub Actions workflow will be added later.

---

## Release & Deployment Coordination

This function app is part of a multi‑repo architecture and is released
independently from the main slotplanner-demo backend. The release workflow
follows a coordinated sequence:

1. Backend deployment (slotplanner-demo)
2. Function app deployment (slotplanner-demo-functions)

This ensures API compatibility for the automation endpoints
(`/admin/generate_next_week`, `/admin/cleanup_old`).

The CI/CD pipeline uses GitHub Actions with OIDC authentication and supports
staging and production environments via Azure Function App slots. Versioning
is aligned with the meta repository that orchestrates cross‑service releases.

---

## Operational Reliability

The automation functions include basic operational safeguards:

- HTTP timeout and error handling when calling the backend
- Logging of each weekly run for auditability
- Idempotent backend endpoints to prevent duplicate activity creation
- Isolation of demo data from production systems

These patterns reflect production‑grade reliability even in a demo context.
