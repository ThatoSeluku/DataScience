import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv
import re
import logging

# Enhanced configuration and error handling
class ATSConfig:
    """Centralized configuration management for the ATS application"""
    MODEL_NAME = "gemini-1.5-pro"
    MAX_FILE_SIZE_MB = 10
    SUPPORTED_FILE_TYPES = ["pdf", "docx"]

# Comprehensive logging setup
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='ats_matchpro.log'
)
logger = logging.getLogger(__name__)

def validate_file_upload(uploaded_file):
    """
    Comprehensive file validation
    
    Args:
        uploaded_file (UploadedFile): Uploaded resume file
    
    Returns:
        bool: Whether file is valid
    """
    if not uploaded_file:
        st.warning("No file uploaded.")
        return False
    
    # File size check
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > ATSConfig.MAX_FILE_SIZE_MB:
        st.error(f"File too large. Maximum size is {ATSConfig.MAX_FILE_SIZE_MB}MB.")
        return False
    
    # File type check
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension not in ATSConfig.SUPPORTED_FILE_TYPES:
        st.error(f"Unsupported file type. Please upload {' or '.join(ATSConfig.SUPPORTED_FILE_TYPES)}.")
        return False
    
    return True

def load_api_key():
    """
    Load API key from environment variable
    
    Returns:
        str: Google API key or None
    """
    try:
        api_key = ''
        
        if not api_key:
            st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
            return None
        
        return api_key
    except Exception as e:
        logger.error(f"API Key retrieval error: {e}")
        st.error("Could not retrieve API key. Please check your configuration.")
        return None

def configure_generative_model(api_key):
    """
    Configure generative AI model with enhanced safety and generation settings
    
    Args:
        api_key (str): Google API key
    
    Returns:
        genai.GenerativeModel: Configured generative model
    """
    try:
        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 0.3,  # Slightly reduced for more consistent outputs
            "top_p": 0.9,  # More conservative sampling
            "top_k": 40,  # Increased diversity
            "max_output_tokens": 2048,  # Reduced for more focused responses
        }
        
        safety_settings = [
            {"category": f"HARM_CATEGORY_{category}", 
             "threshold": "BLOCK_ONLY_HIGH"}  # More nuanced blocking
            for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
        ]
        
        return genai.GenerativeModel(
            model_name=ATSConfig.MODEL_NAME,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
    except Exception as e:
        logger.error(f"Model configuration error: {e}")
        st.error("Could not configure AI model.")
        return None

def extract_text_from_file(uploaded_file):
    """
    Unified text extraction with comprehensive error handling
    
    Args:
        uploaded_file (UploadedFile): Uploaded resume file
    
    Returns:
        str: Extracted text content
    """
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = pdf.PdfReader(uploaded_file)
            text_content = "\n".join(page.extract_text() for page in pdf_reader.pages)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text_content = docx2txt.process(uploaded_file)
        else:
            raise ValueError("Unsupported file type")
        
        # Basic text cleaning
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        if not text_content:
            st.warning("No text could be extracted from the document.")
            return None
        
        return text_content
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        st.error("Error extracting text from the document.")
        return None

def generate_ats_analysis(llm, resume_text, job_description):
    """
    Enhanced prompt for more nuanced ATS analysis
    
    Args:
        llm (genai.GenerativeModel): Generative AI model
        resume_text (str): Resume content
        job_description (str): Job description
    
    Returns:
        str: Detailed ATS analysis
    """
    enhanced_prompt = f"""
    Advanced ATS Resume Analysis Protocol:

    CONTEXT:
    - Provide a comprehensive yet concise evaluation
    - Focus on actionable insights
    - Be objective and data-driven

    RESUME CONTENT:
    {resume_text}

    JOB DESCRIPTION:
    {job_description}

    ANALYSIS REQUIREMENTS:
    1. Precise Job Description Match Percentage
    2. Critical Missing Keywords
    3. Skill Gap Analysis
    4. Recommended Resume Improvements
    5. Potential Interview Readiness Score

    Output Format:
    Job Description Match: X%
    Missing Keywords: [strategic keywords]
    Skill Gaps: [specific areas needing enhancement]
    Resume Improvement Recommendations: [targeted suggestions]
    Interview Readiness: X/10
    """
    
    try:
        response = llm.generate_content(enhanced_prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Analysis generation error: {e}")
        st.error("Could not generate ATS analysis.")
        return None

def main():
    st.set_page_config(
        page_title="ATS MatchPro: Resume Optimizer",
        page_icon="📄",
        layout="centered"
    )
    
    st.title("ATS MatchPro")
    st.markdown("""
    ## Elevate Your Job Application Strategy
    - 📊 Intelligent Resume Matching
    - 🔍 Keyword Optimization
    - 💡 Actionable Insights
    """)

    # API Key Management
    api_key = load_api_key()
    if not api_key:
        st.stop()

    # Model Configuration
    llm = configure_generative_model(api_key)
    if not llm:
        st.stop()

    # User Input Section
    job_description = st.text_area(
        "📝 Job Description", 
        height=200, 
        help="Paste the complete job description for detailed analysis"
    )
    
    uploaded_file = st.file_uploader(
        "📤 Upload Resume", 
        type=ATSConfig.SUPPORTED_FILE_TYPES,
        help="PDF or DOCX format recommended"
    )

    if st.button("🔬 Analyze Resume", use_container_width=True):
        # Validate job description
        if not job_description or len(job_description.strip()) < 50:
            st.error("Please provide a detailed job description (minimum 50 characters).")
            st.stop()

        if not validate_file_upload(uploaded_file):
            st.stop()

        resume_text = extract_text_from_file(uploaded_file)
        if not resume_text:
            st.stop()

        with st.spinner("Generating Intelligent ATS Analysis..."):
            analysis_result = generate_ats_analysis(llm, resume_text, job_description)
            
            if analysis_result:
                st.success("Analysis Complete! 🎉")
                st.write(analysis_result)
            else:
                st.error("Analysis failed. Please try again.")

if __name__ == "__main__":
    main()