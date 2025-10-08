from .pdf_rag import PDFRAGAgent
from .web_Search import WebSearchAgent
from .arxiv_agent import ArxivAgent
from .decision_agent import Decisionagent
from .ans_synthesizer import answer_synthesizer

class Controller:
    def __init__(self):
        self.pdf_agent = PDFRAGAgent()
        self.web_agent = WebSearchAgent()
        self.arxiv_agent = ArxivAgent()
        self.decision_agent = Decisionagent()
        self.answer_synthesizer = answer_synthesizer()
        
    def decide(self, query, file_ids):
        return self.decision_agent.decide(query, file_ids)

    def handle_query(self, query, file_ids, filename):
        decision = self.decide(query, file_ids)
        snippets = []

        if "pdf" in decision['agents'] and filename:
            pdf_res = self.pdf_agent.query(query, filename)
            snippets.extend(pdf_res["snippets"])
            
        if "arxiv" in decision["agents"]:
            arxiv_res = self.arxiv_agent.query(query)
            snippets.extend([{"text": s} for s in arxiv_res["summaries"]])
            
        if "web" in decision["agents"]:
            web_res = self.web_agent.search(query)
            snippets.extend(web_res["snippets"])
            
        final_answer = self.answer_synthesizer.synsthsizer(query, snippets)
            
        return {
            "decision": decision,
            "snippets": snippets,
            "final_answer": final_answer
        }
