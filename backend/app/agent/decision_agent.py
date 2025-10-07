import os 
import google.generativeai as genai
import json

class Decisionagent:
    def __init__(self):
        api_key = os.getenv('GEMINI_KEY')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        
    def decide(self,query: str, file_ids: str =None):
        system_prompt = """You are a decision-making agent for a multi-agent system.
Based on the user's query, decide which agents are best suited:
- 'pdf' → when the user uploaded a document or asks something about their file.
- 'web' → for latest news, general knowledge, or current events.
- 'arxiv' → for research-oriented, academic, or scientific paper queries.

Respond only in strict JSON format:
{
  "agents": ["pdf" or "web" or "arxiv"],
  "rationale": "short explanation why"
}"""

        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nUser query :{query}"
            )
            
            decision = json.load(response.text)
            return decision
        
                
        except Exception as e:
            print("Decision Agent Error")
            
            q =  query.lower()
            agents , rational = [],[]
            if file_ids:
                agents.append("pdf")
                rational.append("user provided a documnet")
                
                
            if any (k in q for k in ['paper','research','study','arxiv']):
                agents.append('arxiv')
                rational.append('reserach-related query')
                
                
            if any (k in q for k in ['latest','news','update','recent']):
                agents.append('web')
                rational.append('latest info pr event event-based query')
            
            if not agents:
                agents.append('web')
                rational.append("default to web search.")
            return {"agents":agents, "rationale":"|".join(rational)}
