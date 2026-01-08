# DevLens Database Setup

This project now uses SQLite3 database instead of mock JSON data.

## Database Features

- **Companies**: Store different companies
- **Managers**: Authentication and company association
- **Teams**: Organize developers by teams within companies
- **Developers**: Store developer performance data
- **Settings**: User preferences and configurations

## Getting Started

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Initialize Database

The database is automatically initialized when you first run the API:

```bash
python main.py
```

This creates `devlens.db` with sample data for 3 companies:
- **TechCorp Inc.** (john.smith@techcorp.com / admin123)
- **Innovate Solutions** (sarah.johnson@innovate.com / manager456)  
- **StartupIO** (mike.chen@startup.io / startup789)

### 3. Create New Managers

Use the interactive script to add new managers:

```bash
python create_manager.py
```

This allows you to:
- Create new managers with custom credentials
- Add developers to existing companies
- Manage the database interactively

## API Endpoints

### Authentication
- `POST /api/login` - Manager login
- `GET /api/companies` - List all companies

### Data
- `GET /api/dashboard/{company}` - Get company dashboard data
- `POST /api/managers` - Create new manager
- `POST /api/developers` - Add new developer

## Database Schema

### Companies
- id (Primary Key)
- name (Unique)
- created_at

### Managers  
- id (Primary Key)
- email (Unique)
- password_hash
- name
- role
- company_id (Foreign Key)
- created_at

### Teams
- id (Primary Key)
- name
- company_id (Foreign Key)
- created_at

### Developers
- id (Primary Key)
- name
- team_id (Foreign Key)
- company_id (Foreign Key)
- commits
- entropy
- meetings
- messages (JSON)
- created_at

## Security

- Passwords are hashed using SHA256
- Company data is isolated (managers only see their company's data)
- Input validation on all API endpoints

## Sample Data

The database comes pre-populated with realistic developer data across 3 companies, including:
- Different team structures per company
- Varied performance metrics
- Realistic commit patterns and communication data

## Extending the Database

To add new features:
1. Update the schema in `database.py`
2. Add new API endpoints in `main.py`
3. Update the frontend to use new endpoints