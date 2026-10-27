"""Single place for Gemini access: model name, client and JSON generation.

All services call generate_json / generate_text instead of talking to the SDK
directly, so the model is configured once (MODEL_NAME in .env) and every
structured response is validated against a Pydantic schema.
"""
import os
import re
import time
from typing import TypeVar

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

load_dotenv()

DEFAULT_MODEL = "gemini-flash-lite-latest"
MODEL_NAME = os.getenv("MODEL_NAME") or DEFAULT_MODEL

T = TypeVar("T", bound=BaseModel)

_client = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def _strip_code_fences(text: str) -> str:
    return re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE).strip()


def _is_rate_limit_error(e: Exception) -> bool:
    msg = str(e).lower()
    return "429" in msg or "resource_exhausted" in msg or "quota" in msg


def generate_text(prompt: str, temperature: float = 0.0) -> str:
    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(temperature=temperature),
    )
    return response.text or ""


def generate_json(prompt: str, schema: type[T], max_retries: int = 3) -> T:
    """Ask Gemini for JSON and validate it against `schema`.

    JSON mode makes the model return syntactically valid JSON; Pydantic then
    checks the structure. Malformed or invalid output is retried, rate limits
    are retried with a growing wait, and any other error is raised at once.
    """
    config = types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        max_output_tokens=4096,
        response_mime_type="application/json",
    )
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            response = get_client().models.generate_content(
                model=MODEL_NAME, contents=prompt, config=config
            )
            if not response.text:
                raise ValueError("Empty response from Gemini")
            return schema.model_validate_json(_strip_code_fences(response.text))

        except (ValidationError, ValueError) as e:
            last_error = e
            print(f"    Invalid model output (attempt {attempt}/{max_retries}): {str(e).splitlines()[0]}")

        except Exception as e:
            if not _is_rate_limit_error(e):
                raise
            last_error = e
            if attempt < max_retries:
                wait = 15 * attempt
                print(f"    Rate limited, waiting {wait}s before retry ({attempt}/{max_retries})...")
                time.sleep(wait)

    raise RuntimeError(f"Gemini did not return valid output after {max_retries} attempts: {last_error}")
