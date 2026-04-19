import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', '_', text)
    return re.sub(r'_+', '_', text).strip('_')

def build_data():
    # Robustly find metadata relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metadata_path = os.path.join(script_dir, 'book_metadata.json')
    if not os.path.exists(metadata_path):
        print(f"Error: {metadata_path} not found.")
        return

    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    source_data = []

    for cat in metadata['roadmap']:
        category_name = cat['category']
        folder = cat['folder']
        
        for topic in cat['topics']:
            topic_name = topic['name']
            topic_id = topic['id']
            
            # Find files
            md_file = os.path.join(folder, f"{topic_id}.md")
            # For code, we check multiple extensions
            code_file = None
            code_exts = ['.py', '.js', '.sql', '.html', '.yaml', '.css', '.sh']
            for ext in code_exts:
                potential_code = os.path.join(folder, f"{topic_id}{ext}")
                if os.path.exists(potential_code):
                    code_file = potential_code
                    language = ext[1:] if ext != '.sh' else 'bash'
                    if language == 'py': language = 'python'
                    break
            
            theory_content = ""
            if os.path.exists(md_file):
                with open(md_file, 'r', encoding='utf-8') as f:
                    theory_content = f.read()
            else:
                theory_content = f"# {topic_name}\nContent coming soon..."

            code_content = ""
            filename = ""
            if code_file:
                with open(code_file, 'r', encoding='utf-8') as f:
                    code_content = f.read()
                filename = os.path.basename(code_file)
            
            source_data.append({
                "id": topic_id,
                "title": topic_name,
                "category": category_name,
                "theory": theory_content,
                "code": code_content,
                "filename": filename,
                "language": language if code_file else ""
            })

    output_path = os.path.join(script_dir, 'book_data.js')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"const SOURCE_DATA = {json.dumps(source_data, indent=2)};")
    
    print(f"Successfully built {output_path} with {len(source_data)} topics.")

if __name__ == "__main__":
    build_data()
