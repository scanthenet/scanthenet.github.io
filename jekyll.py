
import re
import os

sql_file = r"C:\Users\sirfe\Downloads\scanthen.2026-03-14\fullrestorescanthen\mysql\scanthen_F0Gsup6G.sql"
output_dir = r"C:\Users\sirfe\blog_migration\posts"
os.makedirs(output_dir, exist_ok=True)

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pattern = r"\(\d+,\d+,'(\d{4}-\d{2}-\d{2})[^']*','[^']*','(.*?)','(publish)',"
matches = re.findall(pattern, content)

print(f"Posts encontrados: {len(matches)}")

for i, m in enumerate(matches):
    date, post_content, status = m
    clean_content = re.sub(r'<[^>]+>', '', post_content)
    clean_content = clean_content.replace('\\n', '\n').replace("\\'", "'")
    title = clean_content[:50].strip().replace('/', '-')
    filename = f"{date}-post-{i+1}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"---\nlayout: post\ntitle: \"{title}\"\ndate: {date}\n---\n\n{clean_content}")

print("Archivos creados en:", output_dir)
