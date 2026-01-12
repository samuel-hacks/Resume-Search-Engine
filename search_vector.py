import json
from sentence_transformers import SentenceTransformer, util

def load_data(filename):
    with open(filename, "r") as f:
        return json.load(f)
    
def prepare_corpus(data):
    corpus = []
    ids = []

    for person in data:
        text = f"{person["role"]} {person["summary"]}"
        corpus.append(text)
        ids.append(person["name"])

    return ids, corpus

def search_vectors(query, model, corpus_embeddings, ids, top_k = 3):
    query_embedding = model.encode(query, convert_to_tensor = True)

    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=top_k)

    hits = hits[0]

    results = []

    for hit in hits:
        person_name = ids[hit["corpus_id"]]
        score = hit["score"]
        results.append({"name": person_name, "score": score})

    return results

if __name__ == "__main__":
    print("... Loading AI Model ...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    resumes = load_data("resume.json")
    names, text_corpus = prepare_corpus(resumes)
    
    print("... Encoding Resumes to Vectors ...")
    resume_embeddings = model.encode(text_corpus, convert_to_tensor=True)
    
    print("\n" + "="*40)
    print(" VECTOR SEARCH ENGINE ")
    print("="*40)
    
    while True:
        user_query = input("\nEnter Search Query (e.g., 'Leader'): ").strip()
        
        if user_query.lower() in ['exit', 'quit', 'q']:
            break
            
        matches = search_vectors(user_query, model, resume_embeddings, names)
        
        print(f"Top Matches for '{user_query}':")
        for m in matches:
            print(f"   {m['name']} (Score: {m['score']:.4f})")
