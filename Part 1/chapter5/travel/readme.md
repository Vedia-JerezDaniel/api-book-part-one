✈️ WanderData API — Travel Intelligence Platform

markdown
# ✈️ WanderData API — Travel Intelligence Platform

Travel intelligence platform that transforms raw travel data into actionable insights. Built with FastAPI and PostgreSQL, designed for scalability and analytical depth.

---

## 📋 Table of Contents
- [Core Data Model](#-core-data-model)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [API Endpoints](#-api-endpoints)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Core Data Model
┌────────┐  ┌──────────────┐ ┌─────────────┐
 Flights      ****──▶ Prices ◀──── Bookings 
└─────────────┘  └──────────────┘ └─────────────┘
 
▼ ▼ ▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐
 Inventory  Aircraft  Customers 
└─────────────┘ └──────────────┘ └─────────────┘

▼
┌─────────────┐ ┌──────────────┐ ┌─────────────┐
 Events ────▶ Hotels ────▶Hotel Prices 
└─────────────┘ └──────────────┘ └─────────────┘

text

---

## 🔥 Key Features

### ✈️ Flight Analytics
- Routes for 8 destinations ranking with window functions
- Load factor analysis and occupancy rates
- Aircraft utilization metrics
- Payments and revenue breakdowns
- Brief insights of cultural events 

### 🏨 Hotel Intelligence
- Dynamic pricing based on occupancy
- Inventory management with allotment tracking
- Revenue optimization recommendations

### 📅 Event Integration
- Cultural and festival impact analysis

### 👥 Customer Insights
- Customer Lifetime Value (CLV) calculation
- Booking behavior patterns and preferences

### 📦 Inventory Management
- Allotment release period optimization

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **API Framework** | FastAPI | High-performance async endpoints |
| **Database** | PostgreSQL 15 | Primary data store with PostGIS |
| **ORM** | Database abstraction + raw SQL |
| **Data Processing** | Pandas | Analytics and transformations |
| **Visualization** | Streamlit | Tableau dashboards |
| **Testing** | Pytest |
| **Documentation** | Swagger/ReDoc | Auto-generated API docs |

---

## 📁 Project Structure

wanderdata-api/
  + app/
      + init.py
      + main.py # FastAPI application entry point
  + api/ # API endpoints by version
    + init.py
      + v0/ # Initial version
        + flights.py
        + hotels.py
        + bookings.py
        + customers.py
        + analytics.py
      + core/ # Core configuration
        + config.py # Settings, environment
        + database.py # DB connection engine
        + security.py # Auth, CORS
        + logging.py # Logging configuration
      + models/ # SQLAlchemy ORM models
        + flight.py
        + hotel.py
        + booking.py
        + customer.py
        + price.py
        + inventory.py
        + aircraft.py
        + event.py
        + airport.py
      + schemas/ # Pydantic models
        + flight.py
        + hotel.py
        + booking.py
        + customer.py
        + response.py # Standard response wrappers
      + crud/ # Database operations
        + base.py # Base CRUD class
        + flight_crud.py
        + hotel_crud.py
        + booking_crud.py
        + analytics_queries.py # Raw SQL for complex analytics
      + tests/ # Test suite
        + conftest.py
        + test_api/
        + test_models/
        + test_queries/
    + docs/ # Additional documentation
      + openapi_collection.json
      + .env.example # Environment variables template
      + .gitignore
      + requirements.txt # Python dependencies
      + pyproject.toml # Project configuration
      + README.md # This file
---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Git

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/wanderdata-api.git
cd wanderdata-api

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Manually create database:
createdb wanderdata
psql -d wanderdata -c "CREATE SCHEMA travel;"

# 5. Start API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Verify Installation
bash
# Health check
curl http://localhost:8000/health

# Should return:
{"status":"ok","version":"0.1.0"}
🔧 Environment Variables
Create a .env file in the root directory:


📚 Documentation
Access the auto-generated API documentation:

  * Swagger UI: http://localhost:8000/docs
  * ReDoc: http://localhost:8000/redoc
  * OpenAPI JSON: http://localhost:8000/openapi.json

Postman Collection
  * Import the Postman collection from:
   /docs/postman_collection.json for ready-to-use API requests.

🤝 Contributing
We welcome contributions! Please follow these steps:

📄 License
MIT License

Copyright (c) 2026 WanderData

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

🙏 Acknowledgments
FastAPI team for the amazing framework
PostgreSQL community
Coffee ☕, water 💧, and snacks 🍪 for fueling the development process
Built with: Python, FastAPI, PostgreSQL, and a lot of patience!
Version: 0.1.0
Last Updated: March 2026

