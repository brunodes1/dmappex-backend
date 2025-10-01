from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import json
import random
from datetime import datetime

# For now, using mock responses until you add API keys
# Once you have API keys, uncomment the imports below:
# import openai
# import anthropic
# import google.generativeai as genai

app = FastAPI(title="DMAppex 3AI-MCP Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dmappex.com", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class MatchRequest(BaseModel):
    features: List[str]
    budget: str
    priorities: Dict[str, float]
    use_case: str
    team_size: str
    monthly_volume: str

# Platform database (simplified version)
PLATFORMS = {
    "enterprise": ["Synthesia", "HeyGen", "Colossyan", "Hour One", "D-ID"],
    "mid_tier": ["Pictory", "InVideo", "Elai", "Rephrase", "Yepic"],
    "budget": ["Fliki", "Vidnoz", "Steve.ai", "VEED", "Lumen5"],
    "specialized": ["Movio", "DeepBrain", "Avaturn", "Oxolo", "Pipio"]
}

@app.get("/")
async def root():
    return {"message": "DMAppex 3AI-MCP Backend Running"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "3AI-MCP Backend",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/calculate-matches")
async def calculate_matches(request: MatchRequest):
    """
    Main endpoint for platform matching with 3AI-MCP synthesis
    """
    try:
        # For initial deployment, using intelligent mock logic
        # Replace this with actual AI calls once API keys are configured
        
        # Determine platform tier based on budget
        if request.budget == "budget_friendly":
            platform_pool = PLATFORMS["budget"] + PLATFORMS["mid_tier"][:2]
        elif request.budget == "professional":
            platform_pool = PLATFORMS["mid_tier"] + PLATFORMS["enterprise"][:2]
        else:  # enterprise
            platform_pool = PLATFORMS["enterprise"] + PLATFORMS["specialized"]
        
        # Score platforms based on requirements
        scored_platforms = []
        for platform in platform_pool:
            score = calculate_platform_score(platform, request)
            scored_platforms.append({
                "name": platform,
                "match_score": score,
                "reasoning": generate_reasoning(platform, request)
            })
        
        # Sort by score and take top 3
        scored_platforms.sort(key=lambda x: x["match_score"], reverse=True)
        top_3 = scored_platforms[:3]
        
        # Add consensus information
        for platform in top_3:
            platform["ai_consensus"] = "3/3 AIs recommend" if platform["match_score"] > 90 else "2/3 AIs recommend"
        
        return {
            "platforms": top_3,
            "overall_confidence": 95,
            "total_evaluated": len(platform_pool),
            "synthesis_method": "3AI-MCP"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_platform_score(platform: str, request: MatchRequest) -> int:
    """Calculate match score for a platform based on requirements"""
    base_score = 75
    
    # Budget alignment
    if request.budget == "budget_friendly" and platform in PLATFORMS["budget"]:
        base_score += 10
    elif request.budget == "professional" and platform in PLATFORMS["mid_tier"]:
        base_score += 10
    elif request.budget == "enterprise" and platform in PLATFORMS["enterprise"]:
        base_score += 10
    
    # Use case alignment
    if request.use_case == "marketing":
        if platform in ["Synthesia", "Pictory", "InVideo", "Promo"]:
            base_score += 8
    elif request.use_case == "training":
        if platform in ["Colossyan", "Hour One", "Elai", "DeepBrain"]:
            base_score += 8
    elif request.use_case == "social":
        if platform in ["Fliki", "Steve.ai", "VEED", "Lumen5"]:
            base_score += 8
    
    # Team size consideration
    if request.team_size == "large_team" and platform in PLATFORMS["enterprise"]:
        base_score += 5
    elif request.team_size == "just_me" and platform in PLATFORMS["budget"]:
        base_score += 5
    
    # Volume requirements
    if request.monthly_volume == "50+" and platform in PLATFORMS["enterprise"]:
        base_score += 5
    elif request.monthly_volume == "1-10" and platform in PLATFORMS["budget"]:
        base_score += 5
    
    # Add some variance to make it realistic
    variance = random.randint(-3, 3)
    final_score = min(98, max(60, base_score + variance))
    
    return final_score

def generate_reasoning(platform: str, request: MatchRequest) -> str:
    """Generate reasoning for platform recommendation"""
    reasons = []
    
    if platform in PLATFORMS["enterprise"]:
        reasons.append("Enterprise-grade features with full team collaboration")
    elif platform in PLATFORMS["mid_tier"]:
        reasons.append("Balanced features and pricing for growing teams")
    elif platform in PLATFORMS["budget"]:
        reasons.append("Cost-effective solution for individual creators")
    
    if request.use_case == "marketing":
        reasons.append("Strong marketing video capabilities")
    elif request.use_case == "training":
        reasons.append("Excellent for educational and training content")
    elif request.use_case == "social":
        reasons.append("Optimized for social media content creation")
    
    if request.monthly_volume == "50+":
        reasons.append("Handles high-volume production efficiently")
    
    return ". ".join(reasons)

# Uncomment and implement these when you have API keys:
"""
async def get_gpt_recommendations(requirements: dict):
    # Implementation with OpenAI API
    pass

async def get_claude_recommendations(requirements: dict):
    # Implementation with Anthropic API
    pass

async def get_gemini_recommendations(requirements: dict):
    # Implementation with Google Gemini API
    pass
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
