# Quickstart: Database Foundation & Schema

## Setup Instructions

### Prerequisites
- Python 3.13+
- Neon Serverless PostgreSQL account
- Environment with access to backend/ directory

### Installation
1. Install required dependencies:
   ```bash
   pip install sqlmodel psycopg2-binary python-dotenv
   ```

2. Set up environment variables:
   Copy `.env.example` to `.env` and configure your Neon database connection string.

### Database Initialization
1. Initialize the database engine:
   ```python
   from backend.src.database.engine import engine
   from backend.src.database.models import User, Task

   # Create tables in the database
   from sqlmodel import SQLModel
   SQLModel.metadata.create_all(engine)
   ```

### Basic Usage
1. Create a new user:
   ```python
   from backend.src.database.session import get_session
   from backend.src.database.models.user import User

   with get_session() as session:
       user = User(email="example@example.com")
       session.add(user)
       session.commit()
       session.refresh(user)
   ```

2. Create a task for a user:
   ```python
   from backend.src.database.session import get_session
   from backend.src.database.models.task import Task

   with get_session() as session:
       task = Task(user_id=user.id, description="Complete database setup", is_completed=False)
       session.add(task)
       session.commit()
       session.refresh(task)
   ```

### Running Tests
Execute the test suite to validate your database foundation:
```bash
pytest tests/database/
```

## Configuration
- Database connection string: Set `DATABASE_URL` in your environment variables
- Connection pooling: Configured automatically with sensible defaults
- Environment management: All credentials managed via environment variables as required