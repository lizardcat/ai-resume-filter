# AI-Based Resume Screening System

## Overview
This resume filtering system helps recruiters screen job applications based on predefined criteria. It extracts skills, experience, and GPA from uploaded resumes and filters candidates based on must-have skills.

## Features
- Upload resumes in **PDF, TXT, or DOCX** format.
- Extracts **GPA, years of experience, and skills** automatically.
- Uses **fuzzy matching** to ensure flexible skill filtering.
- Responsive **Flask-based UI** with dropdown filters.

## Technologies Used
- **Python** (Backend processing)
- **Flask** (Web framework)
- **PyPDF2 & python-docx** (Resume parsing)
- **FuzzyWuzzy** (Skill matching with flexible search)
- **SQLite** (For storing uploaded resumes) *(Future enhancement)*

## Installation

### **1️. Clone the Repository**
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/ai-resume-filter.git
cd ai-resume-filter
```
### **2️. Install Dependencies**
```sh
pip install -r requirements.txt
```
### **3️. Run the Application** 
```sh
python app.py
```