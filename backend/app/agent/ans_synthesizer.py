import os
import google.generativeai as genai

class answer_synthesizer:
    def __init__(self):
        api_key = os.getenv("GEMINI_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")
        
        
    def synsthsizer(self, query: str, snippets:list):
        
        if not [snippets]:
            return "No relevant info found"
        
        combine_text = "\n\n".join(s['text'] for s in snippets if "text" in s)
        
        prompt = f"""
        You are an AI assistant that synthesizes information from multiple sources.
        The following are snippets collected from different agents (PDF, Web, Arxiv).

        User query:
        {query}

        Snippets:
        {combine_text}

        Please write a clear, concise, and accurate answer in natural language.
        Avoid repeating the same facts, remove redundancy, and maintain factual correctness.
        """
        
        try:
            response=  self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print("answer_synthesizer Error")
            return "I am sorry I could not synthesize th answer "