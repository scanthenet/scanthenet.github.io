import os
import re

# Mapeo de archivo -> categorías, tags, excerpt
POST_META = {
    "01-Scanthenet_Introduccion.md": {
        "categories": ["Teoria"],
        "tags": ["intro", "blog"],
        "excerpt": "Presentación del blog Scanthenet: objetivos, temática y metodología de trabajo."
    },
    "02-Powershell_Empire.md": {
        "categories": ["Pentest"],
        "tags": ["powershell", "empire", "c2", "windows", "red-team"],
        "excerpt": "Uso de PowerShell Empire como framework de Command & Control en entornos Windows."
    },
    "03-Nmap_evasion_firewall.md": {
        "categories": ["Recoleccion"],
        "tags": ["nmap", "evasion", "firewall", "reconocimiento"],
        "excerpt": "Técnicas de evasión de firewall con Nmap para realizar reconocimiento sin ser detectado."
    },
    "04-Recoleccion_ingenieria.md": {
        "categories": ["OSINT"],
        "tags": ["osint", "ingenieria-social", "recoleccion"],
        "excerpt": "Recolección de información mediante ingeniería social: técnicas y vectores de ataque humano."
    },
    "05-Recoleccion_WhatsMyName.md": {
        "categories": ["OSINT"],
        "tags": ["osint", "recoleccion", "alias", "whatsmyname"],
        "excerpt": "Uso de WhatsMyName para localizar alias y perfiles de un objetivo en múltiples plataformas."
    },
    "06-Reversing_NoExecute_Bypass.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "nx", "bypass", "exploitdev"],
        "excerpt": "Bypass de la protección No eXecute (NX/DEP) en binarios: teoría y explotación práctica."
    },
    "07-Reversing_ASLR.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "aslr", "bypass", "exploitdev"],
        "excerpt": "Address Space Layout Randomization: funcionamiento y técnicas para su evasión."
    },
    "08-Reversing_Canary.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "stack-canary", "buffer-overflow", "exploitdev"],
        "excerpt": "Stack Canary: análisis de la protección y métodos para bypasearla en binarios vulnerables."
    },
    "09-Reversing_RELRO.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "relro", "got", "exploitdev"],
        "excerpt": "RELRO (Relocation Read-Only): protección de la GOT y técnicas de bypass."
    },
    "10-Reversing_ASLR+NX.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "aslr", "nx", "rop", "exploitdev"],
        "excerpt": "Combinación de ASLR y NX: estrategias ROP y ret2libc para explotar binarios con múltiples protecciones."
    },
    "11-Reversing_printf.md": {
        "categories": ["Reversing"],
        "tags": ["reversing", "format-string", "printf", "exploitdev"],
        "excerpt": "Vulnerabilidades de cadenas de formato con printf: lectura y escritura arbitraria en memoria."
    },
    "12-Enumeracion.md": {
        "categories": ["Recoleccion"],
        "tags": ["enumeracion", "reconocimiento", "servicios", "metodologia"],
        "excerpt": "Enumeración de servicios: metodología y herramientas para mapear la superficie de ataque."
    },
    "13-Explotacion_primera intrusion.md": {
        "categories": ["Explotacion"],
        "tags": ["explotacion", "intrusion", "metodologia", "pentest"],
        "excerpt": "Primera intrusión en un objetivo: fases, herramientas y técnicas de explotación inicial."
    },
    "14-Post_Explotacion_uno.md": {
        "categories": ["Explotacion"],
        "tags": ["post-explotacion", "pentest", "metodologia"],
        "excerpt": "Post-explotación fase 1: consolidación del acceso, reconocimiento interno y movimiento lateral."
    },
    "15-Control_y_matenimiento.md": {
        "categories": ["Explotacion"],
        "tags": ["post-explotacion", "persistencia", "c2", "red-team"],
        "excerpt": "Control y mantenimiento del acceso: técnicas de persistencia y comunicación con el objetivo comprometido."
    },
    "16-recoleccion_info_linux.md": {
        "categories": ["Recoleccion"],
        "tags": ["linux", "reconocimiento", "enumeracion", "recoleccion"],
        "excerpt": "Recolección de información en sistemas Linux: comandos, rutas y datos clave para el atacante."
    },
    "17-recoleccion_info_linux_2.md": {
        "categories": ["Recoleccion"],
        "tags": ["linux", "reconocimiento", "enumeracion", "recoleccion"],
        "excerpt": "Segunda parte de recolección en Linux: profundizando en usuarios, procesos y configuraciones."
    },
    "18-escalada_priv_suggester.md": {
        "categories": ["Privesc"],
        "tags": ["privesc", "windows", "suggester", "escalada"],
        "excerpt": "Escalada de privilegios en Windows usando Suggester: automatización y explotación de misconfigs."
    },
    "19-htb_lame.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "samba", "metasploit"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Lame: explotación de Samba vulnerable con Metasploit en máquina Linux easy."
    },
    "20-htb_shocker.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "shellshock", "web"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Shocker: explotación de la vulnerabilidad Shellshock en CGI."
    },
    "21-htb_bashed.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "webshell", "web"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Bashed: acceso mediante webshell phpbash y escalada de privilegios."
    },
    "22-htb_sense.md": {
        "categories": ["HTB"],
        "tags": ["htb", "freebsd", "easy", "pfsense", "web"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Sense: explotación de pfSense vulnerable en sistema FreeBSD."
    },
    "23-htb_bank.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "web", "upload"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Bank: enumeración web, bypass de restricciones y escalada de privilegios."
    },
    "24-htb_broker.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "activemq", "cve"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Broker: explotación de ActiveMQ (CVE-2023-46604) y escalada con nginx."
    },
    "25-htb_pilgrimage.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "imagemagick", "cve"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Pilgrimage: explotación de ImageMagick y análisis de binarios para privesc."
    },
    "26-htb_wifinetic.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "wifi", "wps"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Wifinetic: ataque a red WiFi con WPS y escalada de privilegios en Linux."
    },
    "27-htb_topology.md": {
        "categories": ["HTB"],
        "tags": ["htb", "linux", "easy", "latex", "injection"],
        "difficulty": "Easy",
        "excerpt": "Walkthrough de HTB Topology: inyección LaTeX para LFI y escalada mediante Gnuplot."
    },
    "28-pentest_pwsh_I.md": {
        "categories": ["Pentest"],
        "tags": ["powershell", "pentest", "windows", "scripting"],
        "excerpt": "Pentesting con PowerShell parte I: fundamentos, bypass de políticas y comandos esenciales."
    },
    "29-pentest_pwsh_II.md": {
        "categories": ["Pentest"],
        "tags": ["powershell", "pentest", "windows", "scripting", "red-team"],
        "excerpt": "Pentesting con PowerShell parte II: técnicas avanzadas, evasión de defensas y automatización."
    },
    "30-lab1_pivoting.md": {
        "categories": ["Lab"],
        "tags": ["lab", "pivoting", "redes", "windows", "red-team"],
        "excerpt": "Laboratorio 1: pivoting y explotación de redes ocultas en entornos Windows con herramientas propias."
    },
    "31-avisolegal.md": {
        "categories": ["Teoria"],
        "tags": ["legal", "aviso-legal", "privacidad"],
        "excerpt": "Aviso legal, política de privacidad y términos de uso del blog Scanthenet."
    },
}

def enrich_frontmatter(filepath, meta):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Detectar si tiene frontmatter
    if not content.startswith('---'):
        print(f"[SKIP] Sin frontmatter: {filepath}")
        return

    # Extraer frontmatter y cuerpo
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"[SKIP] Frontmatter malformado: {filepath}")
        return

    frontmatter = parts[1]
    body = parts[2]

    # Eliminar campos que vamos a reescribir si ya existen
    for key in ['categories', 'tags', 'excerpt', 'difficulty']:
        frontmatter = re.sub(rf'^{key}:.*$', '', frontmatter, flags=re.MULTILINE)
        # Eliminar listas multilinea del campo
        frontmatter = re.sub(rf'^{key}:\s*\n(  -.*\n)*', '', frontmatter, flags=re.MULTILINE)

    # Limpiar líneas vacías extra
    frontmatter = re.sub(r'\n{3,}', '\n\n', frontmatter).strip()

    # Construir nuevos campos
    new_fields = ""
    cats = meta.get('categories', [])
    tags = meta.get('tags', [])
    excerpt = meta.get('excerpt', '')
    difficulty = meta.get('difficulty', '')

    if cats:
        new_fields += f"\ncategories: [{', '.join(cats)}]"
    if tags:
        new_fields += f"\ntags: [{', '.join(tags)}]"
    if difficulty:
        new_fields += f"\ndifficulty: {difficulty}"
    if excerpt:
        new_fields += f"\nexcerpt: \"{excerpt}\""

    new_content = f"---\n{frontmatter}{new_fields}\n---{body}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] {os.path.basename(filepath)}")


if __name__ == "__main__":
    posts_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Procesando posts en: {posts_dir}\n")

    for filename, meta in POST_META.items():
        filepath = os.path.join(posts_dir, filename)
        if os.path.exists(filepath):
            enrich_frontmatter(filepath, meta)
        else:
            print(f"[NOT FOUND] {filename}")

    print("\n✓ Proceso completado.")
