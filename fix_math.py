import re

with open('sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md', 'r') as f:
    content = f.read()

def replace_math(match):
    # If it's already a double dollar, don't change it
    if match.group(0).startswith('$$'):
        return match.group(0)
    # If it's a single dollar, replace with double dollar
    inner = match.group(1)
    return '$$' + inner + '$$'

# Regex to match either $$...$$ or $...$
# We match $$...$$ first so we can ignore it
new_content = re.sub(r'(\$\$[^$]+\$\$)|(?<!\$)\$([^$]+)\$(?!\$)', 
                     lambda m: m.group(1) if m.group(1) else '$$' + m.group(2) + '$$', 
                     content)

with open('sections/science/_posts/2026-04-28-Skip-connections-and-graph-analysis.md.new', 'w') as f:
    f.write(new_content)

print(f"Replaced {content.count('$')} dollars with new dollars.")
