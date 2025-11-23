from google import genai
from typing import List
import time


class RateLimitError(Exception):
    """Eccezione per rate limit raggiunto"""
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Rate limit raggiunto. Riprova tra {retry_after} secondi.")


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
    
    MAX_REQUESTS_PER_MINUTE = 15
    RATE_LIMIT_WINDOW = 60  # seconds
    
    def __init__(self, api_key: str, model_name: str = "gemma-3-27b-it"):
        self.api_key = api_key
        self.model_name = model_name
        
        self.client = genai.Client(api_key=api_key)
        
        self.generation_config = {
            "temperature": 0.8,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 30,
        }
        
        self._request_timestamps = []
    
    def _check_rate_limit(self):
        """
        Verifica se possiamo fare una richiesta senza superare il rate limit
        
        Raises:
            RateLimitError: Se il rate limit è stato raggiunto
        """
        now = time.time()
        
        self._request_timestamps = [
            ts for ts in self._request_timestamps 
            if now - ts < self.RATE_LIMIT_WINDOW
        ]
        
        if len(self._request_timestamps) >= self.MAX_REQUESTS_PER_MINUTE:
            oldest = self._request_timestamps[0]
            retry_after = int(self.RATE_LIMIT_WINDOW - (now - oldest)) + 1
            raise RateLimitError(retry_after)
        
        self._request_timestamps.append(now)
    
    def generate_word(self, parola_segreta: str, sequenza: List[str]) -> str:
        self._check_rate_limit()
        
        prompt = self._build_prompt(parola_segreta, sequenza)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.generation_config
            )
            
            raw_text = response.text
            cleaned_word = self._validate_response(raw_text)
            
            return cleaned_word
            
        except RateLimitError:
            raise
        except Exception as e:
            error_msg = str(e).lower()
            if "rate limit" in error_msg or "quota" in error_msg or "429" in error_msg:
                raise RateLimitError(60)
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
