from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from reference_file import InvestmentPortfolioAdvisor
import uvicorn

app = FastAPI(
    title="Investment Portfolio Advisor API",
    description="API for generating personalized investment portfolio recommendations for Indian investors",
    version="1.0.0"
)

# Initialize the advisor
advisor = InvestmentPortfolioAdvisor()

class ClientProfileRequest(BaseModel):
    risk_tolerance: str
    investment_timeline: str
    financial_goals: List[str]
    initial_investment: float

@app.post("/create-profile")
async def create_profile(profile_request: ClientProfileRequest):
    """Create a personalized client investment profile"""
    try:
        profile = await advisor.create_client_profile(
            risk_tolerance=profile_request.risk_tolerance,
            investment_timeline=profile_request.investment_timeline,
            financial_goals=profile_request.financial_goals,
            initial_investment=profile_request.initial_investment
        )
        if profile is None:
            raise HTTPException(status_code=500, detail="Failed to create client profile")
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-portfolio")
async def generate_portfolio(profile_request: ClientProfileRequest):
    """Generate portfolio recommendations based on client profile"""
    try:
        # First create the profile
        profile = await advisor.create_client_profile(
            risk_tolerance=profile_request.risk_tolerance,
            investment_timeline=profile_request.investment_timeline,
            financial_goals=profile_request.financial_goals,
            initial_investment=profile_request.initial_investment
        )
        
        if profile is None:
            raise HTTPException(status_code=500, detail="Failed to create client profile")
        
        # Generate portfolio recommendation
        portfolio, strategy = await advisor.generate_portfolio_recommendation(profile)
        if portfolio is None:
            raise HTTPException(status_code=500, detail="Failed to generate portfolio recommendation")
        
        # Generate visualization
        await advisor.generate_portfolio_visualization(portfolio)
        
        return {
            "portfolio": portfolio,
            "strategy": strategy,
            "visualization_path": "plot/portfolio_allocation.png"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
