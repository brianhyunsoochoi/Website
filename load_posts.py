import os
import yaml

class MarkdownArticle:
    def __init__(self, slug, title, cover_img, content, metadata):
        self.slug = slug
        self.title = title
        self.cover_img = cover_img
        self.content = content  # Markdown content as a string
        self.metadata = metadata  # Dict with additional YAML metadata

    @classmethod
    def from_post_dir(cls, post_dir):
        # Load YAML metadata
        yaml_files = [f for f in os.listdir(post_dir) if f.endswith("yaml")]
        metadata = {}
        for yf in yaml_files:
            with open(os.path.join(post_dir, yf), "r") as f:
                data = yaml.load(f, Loader=yaml.SafeLoader)
                if data:
                    metadata.update(data)

        # Load markdown content (assume first .md file is main content)
        md_files = [f for f in os.listdir(post_dir) if f.endswith("md")]
        content = ""
        if md_files:
            with open(os.path.join(post_dir, md_files[0]), "r") as f:
                content = f.read()

        slug = os.path.basename(post_dir)
        title = metadata.get("title", slug)
        cover_img = metadata.get("cover_img", "")

        return cls(slug, title, cover_img, content, metadata)
    
    def to_dir(self):
        return self.metadata

def fetch_all_articles():
    # load all files and filter to only directories
    all_posts = os.listdir("post_assets") 
    all_posts = [d for d in all_posts if os.path.isdir(os.path.join("post_assets", d))]

    # instantiate the articles
    articles = []
    for curr_post in all_posts:
        curr_article = MarkdownArticle.from_post_dir(os.path.join("post_assets", curr_post))
        articles.append(curr_article)
    
    return articles
