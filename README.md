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

## Purpose

This repo demonstrates:

- Cloud‑native automation  
- Serverless architecture  
- Integration between Azure Functions and FastAPI  
- Clean separation of concerns  
- Professional multi‑repo design
