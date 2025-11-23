from google import genai
from typing import List


class AIClient:
    PROMPT_TEMPLATE = """
Stai giocando a Intesa Vincente con Giocatore 1 e Giocatore 2.
Tu e Giocatore 2 dovete fare indovinare la parola segreta al Giocatore 1
componendo una frase indizio parola per parola alternando i turni.
Puoi usare qualsiasi parola italiana. Non puoi usare la parola segreta, né i suoi derivati. Non aggiungere formattazioni.

Esempi:
- Se la parola segreta è "pizza" e la sequenza è ["cibo"], puoi rispondere con "italiano".
- Se la parola segreta è "mago" e la sequenza è ["uomo", "con", "poteri"], puoi rispondere con "magici".
- Se la parola segreta è "computer" e la sequenza è ["strumento", "per"], puoi rispondere con "lavorare".
- Se la parola segreta è "calcio" e la sequenza è ["sport", "più"], puoi rispondere con "popolare".
- Se la parola segreta è "mucca" e la sequenza è ["sinonimo", "di"], puoi rispondere con "vacca".
- Se la parola segreta è "puntura" e la sequenza è ["cosa", "ti", "fa", "una"], puoi rispondere con "zanzara".
- Se la parola segreta è "single" e la sequenza è ["non", "sposato", "né"], puoi rispondere con "fidanzato".

Esempi negativi:
Non produrre sequenze agrammaticali come ["il", "dell'"]
Non produrre sequenze agrammaticali come ["colui", "che", "indossare"]

La parola segreta è [{parola_segreta}] e la sequenza già generata è [{sequenza}], 
genera una sola parola grammaticalmente coerente con la sequenza per continuarla. 
Attenzione, non restituirmi la sequenza aggiornata ma soltanto la parola che hai scelto.
Genera adesso la parola successiva per la sequenza corrente.
"""
    
    def __init__(self, api_key: str, model_name: str = "gemma-3-27b-it"):
        self.api_key = api_key
        self.model_name = model_name
        
        genai.configure(api_key=api_key)
        
        generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 30,
        }
        
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config
        )
    
    def generate_word(self, parola_segreta: str, sequenza: List[str]) -> str:
        prompt = self._build_prompt(parola_segreta, sequenza)
        
        try:
            response = self.model.generate_content(prompt)
            
            raw_text = response.text
            cleaned_word = self._validate_response(raw_text)
            
            return cleaned_word
            
        except Exception as e:
            raise Exception(f"Errore nella chiamata a Gemma API: {str(e)}")
    
    def _build_prompt(self, parola_segreta: str, sequenza: List[str]) -> str:
        sequenza_str = ", ".join(f'"{word}"' for word in sequenza) if sequenza else "vuota"
        
        prompt = self.PROMPT_TEMPLATE.format(
            parola_segreta=parola_segreta,
            sequenza=sequenza_str
        )
        
        return prompt
    
    def _validate_response(self, response: str) -> str:
        cleaned = response.strip()
        
        cleaned = cleaned.rstrip('.,!?;:')
        
        if ' ' in cleaned:
            cleaned = cleaned.split()[0]
        
        cleaned = cleaned.strip('"\'')
        
        cleaned = cleaned.lower()
        
        return cleaned
    
    def test_connection(self) -> bool:
        try:
            response = self.model.generate_content("Rispondi solo con: OK")
            return len(response.text) > 0
        except Exception:
            return False


if __name__ == "__main__":
    API_KEY = "your-api-key-here"
    
    client = GeminiClient(api_key=API_KEY)
    
    if client.test_connection():
        print("Connessione OK")
        
        parola_segreta = "pizza"
        sequenza = ["cibo"]
        
        try:
            parola = client.generate_word(parola_segreta, sequenza)
            print(f"Parola segreta: {parola_segreta}")
            print(f"Sequenza: {sequenza}")
            print(f"Parola generata: {parola}")
        except Exception as e:
            print(f"Errore: {e}")
    else:
        print("Connessione fallita")
