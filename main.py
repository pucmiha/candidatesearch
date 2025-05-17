from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load candidate data
DF = pd.read_csv('blue_collar_candidates.csv')
LOCATIONS = sorted(DF['location'].unique().tolist())

# Prepare vector search for job roles
_vectorizer = TfidfVectorizer(stop_words='english')
_job_matrix = _vectorizer.fit_transform(DF['job_position'])


def search_candidates(role: str = "", location: str = ""):
    df = DF
    if location:
        df = df[df['location'] == location]
    if role:
        query_vec = _vectorizer.transform([role])
        sims = cosine_similarity(query_vec, _job_matrix[df.index]).flatten()
        df = df.assign(similarity=sims)
        df = df[df['similarity'] > 0].sort_values('similarity', ascending=False)
    return df


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    candidates = search_candidates().to_dict('records')
    return templates.TemplateResponse("index.html", {
        "request": request,
        "locations": LOCATIONS,
        "candidates": candidates
    })


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, role: str = "", location: str = ""):
    candidates = search_candidates(role, location).to_dict('records')
    return templates.TemplateResponse("results.html", {
        "request": request,
        "candidates": candidates
    })
