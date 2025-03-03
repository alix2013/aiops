from typing import Any
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import  LLMResult
import sys
class CustStreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self):
        self.tokens = []
        self.finish = False

    def on_llm_new_token(self, token: str, **kwargs):
        # print(token, end="")
        sys.stdout.write(token)
        sys.stdout.flush()
        self.tokens.append(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.finish = 1

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        print("get errors in CustStreamHandler",str(error))
        self.tokens.append(str(error))

    def generate_tokens(self):
        while not self.finish or self.tokens:
            if self.tokens:
                data = self.tokens.pop(0)
                yield data
            else:
                pass


