# WealthWise Portfolio Tracker

A backend API service for tracking investment portfolios, managing stock/mutual fund transactions, and calculating returns. Built as part of a technical assessment demonstrating clean architecture and best practices.

## Features

### Core Functionality
- User management with email-based identification
- Transaction recording (BUY/SELL) with validation
- Portfolio summary with weighted average cost calculation
- Real-time P&L computation based on current market prices
- Transaction history with filtering options

### Bonus Features (All Implemented)
- **JWT Authentication**: Secure user registration and login with token-based auth
- **Redis Caching**: Portfolio summaries cached for 5 minutes, auto-invalidated on updates
- **Background Jobs**: Automated price updates every 1 minute simulating market fluctuations

### Technical Highlights
- Clean layered architecture (Repository → Service → Router)
- Raw SQL with parameterized queries 
- Comprehensive error handling and validation
- Decimal precision for financial calculations
- Connection pooling for database efficiency

## Tech Stack

- **Backend**: Python 3.13, FastAPI
- **Database**: PostgreSQL 14
- **Caching**: Redis
- **Authentication**: JWT (PyJWT + bcrypt)
- **Task Scheduling**: APScheduler
- **API Docs**: Swagger UI (auto-generated)

## Quick Start

### Option 1: Using Docker (Recommended - Works on All Platforms)

**Prerequisites:**
- Docker Desktop (macOS/Windows) or Docker Engine (Linux)
- Docker Compose (included with Docker Desktop)

**Installation:**

1. **Install Docker**
   - **macOS/Windows**: Download [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - **Linux**: 
     ```bash
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     sudo usermod -aG docker $USER
     ```

2. **Clone and Run**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd wn
   chmod +x start-docker.sh
   # Quick start with helper script
   ./start-docker.sh

   # OR manually with docker-compose
   docker-compose up -d

   # Check logs
   docker-compose logs -f app
   ```

3. **Access the API**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs

4. **Verify Everything is Running**
   ```bash
   # Check all containers are healthy
   docker-compose ps

   # Test API
   curl http://localhost:8000/prices
   ```

**Docker Commands:**
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f app

# Restart app only
docker-compose restart app

# Rebuild after code changes
docker-compose up -d --build

# Clean up everything (including database)
docker-compose down -v
```



---

### Option 2: Manual Installation (Local Development)

### Prerequisites
- Python 3.10 or higher
- PostgreSQL 14 or higher
- Redis (optional, for caching bonus feature)

### Installation & Setup

#### Step 1: Install PostgreSQL

**macOS:**
```bash
# Install using Homebrew
brew install postgresql@14

# Start PostgreSQL service
brew services start postgresql@14

# Verify it's running
psql --version
```

**Linux (Ubuntu/Debian):**
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -i -u postgres
```

**Windows:**
```powershell
# Download installer from https://www.postgresql.org/download/windows/
# Run the installer and follow the setup wizard
# Default port: 5432, remember the postgres password you set

# After installation, add PostgreSQL to PATH
# Then verify:
psql --version
```

#### Step 2: Clone and Setup Project

```bash
# Clone the repository
git clone <repository-url>
cd wn

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Create Database

**macOS/Linux:**
```bash
# Create database (as your user)
createdb wealthwise

# Or if you need to use postgres user:
sudo -u postgres createdb wealthwise

# Load schema and sample data
psql wealthwise -f setup.sql
```

**Windows:**
```powershell
# Open Command Prompt or PowerShell
# Create database using psql
psql -U postgres -c "CREATE DATABASE wealthwise;"

# Load schema and sample data
psql -U postgres -d wealthwise -f setup.sql
```

#### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# macOS/Linux
cat > .env << EOF
DATABASE_URL=postgresql://localhost/wealthwise
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-this-in-production
EOF
```

**Windows:** Create `.env` file manually with these contents:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost/wealthwise
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-this-in-production
```

*Note: Replace `yourpassword` with your PostgreSQL password set during installation*

#### Step 5: Start Redis (Optional - for caching)

**macOS:**
```bash
brew install redis
brew services start redis
```

**Linux:**
```bash
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

**Windows:**
```powershell
# Download Redis for Windows from https://github.com/microsoftarchive/redis/releases
# Or use WSL2 with Linux instructions above
# Or use Docker:
docker run -d -p 6379:6379 redis:latest
```

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

#### Step 6: Run the Application

```bash
# Make sure virtual environment is activated
# Make sure you're in the project directory (wn)

# Start the server
uvicorn app.main:app --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

The API is now running at: **http://localhost:8000**

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs

- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Testing the API

### Method 1: Postman

1.  Make sure the application is running via `docker compose up -d`.
2.  Open Postman and click the **Import** button.
3.  Select the `test.postman_collection.json` file from this project's root directory (you must save the JSON as this file first).
4.  The collection will be imported, with all requests grouped by category (Authentication, Users, Transactions, etc.).

### Method 2: Using Swagger UI

1. **Open Swagger UI**
   - Start the server: `uvicorn app.main:app --reload`
   - Open browser: http://localhost:8000/docs
   - You'll see all API endpoints with interactive documentation

2. **Test User Creation**
   - Find the **POST /users** endpoint
   - Click on it to expand
   - Click the **"Try it out"** button
   - Edit the request body:
   ```json
   {
     "name": "Atharv D",
     "email": "atharv@example.com"
   }
   ```
   - Click **"Execute"**
   - Check the response below (you should see user_id: 1)

3. **Test User Registration (JWT Auth)**
   - Find **POST /auth/register**
   - Click **"Try it out"**
   - Request body:
   ```json
   {
     "name": "Atharv D",
     "email": "atharv@example.com",
     "password": "securepass123"
   }
   ```
   - Click **"Execute"**
   - Copy the `access_token` from the response

4. **Authorize Protected Endpoints**
   - Click the **"Authorize"** button at the top right of Swagger UI
   - In the popup, enter: `Bearer <your-access-token>`
   - Click **"Authorize"** then **"Close"**
   - Now you can access protected endpoints like GET /auth/me

5. **Record a BUY Transaction**
   - Find **POST /transactions**
   - Click **"Try it out"**
   - Request body:
   ```json
   {
     "user_id": 1,
     "symbol": "TCS",
     "transaction_type": "BUY",
     "units": 10,
     "price": 3200.00,
     "transaction_date": "2025-01-05"
   }
   ```
   - Click **"Execute"**
   - Note the transaction_id in the response

6. **View Portfolio Summary**
   - Find **GET /portfolio-summary**
   - Click **"Try it out"**
   - Enter `user_id`: 1
   - Click **"Execute"**
   - You'll see holdings, P&L calculations, and total value

7. **Test Price Update (Admin)**
   - Find **POST /admin/update-prices**
   - Click **"Try it out"**
   - Click **"Execute"**
   - This updates all stock prices with ±2-5% fluctuation
   - Refresh portfolio summary to see updated P&L

8. **View Transaction History**
   - Find **GET /transactions**
   - Enter `user_id`: 1
   - Optionally filter by `symbol` or `transaction_type`
   - Click **"Execute"**

### Method 3: Using curl Commands

#### 1. Create a User
```bash
curl -X POST http://localhost:8000/users/create_user \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Atharv D",
    "email": "atharv@example.com"
  }'
```

Expected Response:
```json
{
  "user_id": 1,
  "name": "Atharv D",
  "email": "atharv@example.com",
  "created_at": "2025-11-08T12:30:00"
}
```

#### 2. Register User (JWT Auth)
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Atharv D",
    "email": "atharv.auth@example.com",
    "password": "securepass123"
  }'
```

#### 3. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "atharv.auth@example.com",
    "password": "securepass123"
  }'
```

Save the `access_token` from response, then use it:
```bash
# Replace <TOKEN> with actual token
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer <TOKEN>"
```

#### 4. Record BUY Transaction
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "BUY",
    "units": 10,
    "price": 3200.00,
    "transaction_date": "2025-01-05"
  }'
```

#### 5. Record Another BUY (Different Price)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "BUY",
    "units": 5,
    "price": 3300.00,
    "transaction_date": "2025-01-10"
  }'
```

#### 6. Record SELL Transaction
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "SELL",
    "units": 3,
    "price": 3400.00,
    "transaction_date": "2025-01-15"
  }'
```

#### 7. Get Portfolio Summary
```bash
curl "http://localhost:8000/portfolio-summary?user_id=1"
```

Expected Response:
```json
{
  "user_id": 1,
  "total_invested": "38900.00",
  "current_value": "40800.00",
  "total_pl": "1900.00",
  "total_pl_percent": "4.88",
  "holdings": [
    {
      "symbol": "TCS",
      "total_units": 12,
      "average_cost": "3241.67",
      "current_price": "3400.00",
      "current_value": "40800.00",
      "unrealized_pl": "1900.00",
      "unrealized_pl_percent": "4.88"
    }
  ]
}
```

#### 8. Get Transaction History
```bash
# All transactions for user
curl "http://localhost:8000/transactions?user_id=1"

# Filter by symbol
curl "http://localhost:8000/transactions?user_id=1&symbol=TCS"

# Filter by type
curl "http://localhost:8000/transactions?user_id=1&transaction_type=BUY"
```

#### 9. Update Stock Prices (Admin)
```bash
curl -X POST http://localhost:8000/admin/update-prices
```

#### 10. Get Current Prices
```bash
# All prices (shows all available stock symbols)
curl http://localhost:8000/prices

# Specific symbol
curl "http://localhost:8000/prices/TCS"
```

#### 11. Get User Details
```bash
curl "http://localhost:8000/users/1"
```

### Testing Edge Cases

#### Test 1: Sell More Than Owned (Should Fail)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "SELL",
    "units": 1000,
    "price": 3400.00,
    "transaction_date": "2025-01-20"
  }'
```
Expected: `400 Bad Request` with error message

#### Test 2: Invalid Stock Symbol (Should Fail)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "INVALID",
    "transaction_type": "BUY",
    "units": 10,
    "price": 100.00,
    "transaction_date": "2025-01-01"
  }'
```
Expected: `400 Bad Request` - Symbol not found

#### Test 3: Negative Units (Should Fail)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "BUY",
    "units": -10,
    "price": 3200.00,
    "transaction_date": "2025-01-01"
  }'
```
Expected: `422 Validation Error`

#### Test 4: Future Date (Should Fail)
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "symbol": "TCS",
    "transaction_type": "BUY",
    "units": 10,
    "price": 3200.00,
    "transaction_date": "2026-01-01"
  }'
```
Expected: `422 Validation Error`

#### Test 5: Duplicate Email (Should Fail)
```bash
curl -X POST http://localhost:8000/users/create_user \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Another User",
    "email": "atharv@example.com"
  }'
```
Expected: `409 Conflict`

#### Test 6: Non-existent User Portfolio
```bash
curl "http://localhost:8000/portfolio-summary?user_id=9999"
```
Expected: `404 Not Found`

### Testing Background Jobs

The price update scheduler runs automatically every 1 minute. To test it immediately:

1. **Check current prices:**
   ```bash
   curl http://localhost:8000/prices
   ```

2. **Trigger manual update:**
   ```bash
   curl -X POST http://localhost:8000/admin/update-prices
   ```

3. **Verify prices changed:**
   ```bash
   curl http://localhost:8000/prices
   ```
   Prices should have changed by ±2-5%

4. **Check portfolio with new prices:**
   ```bash
   curl "http://localhost:8000/portfolio-summary?user_id=1"
   ```
   P&L values should reflect the updated prices

### Testing Redis Caching

1. **First portfolio request** (cache miss):
   ```bash
   time curl "http://localhost:8000/portfolio-summary?user_id=1"
   ```

2. **Second request** (cache hit - faster):
   ```bash
   time curl "http://localhost:8000/portfolio-summary?user_id=1"
   ```

3. **Add transaction** (invalidates cache):
   ```bash
   curl -X POST http://localhost:8000/transactions \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": 1,
       "symbol": "INFY",
       "transaction_type": "BUY",
       "units": 5,
       "price": 1550.00,
       "transaction_date": "2025-01-20"
     }'
   ```

4. **Next portfolio request** (cache miss again):
   ```bash
   curl "http://localhost:8000/portfolio-summary?user_id=1"
   ```

To verify caching in Redis:
```bash
# Check Redis has the cache (correct key format)
redis-cli KEYS "portfolio:*"

# See cache content (use user_id directly, not "user:1")
redis-cli GET "portfolio:1"

# Cache expires after 5 minutes or when transactions are added
```

## Troubleshooting

### Docker Issues

**Error: "Cannot connect to Docker daemon"**
```bash
# macOS/Windows: Make sure Docker Desktop is running
# Linux: Start Docker service
sudo systemctl start docker
```

**Error: "Port already in use"**
```bash
# Check what's using the ports
# macOS/Linux:
lsof -i :8000
lsof -i :5432

# Stop conflicting services or change ports in docker-compose.yml
# Example: Change app port to 8001
ports:
  - "8001:8000"
```

**Error: "Database connection failed" in Docker**
```bash
# Check if PostgreSQL container is healthy
docker-compose ps

# If postgres is unhealthy, check logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

**Container won't start:**
```bash
# View detailed logs
docker-compose logs app

# Check all container statuses
docker-compose ps

# Rebuild from scratch
docker-compose down -v
docker-compose up -d --build
```

**App shows old code after changes:**
```bash
# Rebuild the image
docker-compose up -d --build

# Or completely rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### PostgreSQL Connection Issues

**Error: "could not connect to server"**
```bash
# Check if PostgreSQL is running
# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql

# Windows:
# Check Services app for "postgresql" service
```

**Error: "database does not exist"**
```bash
# Create the database
createdb wealthwise

# Or using psql:
psql -U postgres -c "CREATE DATABASE wealthwise;"
```

**Error: "role does not exist"**
```bash
# Create PostgreSQL user (if needed)
# macOS/Linux:
createuser -s yourusername

# Windows:
psql -U postgres -c "CREATE USER yourusername WITH SUPERUSER;"
```

### Python/Dependency Issues

**Error: "ModuleNotFoundError"**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "email-validator not found"**
```bash
pip install email-validator
```

### Redis Issues

**Error: "Connection refused (Redis)"**
- The app will work without Redis (caching disabled)
- To fix: Start Redis service as shown in Step 5

**Verify Redis is running:**
```bash
redis-cli ping
# Should return: PONG
```

### Port Already in Use

**Error: "Address already in use"**
```bash
# Find process using port 8000
# macOS/Linux:
lsof -i :8000

# Windows:
netstat -ano | findstr :8000

# Kill the process or use different port:
uvicorn app.main:app --reload --port 8001
```

## Database Schema

### Users Table
```sql
user_id         SERIAL PRIMARY KEY
name            VARCHAR(100)
email           VARCHAR(255) UNIQUE
password_hash   VARCHAR(255)
created_at      TIMESTAMP
```

### Transactions Table
```sql
transaction_id   SERIAL PRIMARY KEY
user_id          INTEGER REFERENCES users
symbol           VARCHAR(20)
transaction_type VARCHAR(4) CHECK (BUY/SELL)
units            INTEGER CHECK (> 0)
price            DECIMAL(15,2) CHECK (> 0)
transaction_date DATE CHECK (<= today)
created_at       TIMESTAMP
```

### Prices Table
```sql
symbol          VARCHAR(20) PRIMARY KEY
current_price   DECIMAL(15,2)
updated_at      TIMESTAMP
```

## Architecture

```
┌─────────────────┐
│   FastAPI App   │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Routers │  (HTTP layer)
    └────┬────┘
         │
    ┌────┴────┐
    │Services │  (Business logic)
    └────┬────┘
         │
  ┌──────┴───────┐
  │ Repositories │  (Data access)
  └──────┬───────┘
         │
   ┌─────┴──────┐
   │ PostgreSQL │
   └────────────┘
```

## Key Implementation Details

### Portfolio Calculations

**Weighted Average Cost:**
```
avg_cost = total_buy_cost / total_buy_units
```

**Unrealized P&L:**
```
unrealized_pl = (current_price - avg_cost) × current_units
pl_percentage = (unrealized_pl / cost_basis) × 100
```

### Error Handling

The API handles these edge cases:
- Selling more units than owned (400 Bad Request)
- Invalid stock symbols (400 Bad Request)
- Non-existent users (404 Not Found)
- Duplicate emails (409 Conflict)
- Negative units or prices (422 Validation Error)
- Future transaction dates (422 Validation Error)

### Data Validation

All inputs are validated using Pydantic models with custom validators:
- Email format verification
- Positive values for units and prices
- Transaction date not in the future
- Transaction type must be BUY or SELL

## Project Structure

```
wn/
├── app/
│   ├── routers/          # API endpoints
│   │   ├── users.py
│   │   ├── transactions.py
│   │   ├── portfolio.py
│   │   ├── prices.py
│   │   ├── auth.py
│   │   └── admin.py
│   ├── services/         # Business logic
│   │   ├── portfolio_service.py
│   │   ├── transaction_service.py
│   │   ├── auth_service.py
│   │   └── cache_service.py
│   ├── repositories/     # Data access
│   │   ├── user_repository.py
│   │   ├── transaction_repository.py
│   │   └── price_repository.py
│   ├── schemas/          # Pydantic models
│   │   ├── user.py
│   │   ├── transaction.py
│   │   ├── portfolio.py
│   │   ├── auth.py
│   │   └── common.py
│   ├── utils/            # Utilities
│   │   ├── exceptions.py
│   │   └── scheduler.py
│   ├── config.py         # Configuration
│   ├── database.py       # DB connection
│   └── main.py           # Application entry
├── setup.sql             # Database schema
├── requirements.txt      # Dependencies
├── .env.example          # Environment template
└── README.md
```

## Available Stock Symbols

The system comes pre-loaded with 15 Indian stock symbols:
- TCS, INFY, RELIANCE, HDFC, WIPRO
- ICICI, SBIN, HDFCBANK, BHARTIARTL, ITC
- KOTAKBANK, LT, AXISBANK, MARUTI, SUNPHARMA

Prices update automatically every 4 hours (±2-5% fluctuation), or trigger manually:
```bash
curl -X POST http://localhost:8000/admin/update-prices
```


## Development

### Local Development
Run with auto-reload for development:
```bash
uvicorn app.main:app --reload
```

The server will automatically restart when code changes are detected.

### Docker Development
For development with Docker and live code reload:

1. **Modify docker-compose.yml** to mount code as volume:
   ```yaml
   # Add under 'app' service:
   volumes:
     - ./app:/app/app
   command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Restart container**:
   ```bash
   docker-compose up -d --build
   ```

### Accessing Database in Docker

**PostgreSQL:**
```bash
# Connect to database
docker exec -it wealthwise-db psql -U postgres -d wealthwise

# Run SQL queries
docker exec -it wealthwise-db psql -U postgres -d wealthwise -c "SELECT * FROM users;"

# Backup database
docker exec -t wealthwise-db pg_dump -U postgres wealthwise > backup.sql

# Restore database
docker exec -i wealthwise-db psql -U postgres wealthwise < backup.sql
```

**Redis:**
```bash
# Connect to Redis CLI
docker exec -it wealthwise-redis redis-cli

# Check cached data
docker exec -it wealthwise-redis redis-cli KEYS "portfolio:*"
docker exec -it wealthwise-redis redis-cli GET "portfolio:1"
```

## Notes

- All monetary values use Decimal type to avoid floating-point errors
- Database queries are parameterized to prevent SQL injection
- Portfolio calculations handle partial sells correctly using weighted average
- Caching gracefully degrades if Redis is unavailable
- Background scheduler runs independently without blocking requests

