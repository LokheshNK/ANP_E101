#  DevLens: The Silent Architect Finder

**DevLens** is an engineering intelligence dashboard designed to solve the **Visibility Paradox** in remote and hybrid teams. It mathematically separates "Social Noise" from "Technical Impact" to ensure that quiet, high-value contributors are recognized and rewarded fairly.

---

##  The Problem: The Visibility Paradox
In modern software teams, "being seen" is often confused with "being productive." Performance reviews frequently suffer from bias toward "loud" employees who dominate Slack channels or spam low-value commits. This leads to:
* **Silent Architects** (High Impact, Low Visibility) being overlooked.
* **Recognition Gaps** where social activity is mistaken for technical leadership.
* **Burnout** of core talent who feel their "deep work" isn't valued.

##  The Solution
DevLens correlates execution data from **GitHub** with communication signals from **Slack/Teams**. By calculating a "Value Density" score and contrasting it against "Visibility," we map every developer into a **Disparity Quadrant**.



---

##  The Intelligence (Our Logic)

### 1. Value Density (The Impact Signal)
We move beyond raw commit counts to measure **Code Entropy**:
* **File Centrality:** Changes to core system files (e.g., `api-router`, `db-schema`) carry 3x more weight than "leaf" files (e.g., `README.md`, `styles.css`).
* **Work Bifurcation:** We give equal merit to **Optimization** (refactoring/bug fixes) and **Creation** (new features) to reward codebase health.
* **Review Depth:** Quantifying the quality of peer reviews to identify the team's true mentors.

### 2. Communication Filtering (NLP)
We use a keyword-weighting engine to differentiate between "Chatter" and "Contribution":
* **Social Noise:** "Good morning," "Coffee?" → **0.0 Weight.**
* **Technical Signal:** "Refactored the auth-middleware to reduce latency" → **1.5x Weight.**
* **Link Bonus:** Messages containing GitHub/Jira links receive a **2.0x multiplier** as they represent active unblocking.

### 3. Z-Score Normalization
To ensure fairness regardless of team size (3 vs. 50), we use **Z-Score Normalization**:
$$Z = \frac{(x - \mu)}{\sigma}$$
This ranks individuals relative to their **Team Mean ($\mu$)**, making the data scale-invariant and mathematically stable.



---

##  Tech Stack
* **Frontend:** React.js, Tailwind CSS, Recharts (Data Visualization).
* **Backend:** FastAPI (Python).
* **Data Science:** Pandas & NumPy for vectorized statistical calculations.
* **Architecture:** Designed for **CPU-only** environments; high performance with zero GPU overhead.



---

##  How to Run

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload