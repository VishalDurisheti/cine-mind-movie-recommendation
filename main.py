from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from chatbot_logic import recommend_from_query


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="Movie Recommendation API",
    description="AI-powered movie recommendation system",
    version="1.0.0"
)


# ==========================================
# FRONTEND FILES
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ==========================================
# REQUEST MODEL
# ==========================================

class RecommendationRequest(BaseModel):

    query: str


# ==========================================
# HOME PAGE
# ==========================================

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
# ==========================================
# RECOMMENDATION API
# ==========================================

@app.post("/recommend")
def recommend(request: RecommendationRequest):

    recommendations = recommend_from_query(
        request.query
    )

    return {
        "query": request.query,
        "recommendations": recommendations.to_dict(
            orient="records"
        )
    }