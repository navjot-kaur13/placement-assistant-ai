from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def match_jd(resume_text, jd_text):
    if not jd_text.strip():
        return 0.0

    documents = [resume_text, jd_text]
    vectorizer = TfidfVectorizer(stop_words="english")
    
    try:
        tfidf_matrix = vectorizer.fit_transform(documents)
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(similarity * 100, 2)
    except:
        return 0.0

def get_missing_keywords(resume_text, jd_text):
    if not jd_text.strip() or not resume_text.strip():
        return []

    # 🌐 UNIVERSAL MASTER SKILLS LIST
    master_skills = [
        # --- Data Science & AI/ML ---
        "Python", "R", "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "TensorFlow", "Keras", "Scikit-learn", "Pandas", "NumPy", "PyTorch", "LLM",
        "Generative AI", "LangChain", "Prompt Engineering", "Vector Databases", "DistilBERT",
        
        # --- Data & Business Analytics ---
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Power BI", "Tableau", "Excel", 
        "Statistics", "EDA", "Data Visualization", "Data Mining", "ETL", "Big Data",
        
        # --- Full Stack & Web Development ---
        "HTML", "CSS", "JavaScript", "React.js", "Node.js", "Express.js", "Angular",
        "Vue.js", "Django", "Flask", "FastAPI", "REST APIs", "JWT", "Redux",
        "TypeScript", "Java", "Spring Boot", "C++", "PHP", "Laravel",
        
        # --- DevOps & Cloud ---
        "AWS", "AWS Bedrock", "Azure", "Google Cloud", "Docker", "Kubernetes",
        "Git", "GitHub", "CI/CD", "Terraform", "Microservices", "System Design"
    ]
    
    resume_text_lower = resume_text.lower()
    jd_text_lower = jd_text.lower()
    
    missing = []
    for skill in master_skills:
        # 1. Kya skill JD mein hai?
        if skill.lower() in jd_text_lower:
            # 2. Kya wo resume mein MISSING hai?
            # Hum thoda extra check lagayenge taaki partial match na ho (e.g., 'Java' in 'JavaScript')
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if not re.search(pattern, resume_text_lower):
                missing.append(skill)
                
    return missing[:5] # Top 5 relevant suggestions