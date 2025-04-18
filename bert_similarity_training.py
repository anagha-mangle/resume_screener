

import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

# Load dataset
df = pd.read_csv(r"C:\Users\satya\Desktop\resume_builder\data\dataset.csv").dropna()

resumes = df['Resume'].astype(str).tolist()
categories = df['Category'].astype(str).tolist()
job_descriptions = [f"Looking for a professional in {c}" for c in categories]

# ========== BERT MODEL SCORING ==========
print("\n Calculating similarity with BERT...")

# Load pre-trained Sentence-BERT
bert_model = SentenceTransformer("all-MiniLM-L6-v2")
resume_embeddings_bert = bert_model.encode(resumes, convert_to_tensor=True, show_progress_bar=True)
job_embeddings_bert = bert_model.encode(job_descriptions, convert_to_tensor=True, show_progress_bar=True)

# Compute BERT similarity
bert_scores = []
for i in tqdm(range(len(resumes))):
    sim = util.cos_sim(resume_embeddings_bert[i], job_embeddings_bert[i]).item()
    bert_scores.append(round(sim * 100, 2))  # convert to %

df['BERT_Score'] = bert_scores

# ========== TF-IDF SCORING ==========
print("\n Calculating similarity with TF-IDF...")

tfidf = TfidfVectorizer()
tfidf_scores = []

for i in tqdm(range(len(resumes))):
    docs = [job_descriptions[i], resumes[i]]
    tfidf_matrix = tfidf.fit_transform(docs)
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    tfidf_scores.append(round(sim * 100, 2))  # convert to %

df['TFIDF_Score'] = tfidf_scores

# ========== COMPARISON ==========
avg_bert = df['BERT_Score'].mean()
avg_tfidf = df['TFIDF_Score'].mean()

print("\n Average Similarity Scores:")
print(f"BERT:   {avg_bert:.2f}%")
print(f"TF-IDF: {avg_tfidf:.2f}%")

best_model = "BERT" if avg_bert > avg_tfidf else "TF-IDF"
print(f"\n Best Model: {best_model}")

# ========== SAVE RESULTS ==========
df.to_csv("data/bert_vs_tfidf_scores.csv", index=False)
print("\nResults saved to data/bert_vs_tfidf_scores.csv")
