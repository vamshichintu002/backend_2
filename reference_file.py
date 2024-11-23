import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from typing import Dict, Tuple, Any, List
import openai
import json
import numpy as np

class InvestmentPortfolioAdvisor:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found in .env file")
            
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
            
        # Initialize directories
        self.data_dir = Path("data")
        self.plot_dir = Path("plot")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.plot_dir.mkdir(parents=True, exist_ok=True)

    async def create_client_profile(self, 
                                  risk_tolerance: str,
                                  investment_timeline: str,
                                  financial_goals: List[str],
                                  initial_investment: float) -> Dict:
        """Create a personalized client profile for Indian investors"""
        try:
            system_message = """You are a sophisticated Indian Investment Portfolio Advisor with expertise in:
            1. Indian stock market and mutual funds
            2. Risk assessment and management for Indian investors
            3. Portfolio diversification in Indian context
            4. Indian market analysis and trend identification
            5. Tax-efficient investment planning under Indian tax laws"""
            
            user_message = f"""Create a detailed Indian investment profile with the following parameters:
            - Risk Tolerance: {risk_tolerance}
            - Investment Timeline: {investment_timeline}
            - Financial Goals: {', '.join(financial_goals)}
            - Initial Investment: ₹{initial_investment:,.2f}
            
            Consider Indian market conditions and investment options.
            
            Provide the response in a JSON format with the following structure:
            {{
                "risk_profile": {{
                    "tolerance_level": str,
                    "investment_horizon": str,
                    "risk_capacity": str
                }},
                "investment_objectives": {{
                    "primary_goals": list,
                    "target_return": str,
                    "constraints": list
                }},
                "financial_situation": {{
                    "initial_investment": float,
                    "investment_category": str,
                    "liquidity_needs": str
                }}
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            # Extract and parse the response content
            response_text = response.choices[0].message.content.strip()
            print("\nRaw Response:", response_text)  # Debug print
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print("Response text:", response_text)
                return {
                    "risk_profile": {
                        "tolerance_level": risk_tolerance,
                        "investment_horizon": investment_timeline,
                        "risk_capacity": "moderate"
                    },
                    "investment_objectives": {
                        "primary_goals": financial_goals,
                        "target_return": "10-12% per annum",
                        "constraints": ["Market volatility", "Liquidity needs"]
                    },
                    "financial_situation": {
                        "initial_investment": initial_investment,
                        "investment_category": "Moderate Growth",
                        "liquidity_needs": "Medium"
                    }
                }
            
        except Exception as e:
            print(f"Error creating client profile: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return None

    async def generate_portfolio_recommendation(self, client_profile: Dict) -> Tuple[Dict, str]:
        """Generate personalized portfolio recommendations for Indian market"""
        try:
            system_message = """You are an expert Indian Investment Portfolio Advisor. 
            Provide detailed portfolio recommendations based on Indian market conditions and client profiles.
            Return the response in valid JSON format."""
            
            user_message = f"""Based on the following client profile, provide a detailed Indian market portfolio recommendation:
            
            Client Profile:
            {json.dumps(client_profile, indent=2)}
            
            Include Indian equity, debt, and other investment options like:
            - Large-cap Indian stocks (Nifty 50)
            - Mid-cap and Small-cap stocks
            - Indian Government Bonds
            - Corporate Fixed Deposits
            - Indian Mutual Funds
            - Gold ETFs
            
            Return the response in this exact JSON format:
            {{
                "portfolio": {{
                    "Large_Cap_Stocks": percentage,
                    "Mid_Cap_Stocks": percentage,
                    "Small_Cap_Stocks": percentage,
                    "Government_Bonds": percentage,
                    "Corporate_FDs": percentage,
                    "Mutual_Funds": percentage,
                    "Gold_ETFs": percentage
                }},
                "strategy": "detailed strategy explanation"
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            # Extract and parse the response content
            response_text = response.choices[0].message.content.strip()
            print("\nPortfolio Raw Response:", response_text)  # Debug print
            
            try:
                result = json.loads(response_text)
                return result["portfolio"], result["strategy"]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing portfolio response: {str(e)}")
                # Return default portfolio if parsing fails
                return {
                    "Large_Cap_Stocks": 30,
                    "Mid_Cap_Stocks": 20,
                    "Small_Cap_Stocks": 10,
                    "Government_Bonds": 15,
                    "Corporate_FDs": 10,
                    "Mutual_Funds": 10,
                    "Gold_ETFs": 5
                }, "Balanced portfolio strategy for moderate risk profile"
            
        except Exception as e:
            print(f"Error generating portfolio recommendation: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return None, None

    async def generate_portfolio_visualization(self, portfolio: Dict):
        """Generate portfolio visualization"""
        try:
            # Create pie chart for asset allocation
            plt.figure(figsize=(12, 8))
            plt.pie(
                portfolio.values(), 
                labels=portfolio.keys(), 
                autopct='%1.1f%%',
                colors=plt.cm.Pastel1(np.linspace(0, 1, len(portfolio)))
            )
            plt.title('Recommended Portfolio Allocation', pad=20, size=14)
            plt.legend(
                portfolio.keys(),
                title="Asset Classes",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1)
            )
            
            # Save the visualization
            plt.savefig(
                self.plot_dir / "portfolio_allocation.png",
                bbox_inches='tight',
                dpi=300
            )
            plt.close()
            
        except Exception as e:
            print(f"Error generating portfolio visualization: {str(e)}")

    async def get_market_analysis(self, symbols: List[str]) -> Dict[str, Any]:
        """Get market analysis for Indian stocks"""
        try:
            symbols_str = ", ".join(symbols)
            
            system_message = """You are an Indian financial market analyst. 
            Provide detailed analysis for Indian stock market and specific symbols.
            Return the response in valid JSON format."""
            
            user_message = f"""Provide a market analysis for the following Indian stocks: {symbols_str}
            
            Consider:
            1. Current Indian market trends and sentiment
            2. Sector-specific factors in Indian context
            3. Risk factors including regulatory environment
            4. Growth potential in Indian market
            5. Impact of global markets on these stocks
            
            Return the response in this exact JSON format:
            {{
                "market_trends": {{
                    "nifty50_outlook": "string describing Nifty 50 outlook",
                    "sector_analysis": {{
                        "sector_name": "analysis of the sector",
                        "sector_outlook": "positive/negative/neutral"
                    }},
                    "global_factors": ["factor1", "factor2"]
                }},
                "risk_analysis": {{
                    "market_risks": ["risk1", "risk2"],
                    "regulatory_risks": ["risk1", "risk2"],
                    "company_specific_risks": {{
                        "company_name": ["risk1", "risk2"]
                    }}
                }},
                "growth_potential": {{
                    "short_term": {{
                        "company_name": "outlook"
                    }},
                    "long_term": {{
                        "company_name": "outlook"
                    }},
                    "catalysts": ["catalyst1", "catalyst2"]
                }},
                "recommendations": {{
                    "buy_hold_sell": {{
                        "company_name": "BUY/HOLD/SELL"
                    }},
                    "target_prices": {{
                        "company_name": "price target"
                    }},
                    "investment_horizon": {{
                        "company_name": "short/medium/long term"
                    }}
                }}
            }}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            # Extract and parse the response content
            response_text = response.choices[0].message.content.strip()
            print("\nMarket Analysis Raw Response:", response_text)  # Debug print
            
            try:
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"Error parsing market analysis response: {str(e)}")
                # Return default analysis if parsing fails
                return {
                    "market_trends": {
                        "nifty50_outlook": "Stable with positive bias",
                        "sector_analysis": {
                            "IT": "Stable growth expected",
                            "Banking": "Positive outlook",
                            "Telecom": "Competitive market conditions"
                        },
                        "global_factors": ["Global economic conditions", "FII flows"]
                    },
                    "risk_analysis": {
                        "market_risks": ["Market volatility", "Global uncertainties"],
                        "regulatory_risks": ["Policy changes", "Compliance requirements"],
                        "company_specific_risks": {
                            stock: ["Competition", "Market share"] for stock in symbols
                        }
                    },
                    "growth_potential": {
                        "short_term": {stock: "Moderate growth" for stock in symbols},
                        "long_term": {stock: "Positive outlook" for stock in symbols},
                        "catalysts": ["Digital transformation", "Economic recovery"]
                    },
                    "recommendations": {
                        "buy_hold_sell": {stock: "HOLD" for stock in symbols},
                        "target_prices": {stock: "NA" for stock in symbols},
                        "investment_horizon": {stock: "Long term" for stock in symbols}
                    }
                }
            
        except Exception as e:
            print(f"Error getting market analysis: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            return None