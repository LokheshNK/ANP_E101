# DevLens Frontend

A professional developer performance analytics dashboard built with React and Tailwind CSS.

## Features

- **Performance Impact Matrix**: Interactive scatter plot visualization showing developer impact vs visibility metrics
- **Performance Rankings**: Real-time leaderboard of team members based on impact scores
- **Individual Analytics**: Detailed performance metrics for each developer
- **Professional UI**: Clean, modern interface designed for enterprise environments

## Technology Stack

- **React 18**: Modern React with hooks and functional components
- **Tailwind CSS**: Utility-first CSS framework for consistent styling
- **Recharts**: Professional charting library for data visualization
- **Lucide React**: Clean, consistent icon library

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Open [http://localhost:3000](http://localhost:3000) to view the application

## Project Structure

```
src/
├── components/
│   ├── Dashboard.jsx     # Main analytics dashboard
│   ├── Sidebar.jsx       # Navigation sidebar
│   └── UserStats.jsx     # Individual developer metrics
├── App.js               # Main application component
├── index.js             # Application entry point
└── index.css            # Global styles and Tailwind imports
```

## Design Principles

- **Professional**: Clean, business-appropriate interface
- **Consistent**: Unified color scheme and typography
- **Accessible**: High contrast ratios and semantic HTML
- **Responsive**: Optimized for various screen sizes
- **Performance**: Efficient rendering and smooth interactions

## API Integration

The frontend connects to the backend API at `http://127.0.0.1:8000/api/dashboard` to fetch developer performance data.