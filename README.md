# 💳 Credit Approval System

This project provides a Dockerized Django-based backend for managing customer loans, eligibility checks, and credit scoring.

---

## 📁 Prerequisites

- Docker
- Docker Compose
- Excel files: `customer_data.xlsx` and `loan_data.xlsx` (placed in root)

---

## 🔧 Clone the Repository

```bash
git clone https://github.com/yourusername/credit-approval-system.git
cd credit-approval-system
```

## Build and Start All Services
```bash
docker-compose up -d --build
```

## Create a Superuser (Optional)
```bash
docker-compose exec web python manage.py createsuperuser
```

## Ingest Data from Excel
```bash
docker-compose exec web python manage.py ingestion
```

##  Run All Unit Tests
``` bash
docker-compose exec web pytest
```

## Shut Down All Containers
``` bash
docker-compose down
```

## API Endpoints (No Auth Required)
  - POST    /register
  - POST    /check-eligibility
  - POST    /create-loan
  - GET     /view-loan/<loan_id>
  - GET     /view-loans/<customer_id>
