# DataCody API Reference

## Authentication
- Use JWT Bearer token in Authorization header.

## Endpoints
- POST /v1/compile: Compile data task
  - Body: { "task": "your natural language task" }
- POST /v1/auth/login: Login to get token
  - Body: { "email": "user@example.com", "password": "pass" }
- POST /v1/billing/checkout: Upgrade tier
- GET /v1/billing/invoice: Get monthly invoice PDF
