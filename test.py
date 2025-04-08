from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyCtiLCXnw7OADRhGjqL5bBRko8hk8VGgps"  # Replace with your actual API key

# Initialize LangChain Gemini Model
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY)

# Input values for testing
title = "AI-Powered Recipe App"
purpose = "To revolutionize the food industry by creating a personalized recipe app."
funding = "$47,000"

# Create a structured prompt to avoid any formatting like stars
prompt = ChatPromptTemplate.from_template(
    """Generate a project funding proposal with the following details:
    - Title: {title}
    - Purpose: {purpose}
    - Funding Amount: {funding}
    """
)

# Run the prompt with LangChain
formatted_prompt = prompt.format(title=title, purpose=purpose, funding=funding)
response = model.invoke(formatted_prompt)

# Print the result
if hasattr(response, 'content'):
    print(response.content)
else:
    print(response)

