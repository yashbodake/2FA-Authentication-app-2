# Docker Setup Guide for 2FA Application

This guide explains how to set up and run the 2FA application using Docker. The application consists of three services: backend (FastAPI), frontend (React/Vue), and MySQL database.

## Prerequisites

Before starting, ensure you have the following installed on your system:

- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
  - Download from [https://www.docker.com/get-started](https://www.docker.com/get-started)
- **Docker Compose** (usually included with Docker Desktop)
  - If installing separately: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

## Getting the Project

You can get the project in one of these ways:

### Option 1: If you have the ZIP file
1. Extract the ZIP file to a folder on your computer
2. Open a terminal/command prompt in the extracted folder
3. You should see the project structure with `backend/`, `frontend/`, and `docker-compose.yml`

### Option 2: If using Git
```bash
git clone <repository-url>
cd 2FA-APP
```

## Project Structure

After extracting/obtaining the project, you should have this structure:

```
2FA-APP/
├── docker-compose.yml          # Main Docker configuration
├── README.md                   # Main documentation
├── backend/
│   ├── Dockerfile              # Backend container configuration
│   ├── main.py                 # Main application code
│   ├── requirements.txt        # Python dependencies
│   └── db.sql                  # Database schema
└── frontend/
    ├── Dockerfile              # Frontend container configuration
    ├── package.json            # Node.js dependencies
    └── ...                     # Frontend source files
```

## Setting Up Docker

### Step 1: Open Terminal in Project Directory
Open your command prompt, PowerShell, or terminal and navigate to the project folder:

```bash
cd /path/to/2FA-APP
```

### Step 2: Build and Start the Services

Run the following command to build and start all services:

```bash
docker-compose up --build
```

This command will:
- Download required base images (Python, Node.js, MySQL)
- Build your custom backend and frontend images
- Start all three services (backend, frontend, database)
- Create a Docker network connecting all services

**Note:** The first time you run this, it may take 3-5 minutes to download and build everything.

### Step 3: Verify Services are Running

After successful startup, you should see all services running. In a new terminal, you can check:

```bash
docker-compose ps
```

You should see three services running:
- `2fa-app-backend-1`
- `2fa-app-frontend-1`
- `2fa-app-db-1`

### Step 4: Access the Application

Once everything is running, access the application at:

- **Frontend (User Interface):** [http://localhost:8080](http://localhost:8080)
- **Backend API:** [http://localhost:8000](http://localhost:8000)
- **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

## Understanding the Docker Setup

### Services in docker-compose.yml

The `docker-compose.yml` file defines three services:

1. **backend**
   - Builds from `backend/Dockerfile`
   - Runs on port 8000
   - Connects to the database service

2. **frontend**
   - Builds from `frontend/Dockerfile`
   - Runs on port 8080
   - Serves the user interface

3. **db**
   - Uses official MySQL 8.0 image
   - Stores data persistently using Docker volumes
   - Connects to backend service

### Environment Variables

The setup uses these environment variables:
- Database: `root_password`, `mydatabase`, `user`/`password`

## Common Docker Commands

### Starting Services
```bash
# Build and start (first time or when code changes)
docker-compose up --build

# Start without rebuilding (faster, when no code changes)
docker-compose up
```

### Running in Background
```bash
# Start services in background
docker-compose up --build -d

# Check running services
docker-compose ps
```

### Stopping Services
```bash
# Stop services (if running in foreground, press Ctrl+C)
docker-compose down

# Stop services (if running in background)
docker-compose down
```

### Viewing Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
```

### Rebuilding Specific Service
```bash
# Rebuild only backend
docker-compose build backend
docker-compose up --build backend

# Rebuild only frontend
docker-compose build frontend
docker-compose up --build frontend
```

## Database Setup and Management

### Initial Database Setup
The database tables are created using the `backend/db.sql` file. This happens automatically when you run:

```bash
docker-compose up --build
```

### Accessing the Database

You can access the MySQL database from the command line:

```bash
# Execute a command
docker exec 2fa-app-db-1 mysql -u root -proot_password -e "USE mydatabase; SHOW TABLES;"

# Enter MySQL interactive mode
docker exec -it 2fa-app-db-1 mysql -u root -proot_password mydatabase
```

## Troubleshooting Common Issues

### Issue 1: Ports Already in Use
**Error:** "port is already allocated"
**Solution:** Make sure nothing else is running on ports 8000 and 8080

### Issue 2: Out of Memory
**Solution:** Increase Docker's memory allocation in Docker Desktop settings

### Issue 3: Build Failures
**Solution:**
```bash
# Clean up Docker system
docker system prune -a

# Rebuild
docker-compose up --build
```

### Issue 4: Database Connection Errors
**Solution:** Make sure all services are running:
```bash
docker-compose ps
```

### Check if services are healthy:
- All services show "Up" status
- No error messages in logs: `docker-compose logs backend`

## Stopping and Cleaning Up

### Normal Shutdown
```bash
# Press Ctrl+C in the terminal where you ran docker-compose up
# OR in another terminal:
docker-compose down
```

### Complete Cleanup (removes containers, networks, but keeps volumes)
```bash
docker-compose down
```

### Clean Up Everything (removes containers, networks, and volumes)
```bash
docker-compose down -v
```

## Tips for Success

1. **First Time:** Expect the initial build to take 3-5 minutes
2. **Internet Connection:** Required for first build to download base images
3. **System Resources:** Ensure you have at least 2GB free disk space
4. **Persistent Data:** Database data is preserved between runs using volumes
5. **Development:** Services will restart automatically when you change code

## Next Steps

Once your Docker setup is running:

1. Access the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs)
2. Register a new user using the registration endpoint
3. Test the 2FA functionality
4. Use the frontend interface at [http://localhost:8080](http://localhost:8080)

## Getting Help

If you encounter issues:

1. Check that Docker is running
2. Verify you're in the correct project directory
3. Ensure ports 8000 and 8080 are available
4. Check the logs: `docker-compose logs backend`
5. Restart Docker if needed