# DevLens Synthetic Data Generation System

This directory contains scripts for generating consistent, reproducible synthetic data for the DevLens application.

## Overview

The data generation system creates realistic developer activity data including:
- **Communication Data**: Slack-like messages with technical and social content
- **Execution Data**: Git commits with entropy calculations and file changes
- **HR Behavioral Data**: Attendance, collaboration, and performance metrics
- **Activity-Based Metrics**: Calculated metrics from communication and execution patterns

## Quick Start

### Generate All Data (Recommended)
```bash
# Run the complete pipeline
python backend/scripts/run_complete_data_pipeline.py
```

### Individual Scripts

1. **Generate Base Synthetic Data**
   ```bash
   python backend/scripts/generate_synthetic_data.py
   ```

2. **Calculate Activity Metrics**
   ```bash
   python backend/scripts/calculate_attendance_from_activity.py
   ```

3. **Test Everything**
   ```bash
   python backend/test_data_generation.py
   ```

## Generated Files

All data is saved to `backend/data/`:

- `comm_mock_data.json` - Communication messages (800 messages)
- `exec_mock_data.json` - Git commits with entropy (1200 commits) 
- `hr_behavioral_data.json` - HR and behavioral metrics (25 team members)
- `activity_based_metrics.json` - Calculated activity patterns

## Data Characteristics

### Team Structure
- **25 team members** across 4 teams:
  - Frontend (7 members)
  - Backend (7 members) 
  - DevOps (6 members)
  - QA (5 members)

### Time Period
- **Analysis Period**: May 21, 2024 - June 15, 2024 (90 days)
- **Work Days**: 19 days (excluding weekends)

### Reproducibility
- Uses **fixed seed (42)** for consistent data generation
- Same data generated every time for testing and development

## Key Features

### 1. Realistic Communication Patterns
- Technical messages weighted by team expertise
- Social interactions and team coordination
- Reply chains and threaded conversations

### 2. Sophisticated Git Metrics
- **Shannon Entropy** calculation for code complexity
- File distribution analysis across repositories
- Team-specific productivity patterns

### 3. Behavioral Analytics
- Attendance patterns inferred from activity
- Collaboration scores from communication frequency
- Knowledge sharing indicators from message content
- Innovation metrics from technical contributions

### 4. Scoring Engine Integration
- Compatible with existing `DevLensKeywordScorer`
- Quadrant analysis (Impact vs Visibility)
- Performance archetype classification

## Customization

### Modify Team Size
```python
# In generate_synthetic_data.py
self.NUM_USERS = 25  # Change this value
```

### Adjust Data Volume
```python
self.NUM_MESSAGES = 800   # Communication messages
self.NUM_COMMITS = 1200   # Git commits
```

### Change Time Period
```python
self.ANALYSIS_PERIOD_DAYS = 90  # Analysis window
self.start_time = datetime(2024, 5, 21, 8, 0, 0)  # Start date
```

## Integration with DevLens

The generated data works seamlessly with:
- Backend API endpoints
- Frontend dashboard components
- Scoring and analytics engine
- Database import scripts

## Troubleshooting

### Common Issues

1. **Unicode Errors on Windows**
   - Fixed: Removed emoji characters for Windows compatibility

2. **Path Issues**
   - Fixed: Uses `os.path.join()` for cross-platform compatibility

3. **Missing Dependencies**
   ```bash
   pip install pandas numpy
   ```

### Verify Installation
```bash
python backend/test_data_generation.py
```

## Next Steps

After generating data:

1. **Start Backend Server**
   ```bash
   python backend/main.py
   ```

2. **Start Frontend**
   ```bash
   cd frontend && npm start
   ```

3. **View Dashboard**
   - Open browser to `http://localhost:3000`
   - Explore the synthetic team data

## Data Schema

### Communication Message
```json
{
  "id": "m_0001",
  "createdDateTime": "2024-05-21T08:00:00Z",
  "from": {
    "user": {
      "id": "teams_guid_001",
      "displayName": "Alex Chen",
      "team": "Frontend"
    }
  },
  "body": {
    "content": "<div>Fixed authentication bug</div>"
  }
}
```

### Git Commit
```json
{
  "sha": "sha_exec_00001",
  "commit": {
    "author": {
      "name": "Alex Chen",
      "date": "2024-05-21T08:00:00Z"
    }
  },
  "devlens_meta": {
    "teams_user_id": "teams_guid_001",
    "team": "Frontend",
    "stats": {
      "additions": 45,
      "deletions": 12,
      "total_entropy": 1.23
    }
  }
}
```

This system provides a solid foundation for testing and developing DevLens features with realistic, consistent data.