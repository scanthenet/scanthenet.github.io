import os

base = r"C:\Users\sirfe\blog_migration"

config = """title: Scanthenet
description: Blog de ciberseguridad
theme: minima
"""

index = """---
layout: home
title: Scanthenet - Blog de ciberseguridad
---
"""

with open(os.path.join(base, "_config.yml"), "w") as f:
    f.write(config)

with open(os.path.join(base, "index.md"), "w") as f:
    f.write(index)

print("Archivos creados!")
