# Smart ATS Resume Analyzer

## Overview
A Streamlit-powered web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) using Google's Gemini AI.

## Features
- Resume text extraction from PDF, DOCX, and TXT files
- Job description comparison
- ATS compatibility scoring
- Keyword matching analysis
- Detailed profile summary
- Keyword visualization

## Prerequisites

- Python 3.8+
- Streamlit
- Google Generative AI
- PyPDF2
- python-docx
- python-dotenv
- matplotlib
- wordcloud

## Installation
```bash
git clone https://github.com/yourusername/ats-resume-analyzer.git
cd ats-resume-analyzer
pip install -r requirements.txt
```



## Images

![Image](https://github.com/user-attachments/assets/d635f16a-1081-4102-b758-563f9c038b9d)

![Image](https://github.com/user-attachments/assets/4c9d1882-ccc3-4247-b8ee-13175388a1ce)



## Setup

1. Create a .env file
   
Add your Google API key: GOOGLE_API_KEY="your_api_key_here" (use markersuite website to generate API)

3. Running the App
   
streamlit run app.py

## How to Use

- Paste job description
- Upload resume
- Click "Analyze Resume"
- Review ATS compatibility report


## Contributing

Pull requests welcome. For major changes, open an issue first.

## License
[MIT]




