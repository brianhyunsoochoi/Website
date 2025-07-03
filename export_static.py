import os
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from load_posts import fetch_all_articles

# Directories
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
POST_ASSETS_DIR = BASE_DIR / 'post_assets'
OUTPUT_DIR = BASE_DIR / 'static_site'

# Prepare output directory
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Set up Jinja2
env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))

def url_for_static(name, path=None):
    # Handle static and post_assets
    if name == 'static' and path:
        return f'static/{path}'
    if name == 'post_assets' and path:
        return f'post_assets/{path}'
    # Handle route names
    if name == 'home':
        return 'index.html'
    # Add more routes as needed
    return '#'

env.globals['url_for'] = url_for_static

# Fetch all articles
all_articles = fetch_all_articles()

# 1. Export home page
home_template = env.get_template('home.html')
posts = [a.to_dir() for a in all_articles]
home_html = home_template.render(id='static', posts=posts)
with open(OUTPUT_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(home_html)

# 2. Export each blog post
base_template = env.get_template('base.html')
for article in all_articles:
    slug = article.slug if hasattr(article, 'slug') else article.to_dir()
    post_dir = POST_ASSETS_DIR / slug
    if not post_dir.exists():
        continue
    md_files = [f for f in os.listdir(post_dir) if f.endswith('article.md')]
    if not md_files:
        continue
    md_path = post_dir / md_files[0]
    md_content = md_path.read_text(encoding='utf-8')
    html_content = markdown(md_content)
    rendered = base_template.render(request=None, content=html_content)
    out_path = OUTPUT_DIR / f'{slug}.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(rendered)

# 3. Copy static assets
shutil.copytree(STATIC_DIR, OUTPUT_DIR / 'static')
if POST_ASSETS_DIR.exists():
    shutil.copytree(POST_ASSETS_DIR, OUTPUT_DIR / 'post_assets')

print(f"Static site exported to '{OUTPUT_DIR}/'")
