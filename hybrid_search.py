import json
from sentence_transformers import SentenceTransformer

from resume_graph import load_data, resume_graph
from search_graph import search as graph_search, parse_query
from search_vector import prepare_corpus, search_vectors

def hybrid_search(user_query, graph, model, vector_embeddings, names, top_k=5):
    skill_constraint, min_years = parse_query(user_query)

    vector_results = search_vectors(user_query, model, vector_embeddings, names, top_k=top_k*2)

    graph_results = graph_search(graph, skill_constraint, min_years)

    valid_experts = {person["name"] for person in graph_results}

    print(f"\n   [Debug] Vector Matches: {len(vector_results)}")
    print(f"   [Debug] Graph Experts: {len(valid_experts)}")

    final_results = []

    for match in vector_results:
        person_name = match["name"]
        original_score = match["score"]

        if person_name in valid_experts:
            if min_years > 0:
                new_score = original_score * 1.5
                status = "Hybrid Star"

            else:
                new_score = original_score
                status = "Semantic Match"
        
        elif min_years > 0 and person_name not in valid_experts:
            new_score = original_score * 0.5
            status = "Experience Mismatch"
        
        else:
            new_score = original_score
            status = "Semantic Match"

        final_results.append({
            "name": person_name,
            "score": new_score,
            "reason": status,
            "original_score": original_score
        })

        return sorted(final_results, key=lambda x: x["score"], reverse = True)[:top_k]
    
if __name__ == "__main__":
    print("... Initializing Hybrid Engine ...")

    data = load_data("resume.json")
    
    G = resume_graph(data)
    
    print("... Loading AI Model ...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    names, text_corpus = prepare_corpus(data)
    embeddings = model.encode(text_corpus, convert_to_tensor=True)
    
    print("\n" + "="*50)
    print("HYBRID SEARCH ENGINE")
    print("="*50)
    
    while True:
        query = input("\nEnter Query: ").strip()
        if query.lower() in ['q', 'exit']: break
        
        results = hybrid_search(query, G, model, embeddings, names)
        
        print(f"\nTop Matches for '{query}':")
        for r in results:
            print(f"  {r['score']:.4f} | {r['name']} | {r['reason']}")