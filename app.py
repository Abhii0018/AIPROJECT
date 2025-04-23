from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "AIzaSyC3tFoG8su2M5DkWbomrOujUmueAm60q70"
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GEMINI_API_KEY)

@app.route('/generate-proposal', methods=['POST'])
def generate_proposal():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        title = data.get('title', '').strip()   
        purpose = data.get('purpose', '').strip()
        funding = data.get('funding', '').strip()

        if not all([title, purpose, funding]):
            return jsonify({
                "status": "error",
                "message": "All fields (title, purpose, funding) are required"
            }), 400

        prompt_template = """Generate a comprehensive project funding proposal with the following details:
        Project Title: {title}
        Project Purpose: {purpose}
        Requested Funding Amount: ${funding}

        The proposal should include these sections:
        1. Executive Summary
        2. Project Description
        3. Objectives
        4. Budget Breakdown
        5. Expected Outcomes
        
        Use clear section headings and bullet points where appropriate.
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        response = model.invoke(prompt.format(title=title, purpose=purpose, funding=funding))

        if not response or not response.content:
            return jsonify({
                "status": "error",
                "message": "Failed to generate proposal content"
            }), 500

        return jsonify({
            "status": "success",
            "title": title,
            "purpose": purpose,
            "funding": funding,
            "proposal": response.content
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)