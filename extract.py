import re
import os

sql_file = r"C:\Users\sirfe\Downloads\scanthen.2026-03-14\fullrestorescanthen\mysql\scanthen_F0Gsup6G.sql"
output_dir = r"C:\Users\sirfe\blog_migration\posts"
os.makedirs(output_dir, exist_ok=True)

with open(sql_file, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

pattern = r"\(\d+,\d+,'(\d{4}-\d{2}-\d{2})[^']*','[^']*','(.*?)','(publish)',"
matches = re.findall(pattern, content)

print(f"Artículos encontrados: {len(matches)}")
for m in matches[:10]:
    print(f"- [{m[0]}] {m[1][:80]}")
