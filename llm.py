from langchain.llms.base import LLM
from transformers import pipeline
from pydantic import Field

class HuggingFaceLLM(LLM):
    # Declare the pipeline as a private field to avoid pydantic errors
    pipe: object = Field(default=None, exclude=True)

    def __init__(self, model_name: str):
        super().__init__()
        self.pipe = pipeline("text-generation", model=model_name, max_length=100)

    def _call(self, prompt: str, stop=None) -> str:
        result = self.pipe(prompt, do_sample=False)
        return result[0]['generated_text']

    @property
    def _identifying_params(self):
        return {"model_name": self.pipe.model.model_name}

    @property
    def _llm_type(self) -> str:
        return "huggingface_llm"
