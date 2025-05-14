import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
import python-docx as docx
import json
import matplotlib.pyplot as plt
import wordcloud
from dotenv import load_dotenv

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Page configuration
st.set_page_config(
    page_title="Smart ATS - Resume Evaluator",
    page_icon="📄",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    /* Dark theme colors */
    :root {
        --background-color: #0E1117;
        --secondary-background-color: #262730;
        --text-color: #FAFAFA;
        --accent-color: #4F8BF9;
        --success-color: #00CC66;
        --warning-color: #F0AD4E;
        --error-color: #FF4B4B;
    }
    
    .main {
        background-color: var(--background-color);
        color: var(--text-color);
        padding: 2rem;
    }
    
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: var(--accent-color);
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
    }
    
    .stButton>button:hover {
        background-color: #3A6ED0;
    }
    
    .block-container {
        padding-top: 2rem;
        background-color: var(--background-color);
    }
    
    h1, h2, h3 {
        color: var(--accent-color) !important;
    }
    
    .stTextArea textarea {
        background-color: var(--secondary-background-color);
        color: var(--text-color);
        border: 1px solid #4B4B4B;
    }
    
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
        background-color: var(--secondary-background-color);
        border: 1px solid #4B4B4B;
    }
    
    /* Custom styles for file uploader */
    .uploadedFile {
        background-color: var(--secondary-background-color);
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Metric styles */
    .css-1wivap2 {
        background-color: var(--secondary-background-color);
        border: 1px solid #4B4B4B;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Divider style */
    hr {
        border-color: #4B4B4B;
    }

    /* Logo style */
    .logo-emoji {
        font-size: 4rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = "".join(page.extract_text() or "" for page in reader.pages)
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragrapaths])

def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    return None

input_prompt = """
Hey, act like a skilled ATS (Applicant Tracking System) with expertise in software engineering, data science, and big data. Evaluate the resume against the given job description in a competitive job market.

Resume: {text}
Job Description: {jd}

Response format:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

def create_wordcloud(keywords):
    wc = wordcloud.WordCloud(
        width=800,
        height=400,
        background_color='#262730',  # Dark background
        colormap='viridis',
        max_words=50,
        prefer_horizontal=0.7
    ).generate(" ".join(keywords))
    return wc

def main():
    try:
        # Header section with emoji logo
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="logo-emoji">📊</div>', unsafe_allow_html=True)
            st.title("Smart ATS - Resume Evaluator")
            st.markdown("### Optimize Your Resume for ATS Systems")
        
        st.markdown("---")

        # Input section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Job Description")
            jd = st.text_area(
                "Paste the job description here",
                height=300,
                placeholder="Enter the job description you want to analyze your resume against..."
            )

        with col2:
            st.markdown("### 📎 Resume Upload")
            st.markdown("#### 📄 Upload your resume below")
            uploaded_file = st.file_uploader(
                "Upload your resume",
                type=["pdf", "docx", "txt"],
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if uploaded_file:
                with st.expander("📋 File Details", expanded=True):
                    file_details = {
                        "Filename": uploaded_file.name,
                        "File size": f"{uploaded_file.size/1024:.2f} KB",
                        "File type": uploaded_file.type
                    }
                    for key, value in file_details.items():
                        st.write(f"**{key}:** {value}")

        # Analysis button
        if st.button("🔍 Analyze Resume", use_container_width=True):
            if uploaded_file and jd:
                with st.spinner("🔄 Analyzing your resume..."):
                    resume_text = extract_text(uploaded_file)
                    if resume_text:
                        formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
                        response_text = get_gemini_response(formatted_prompt)
                        
                        try:
                            response_data = json.loads(response_text)
                            
                            # Results section
                            st.markdown("---")
                            st.markdown("### 📊 ATS Evaluation Report")
                            
                            # Create three columns for metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                match_score = response_data['JD Match'].replace('%', '')
                                st.metric(
                                    "Match Score",
                                    f"{match_score}%",
                                    delta=None
                                )

                            # Profile Summary in a card-like container
                            st.subheader("🎯 Profile Summary")
                            st.markdown(f"""
                                <div style='background-color: #262730; padding: 20px; border-radius: 5px; margin: 10px 0;color:white'>
                                    {response_data['Profile Summary']}
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Missing Keywords
                            st.subheader("🔑 Missing Keywords")
                            if response_data['MissingKeywords']:
                                cols = st.columns(3)
                                for idx, keyword in enumerate(response_data['MissingKeywords']):
                                    cols[idx % 3].markdown(
                                        f"""<div style='background-color: #262730; padding: 10px; 
                                        border-radius: 5px; margin: 5px 0;color:white'>{keyword}</div>""",
                                        unsafe_allow_html=True
                                    )
                                
                                # Word Cloud with dark theme
                                st.subheader("📈 Keyword Visualization")
                                wc = create_wordcloud(response_data['MissingKeywords'])
                                fig, ax = plt.subplots(figsize=(10, 5))
                                plt.style.use('dark_background')
                                ax.imshow(wc, interpolation='bilinear')
                                ax.axis("off")
                                st.pyplot(fig)
                            else:
                                st.success("✨ Great job! No missing keywords found.")
                                
                        except json.JSONDecodeError:
                            st.error("❌ Failed to process response. Please try again.")
                    else:
                        st.error("❌ Unable to extract text from the uploaded file. Please check the file format.")
            else:
                st.warning("⚠️ Please upload a resume and enter a job description to proceed.")
                
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")
        
if __name__ == "__main__":
    main()
