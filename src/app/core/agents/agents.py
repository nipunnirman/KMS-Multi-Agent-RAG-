"""Agent implementations for the multi-agent RAG flow.

This module defines thin node functions that execute logic directly using OpenAI client
to avoid LangChain's SecretStr handling issues in uvicorn environment.
"""

from typing import List, Tuple
import os

import openai
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage

from ..config import Settings
from .prompts import (
    RETRIEVAL_SYSTEM_PROMPT,
    SUMMARIZATION_SYSTEM_PROMPT,
    VERIFICATION_SYSTEM_PROMPT,
)
from .state import QAState
from .tools import retrieval_tool


def _extract_last_ai_content(messages: List[BaseMessage]) -> str:
    """Extract the content of the last AIMessage in a messages list."""
    if messages and isinstance(messages[-1], AIMessage):
        return str(messages[-1].content)
    return ""


def retrieval_node(state: QAState) -> QAState:
    """Retrieval Node: gathers context from vector store directly.

    This node:
    - Calling the retrieval tool directly with the user's question.
    - Stores the consolidated context string in `state["context"]`.
    """
    question = state["question"]
    
    # Directly invoke the tool
    try:
        tool_output = retrieval_tool.invoke(question)
        
        # Handle different output formats based on langchain version
        if isinstance(tool_output, tuple) and len(tool_output) == 2:
            context, artifact = tool_output
            citations = artifact.get("citations", {}) if isinstance(artifact, dict) else {}
        else:
            # Fallback if it returns just content
            context = str(tool_output)
            citations = {}

        return {
            "context": context,
            "citations": citations,
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        # In case of tool error, return empty context
        return {"context": "", "citations": {}}


def summarization_node(state: QAState) -> QAState:
    """Summarization Node: generates draft answer from context using OpenAI directly.

    This node:
    - Constructs a prompt with system instructions and user content.
    - Invokes OpenAI API directly.
    - Stores the draft answer in `state["draft_answer"]`.
    """
    question = state["question"]
    context = state.get("context")

    user_content = f"Question: {question}\n\nContext:\n{context}"
    
    # Instantiate Settings directly
    settings = Settings()
    # Force strip key if needed
    api_key = settings.openai_api_key.strip() if settings.openai_api_key else ""
    client = openai.Client(api_key=api_key)
    
    response = client.chat.completions.create(
        model=settings.openai_model_name,
        messages=[
            {"role": "system", "content": SUMMARIZATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.0
    )
    
    draft_answer = response.choices[0].message.content

    return {
        "draft_answer": str(draft_answer),
    }


def verification_node(state: QAState) -> QAState:
    """Verification Node: verifies and corrects the draft answer using OpenAI directly.

    This node:
    - Constructs a prompt with verification instructions.
    - Invokes OpenAI API directly.
    - Stores the final verified answer in `state["answer"]`.
    """
    question = state["question"]
    context = state.get("context", "")
    draft_answer = state.get("draft_answer", "")

    user_content = f"""Question: {question}

Context:
{context}

Draft Answer:
{draft_answer}

Please verify and correct the draft answer, removing any unsupported claims."""

    # Instantiate Settings directly
    settings = Settings()
    api_key = settings.openai_api_key.strip() if settings.openai_api_key else ""
    
    client = openai.Client(api_key=api_key)

    response = client.chat.completions.create(
        model=settings.openai_model_name,
        messages=[
            {"role": "system", "content": VERIFICATION_SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.0
    )
    
    answer = response.choices[0].message.content

    return {
        "answer": str(answer),
    }
