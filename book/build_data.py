import json
import os

# Map your display categories (from metadata.json) to your local folder names
CATEGORY_MAP = {
    "Architecture & Fundamentals": "01_Basics",
    "Web Infrastructure": "02_Web_Fundamentals",
    "Frontend Core": "03_HTML_CSS",
    "Data & Backend Principles": "04_Data_and_MVC",
    "Backend Development": "05_Backend_Flask",
    "Security & Operations": "06_APIs_Security",
    "Advanced Frontend": "07_Frontend_Advanced",
    "Lifecycle & DevOps": "08_Testing_DevOps",
    "Practical Experiments": "Practical_Experiments"
}

EXP_FOLDER_MAP = {
    "exp01": "01-experiment1",
    "exp02": "02-experiment-templates",
    "exp03": "03-experiment-simple-flask-app",
    "exp04": "04-experiment-sqlitedb",
    "exp05": "05-experiment-sqlalchemy",
    "exp06": "06-experiment-flask-sqlalchemy",
    "exp07": "07-experiment-flask-fullstack-setup",
    "exp08": "08-experiment-flask-restful",
    "exp09": "09-experiment-flask-setup-logging",
    "exp10": "10-experiment-fts"
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
        dir_name = CATEGORY_MAP.get(category_name)
        
        if not dir_name:
            continue

        processed_category = {
            "category": category_name,
            "topics": []
        }

        for topic in category_item["topics"]:
            topic_name = topic["name"]
            # To support numbering conventions like '00_overview', you might need to adjust this matching logic
            # depending on how exactly files are named. 
            slug = slugify(topic_name)
            
            # Since files might have prefixes like "00_", we search for files ending with the slug
            md_content = ""
            code_content = ""
            
            dir_path = os.path.join(project_root, dir_name)
            if category_name == "Practical Experiments":
                topic_id = topic.get("id")
                exp_folder = EXP_FOLDER_MAP.get(topic_id)
                if exp_folder:
                    exp_path = os.path.join(dir_path, exp_folder)
                    md_content = load_file_content(os.path.join(project_root, "Screencast_Theory", f"{topic_id}.md"))
                    if os.path.exists(exp_path):
                        for root, dirs, files in os.walk(exp_path):
                            # Exclude hidden directories and bootstrap
                            dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() != 'bootstrap' and d.lower() != 'node_modules']
                            
                            for file in files:
                                # Skip hidden files and maps
                                if file.startswith('.') or file.endswith('.map'): continue
                                
                                if file.endswith((".py", ".js", ".css", ".html", ".sql", ".yaml", ".sh", ".txt", ".env")):
                                    rel_path = os.path.relpath(os.path.join(root, file), exp_path)
                                    code_content += f"// --- {rel_path} ---\n" + load_file_content(os.path.join(root, file)) + "\n\n"
            elif os.path.exists(dir_path):
                for filename in os.listdir(dir_path):
                    if slug in filename.lower() or filename.lower().endswith(f"{slug}.md") or filename.lower().endswith(f"{slug}.py") or slug.replace("_", "") in filename.lower().replace("_", ""):
                        if filename.endswith(".md"):
                            md_content = load_file_content(os.path.join(dir_path, filename))
                        elif filename.endswith((".py", ".js", ".css", ".html", ".sql", ".yaml")):
                            code_content += f"// --- {filename} ---\n" + load_file_content(os.path.join(dir_path, filename)) + "\n\n"

            processed_topic = topic.copy()
            processed_topic["theory"] = md_content
            processed_topic["code"] = code_content
            processed_category["topics"].append(processed_topic)

        book_data.append(processed_category)

    # Save aggregated data as JS for browser usage
    output_js = os.path.join(script_dir, "book_data.js")
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("const SOURCE_DATA = ")
        json.dump(book_data, f, indent=2)
        f.write(";")
        
    print(f"Successfully generated {output_js}")

if __name__ == "__main__":
    main()
