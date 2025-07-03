from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from markdown import markdown
from load_posts import fetch_all_articles, MarkdownArticle
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/post_assets", StaticFiles(directory="post_assets"), name="post_assets")
templates = Jinja2Templates(directory="templates")

all_articles = fetch_all_articles()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    posts = [a.to_dir() for a in all_articles]
    return templates.TemplateResponse(
        request=request, name="home.html", 
        context={
            "id": id, 
            "posts": posts
            }
    )

@app.get("/posts/{slug}", response_class=HTMLResponse)
def read_blog(request: Request, slug: str):
    print("READING BLOG")
    files = os.listdir(os.path.join("post_assets", slug))
    md_path = [f for f in files if str(f).endswith("article.md")][0]
    md_path = Path(os.path.join("post_assets", slug, md_path))
    print(md_path.absolute)
    if not md_path.exists():
        return HTMLResponse("Post not found", status_code=404)
    
    md_content = md_path.read_text()
    html_content = markdown(md_content)
    
    return templates.TemplateResponse("base.html", {
        "request": request,
        "content": html_content
    })
