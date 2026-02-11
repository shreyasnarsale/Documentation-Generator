
import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

try:
    from services.llm_service import get_llm
    from langchain_core.messages import HumanMessage
    
    print("Testing LLM connection...")
    llm = get_llm()
    print(f"LLM initialized with model: {llm.model}")
    
    # Simple test invocation
    response = llm.invoke([HumanMessage(content="Hello, are you working?")])
    print("Response received:")
    print(response.content)
    print("\nSUCCESS: LLM is working correctly.")
    
except Exception as e:
    print(f"\nERROR: {e}")
    sys.exit(1)
