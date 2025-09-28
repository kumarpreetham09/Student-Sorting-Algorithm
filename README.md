# Student Sorting Algorithm

This project automates the process of allocating students into balanced tutorial groups.  
The program ensures diversity and fairness by considering **CGPA, gender balance, and school representation** when forming groups.

---

## 📌 Features
- Loads student data from a CSV file.
- Automatically generates **120 tutorial groups** of 50 students each.
- Distributes students across **10 groups per tutorial**, with:
  - Balanced **CGPA** distribution (high and low performers spread evenly).
  - Balanced **gender ratio** (avoiding 4+ of the same gender in a group).
  - Diversity in **school representation** (avoiding >3 of the same school in a group).
- Exports results into a clean CSV file (`FCE2_Team1.csv`).
- Provides **analysis reports** on:
  - Group GPA deviations
  - Gender imbalance
  - School concentration

---

## 📂 File Overview
- **`main()`** – Orchestrates the entire grouping process.
- **`load_data()`** – Loads student records from CSV.
- **`init_new_dict()` / `init_id_list()`** – Initializes student dictionaries and ID lists.
- **`CGPAmergesort()`** – Custom merge sort to rank students by GPA.
- **Distribution Functions**:
  - `distribute_schools()` – Ensures representation from popular schools.
  - `distribute_gender()` – Balances genders within groups.
  - `distribute_high_GPA()` / `distribute_low_GPA()` – Ensures GPA spread.
  - `distribute_remaining()` – Fills remaining spots fairly.
- **`evaluate_priority()`** – Flags groups with possible imbalance.
- **`analysis()`** – Evaluates performance of allocation.
- **`total_analysis()`** – Summarizes across all 120 tutorial groups.

---

## 📊 Output
The program generates:

1. **CSV File** (`FCE2_Team1.csv`):  
   With headings:
   ```
   Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned
   ```
   Each row represents one student with their assigned group.

2. **Analysis Report** (printed in console):  
   Example:
   ```
   EFFECTIVENESS
   GENDER: 92.5% PASSES
   SCHOOLS: 95.8% PASSES
   MAXIMUM DEVIATION: 0.85 POINTS
   ```

---

## ▶️ How to Run
1. Place your input student data in `FCE2_Team1.csv` with the following format:
   ```
   Tutorial Group,Student ID,School,Name,Gender,CGPA,Team Assigned
   ```
   (The script will overwrite this file with results.)

2. Run the script:
   ```bash
   python team_allocation.py
   ```

3. Check:
   - **`FCE2_Team1.csv`** → contains allocated groups.
   - Console output → effectiveness analysis.

---

## ⚠️ Notes
- Each tutorial group must have **exactly 50 students**.
- Ensure `FCE2_Team1.csv` exists with at least a header row before running.
- The script overwrites `FCE2_Team1.csv` during execution.
- All analysis is cumulative across **120 tutorial groups**.

---

## 🚀 Future Improvements
- Add **random seed** option for reproducibility.
- Generate **visual reports** (graphs for GPA, gender, school distributions).
- Improve handling of edge cases (e.g., uneven gender ratio in data).
