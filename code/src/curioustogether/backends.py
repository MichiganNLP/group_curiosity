from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class GenerationBackend(Protocol):
    def generate(self, prompt: str) -> str:
        """Return one model continuation for a complete prompt."""


@dataclass
class DryRunBackend:
    """Deterministic backend for testing the pipeline without model weights."""

    response: str = "dry-run response"

    def generate(self, prompt: str) -> str:
        last_instruction = next(
            (line for line in reversed(prompt.splitlines()) if line.strip()),
            "respond",
        )
        return f"[DRY RUN] {self.response}: {last_instruction[:120]}"


class TransformersBackend:
    """Minimal local Hugging Face causal-language-model backend."""

    def __init__(
        self,
        model_name: str,
        max_new_tokens: int = 192,
        temperature: float = 0.7,
        seed: int = 0,
        device_map: str = "auto",
    ) -> None:
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "Install the model extras with: pip install -e '.[models]'"
            ) from exc

        torch.manual_seed(seed)
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype="auto",
        )
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

    def generate(self, prompt: str) -> str:
        tokenizer = self.tokenizer
        messages = [{"role": "user", "content": prompt}]
        if getattr(tokenizer, "chat_template", None):
            rendered = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        else:
            rendered = prompt
        inputs = tokenizer(rendered, return_tensors="pt").to(self.model.device)
        do_sample = self.temperature > 0
        with self.torch.inference_mode():
            generated = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=do_sample,
                temperature=self.temperature if do_sample else None,
                pad_token_id=tokenizer.eos_token_id,
            )
        continuation = generated[0, inputs["input_ids"].shape[1] :]
        return tokenizer.decode(continuation, skip_special_tokens=True).strip()
