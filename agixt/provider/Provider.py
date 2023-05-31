from threading import Thread
from concurrent.futures import Future

def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future

    return wrapper

class Provider:

    def __init__(
        self,
        AI_PROVIDER_URI: str = "",
        API_KEY: str = "",
        MAX_TOKENS: int = 2000,
        AI_TEMPERATURE: float = 0.7,
        AI_MODEL: str = "",
        **kwargs,
    ):
        self.requirements = []
        self.AI_PROVIDER_URI = AI_PROVIDER_URI
        self.MAX_TOKENS = MAX_TOKENS
        self.AI_TEMPERATURE = AI_TEMPERATURE
        self.AI_MODEL = AI_MODEL
        self.API_KEY = API_KEY
        
    def instruct(self, prompt, tokens):
        return run(prompt,tokens)
        
    @threaded
    def run(self, prompt, tokens):
        pass
    
