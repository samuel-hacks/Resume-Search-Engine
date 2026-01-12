import networkx as nx
from resume_graph import load_data, resume_graph

def finding_skill(graph, user_input):
    user_input = user_input.lower().strip()
    
    skills = [n for n, attr in graph.nodes(data=True) if attr.get("type") == "skill"]
    
    for skill in skills:
        if skill.lower() == user_input:
            return skill
            
    return None

def search(graph, skill_name, min_years=0):
    name = finding_skill(graph, skill_name)

    if not name:
        print(f"Skill '{skill_name}' not found in database.")
        return []

    print(f"Looking for: {name} ({min_years}+ years)...")
    
    matches = []
    potential_candidates = graph.neighbors(name)

    for person in potential_candidates:
        edge_data = graph.get_edge_data(person, name)
        exp = edge_data["weight"]

        if exp >= min_years:
            role = graph.nodes[person]["role"]
            matches.append({
                "name": person,
                "years": exp,
                "role": role
            })

    return sorted(matches, key=lambda x: x["years"], reverse=True)

def parse_query(user_input):
    parts = user_input.split()
    
    if parts[-1].isdigit():
        years = int(parts[-1])
        skill = ' '.join(parts[:-1]) 
    else:
        years = 0
        skill = user_input
        
    return skill, years

if __name__ == "__main__":
    print("... Building Knowledge Graph ...")
    resumes = load_data("resume.json")
    G = resume_graph(resumes)
    
    print("\n" + "="*40)
    print(" RESUME GRAPH SEARCH ENGINE ")
    print("="*40)
    print("Commands:")
    print(" - Type 'Java' to find all Java developers")
    print(" - Type 'Java 5' to find devs with 5+ years")
    print(" - Type 'exit' to quit")
    print("-" * 40)

    while True:
        try:
            user_query = input("\nEnter Search Query: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            skill, years = parse_query(user_query)
            
            results = search(G, skill, years)
            
            if results:
                print(f"Found {len(results)} matches:")
                for r in results:
                    print(f"   {r['name']} | {r['years']} yrs | {r['role']}")
            
        except Exception as e:
            print(f"Error: {e}")