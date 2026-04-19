import json
import os

# Map category display names (from metadata.json) to their local folder names.
CATEGORY_MAP = {
    "Basic terminologies of Web": ["Basics", "Web_Fundamentals"],
    "Webpages written in HTML and CSS": ["HTML_CSS", "Practical_Experiments"],
    "Presentation layer - View": ["Frontend_Advanced", "Practical_Experiments"],
    "Models - Introduction to databases": ["Data_and_MVC", "Practical_Experiments"],
    "Controllers - Business logic": ["Data_and_MVC", "Practical_Experiments"],
    "APIs and REST APIs": ["Backend_Flask", "Practical_Experiments"],
    "Backend Systems": ["Backend_Flask", "Data_and_MVC", "Practical_Experiments"],
    "Application Frontend": ["Frontend_Advanced", "Practical_Experiments"],
    "Application Security": ["APIs_Security"],
    "Testing of Web Applications": ["Testing_DevOps"],
    "HTML Evolution and Beyond HTML": ["Frontend_Advanced"],
    "Application Deployment": ["Testing_DevOps"]
}

EXP_FOLDER_MAP = {
    "exp01": "experiment1",
    "exp02": "experiment-templates",
    "exp03": "experiment-simple-flask-app",
    "exp04": "experiment-sqlitedb",
    "exp05": "experiment-sqlalchemy",
    "exp06": "experiment-flask-sqlalchemy",
    "exp07": "experiment-flask-fullstack-setup",
    "exp08": "experiment-flask-restful",
    "exp09": "experiment-flask-setup-logging",
    "exp10": "experiment-fts"
}

def slugify(text):
    return text.lower().replace(" ", "_").replace("&", "and")

def load_file_content(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    metadata_path = os.path.join(script_dir, "metadata.json")
    if not os.path.exists(metadata_path):
        print(f"Error: {metadata_path} not found.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    book_data = []

    for category_item in data:
        category_name = category_item["category"]
        dir_names = CATEGORY_MAP.get(category_name, [])
        
        if not dir_names:
            print(f"Warning: Category '{category_name}' not in map.")
            continue

        processed_category = {
            "category": category_name,
            "topics": []
        }

        for topic in category_item["topics"]:
            topic_name = topic["name"]
            topic_id = topic.get("id")
            slug = slugify(topic_name)
            
            md_content = ""
            code_content = ""
            if topic_id:
                exp_folder = EXP_FOLDER_MAP.get(topic_id)
                if exp_folder:
                    exp_path = os.path.join(project_root, "Practical_Experiments", exp_folder)
                    # Try to load screencast theory if it exists
                    theory_file = os.path.join(project_root, "Screencast_Theory", f"{topic_id}.md")
                    if os.path.exists(theory_file):
                        md_content = load_file_content(theory_file)
                    
                    if os.path.exists(exp_path):
                        for root, dirs, files in os.walk(exp_path):
                            dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() != 'bootstrap' and d.lower() != 'node_modules']
                            for file in files:
                                if file.startswith('.') or file.endswith('.map'): continue
                                if file.endswith((".py", ".js", ".css", ".html", ".sql", ".yaml", ".sh", ".txt", ".env")):
                                    rel_path = os.path.relpath(os.path.join(root, file), exp_path)
                                    code_content += f"// --- {rel_path} ---\n" + load_file_content(os.path.join(root, file)) + "\n\n"
            else:
                # Search across all mapped directories for theory files
                for dir_name in dir_names:
                    if dir_name == "Practical_Experiments": continue # Skip experiments folder for theory search
                    dir_path = os.path.join(project_root, dir_name)
                    if not os.path.exists(dir_path): continue
                    
                    for filename in os.listdir(dir_path):
                        # Match by slug or partial name
                        if slug in filename.lower() or filename.lower().endswith(f"{slug}.md") or slug.replace("_", "") in filename.lower().replace("_", ""):
                            if filename.endswith(".md"):
                                md_content = load_file_content(os.path.join(dir_path, filename))
                            elif filename.endswith((".py", ".js", ".css", ".html", ".sql", ".yaml")):
                                code_content += f"// --- {filename} ---\n" + load_file_content(os.path.join(dir_path, filename)) + "\n\n"
                        if md_content: break # Found it
                    if md_content: break

            processed_topic = topic.copy()
            processed_topic["theory"] = md_content
            processed_topic["code"] = code_content
            processed_category["topics"].append(processed_topic)

        book_data.append(processed_category)

    # Save aggregated data
    output_js = os.path.join(script_dir, "book_data.js")
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("const SOURCE_DATA = ")
        json.dump(book_data, f, indent=2)
        f.write(";")
        
    print(f"Successfully generated {output_js}")

if __name__ == "__main__":
    main()
