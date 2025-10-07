import requests
from xml.etree import ElementTree as ET 

class ArxivAgent:
    def query(self,q: str, max_results: int =5):
        params = {"search_query":q,"start":0,"max_result":max_results}
        r = requests.get("http://export.arxiv.org/api/query",params=params, timeout=10)
        
        
        
        entries, summaries = [],[]
        root = ET.fromstring(r.text)
        ns = {'atom':'http://www.w3.org/2005/Atom'}
        
        
        for entry in root.findall('atom:entry',ns)[:max_results]:
            title =  entry.find('atom:title',ns).text.strip()
            summary = entry.find('atom:summary',ns).text.strip()
            link = next((ln.attrib.get('href') for ln in entry.findall('atom:link',ns) 
                         if ln.attrib.get('type') == 'application/pdf'),None)
            entries.append({'title':title,"summary":summary,"pdf":link})
            summaries.append(summary)
            
            
        return {'entries':entries,"summaries":summaries}