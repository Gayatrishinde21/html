from sentence_transformers import SentenceTransformer
import pandas as pd
import os
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Predefined correct names
correct_names_list = ["gayatri", "rohit", "priya", "anil", "rahul", "komal"]

# Precompute correct name embeddings
correct_name_embeddings = {name: model.encode(name) for name in correct_names_list}

# Excel file
output_file = "embeddings_output.xlsx"

# Input from user
user_input = input("Enter name (partial or short): ").strip()
user_embedding = model.encode(user_input)

# Find most similar correct name
best_match = None
best_score = -1

for cname, cembed in correct_name_embeddings.items():
    similarity = np.dot(user_embedding, cembed) / (np.linalg.norm(user_embedding) * np.linalg.norm(cembed))
    if similarity > best_score:
        best_score = similarity
        best_match = cname

# Show warning if similarity is too low
if best_score < 0.6:
    print(f"⚠️ Low confidence match: '{user_input}' matched to '{best_match}' (similarity: {best_score:.2f})")
else:
    print(f"✅ '{user_input}' matched to '{best_match}' (similarity: {best_score:.2f})")

# Save record
record = {
    'name': best_match,
    'embedding': correct_name_embeddings[best_match].tolist(),
    'user question': user_input,
    'user embedding': user_embedding.tolist(),
    'correct name': best_match
}

# Save to Excel
df_new = pd.DataFrame([record])

if os.path.exists(output_file):
    df_existing = pd.read_excel(output_file)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_combined = df_new

df_combined.to_excel(output_file, index=False)

print(f"📁 Data saved to '{output_file}'")
