from groq import Groq
import fitz
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def parse_resume(file_bytes):
    pdf = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text


def get_match_score(resume_text, job_description):
    prompt = f"""
    You are an expert HR analyst. Analyze the resume against the job description across 25 parameters including skills, experience, education, tools, responsibilities, certifications, projects, communication, leadership, problem solving, and domain knowledge.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return your response in this exact format:
    MATCH_SCORE: <number between 0 and 100>
    ANALYSIS: <detailed analysis in 3-4 lines>
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def get_skill_gap(resume_text, job_description):
    prompt = f"""
    You are an expert career coach. Compare the resume with the job description and identify skill gaps.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return your response in this exact format:
    PRESENT_SKILLS: <comma separated list of matching skills>
    MISSING_SKILLS: <comma separated list of missing skills>
    RECOMMENDATIONS: <3-4 actionable recommendations to bridge the gap>
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content