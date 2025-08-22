from fastapi import FastAPI, Query
from app.services.tree_service import scrape_tree
from app.schemas.response import TreeResponse

app = FastAPI(title="DOM Tree Extractor API", version="1.0.0")

@app.get("/scrape", response_model=TreeResponse)
def scrape(url: str = Query(..., description="Target website URL")):
    """
    Scrape and return the DOM tree of a given webpage.
    """
    try:
        result = scrape_tree(url)
        return result
    except Exception as e:
        return {"url": url, "clicked": 0, "tree": [], "error": str(e)}
