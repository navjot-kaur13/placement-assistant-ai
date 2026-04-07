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
    if not jd_text.strip():
        return []

    # 1. Badi list common industry keywords ki
    master_keywords = [
        "Python", "Java", "React", "Node.js", "SQL", "AWS", "Docker", 
        "Kubernetes", "System Design", "Scalability", "Unit Testing", 
        "REST APIs", "Cloud Deployment", "NoSQL", "Machine Learning",
        "CI/CD", "Agile", "Microservices", "TypeScript", "Git", "Flask"
    ]
    
    resume_text = resume_text.lower()
    jd_text = jd_text.lower()
    
    # 2. Sirf wo words dhundo jo JD mein hain
    jd_keywords = [word for word in master_keywords if word.lower() in jd_text]
    
    # 3. Phir check karo unmein se resume mein kaunse MISSING hain
    missing = [word for word in jd_keywords if word.lower() not in resume_text]
    
    return missing[:5] # Top 5 missing return karo