from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
# Note: We no longer need LLMChain; we use the | (pipe) operator now

class TestCaseGenerator:
    """Generate test cases using local LLM"""
    
    def __init__(self, model_name="llama3.2:3b"):
        """Initialize with Ollama model"""
        self.llm = Ollama(model=model_name, temperature=0.7)
        self.prompt_template = self._create_prompt_template()
    
    def _create_prompt_template(self):
        """Create structured prompt for test case generation"""
        template = """You are an expert QA engineer. Based on the following requirements/documentation, generate comprehensive test cases.

REQUIREMENTS:
{requirements}

Generate test cases in the following format:

TEST CASE ID: TC-001
TITLE: [Clear test case title]
DESCRIPTION: [What this test verifies]
PRECONDITIONS: [What needs to be set up before testing]
TEST STEPS:
1. [Step 1]
2. [Step 2]
EXPECTED RESULT: [What should happen]
PRIORITY: [High/Medium/Low]

TEST CASES:
"""
        return PromptTemplate(template=template, input_variables=["requirements"])
    
    def generate_test_cases(self, requirements_text):
        """Generate test cases from requirements using LCEL (|)"""
        # Modern LangChain syntax: Prompt | LLM
        chain = self.prompt_template | self.llm
        result = chain.invoke({"requirements": requirements_text})
        return result
    
    def generate_from_prompt(self, custom_prompt):
        """Generate test cases from custom prompt"""
        # Simple direct invocation
        response = self.llm.invoke(custom_prompt)
        return response