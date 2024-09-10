# Product Shipping/Risk AI API 🧑‍💻🛒
This repository hosts an **AI-powered API** that assists shipping agents in determining whether products are risky or safe to ship. The API uses natural language processing to analyze user input and product details, returning suggestions based on shipping rules and potential product risks.
## Features
- 🚚 **Shipping Risk Analysis**: Automatically assess whether a product poses risks during shipping.
- 📦 **AI-Powered Decisions**: Leverages the OpenAI API to provide shipping advice based on the analysis of user messages and product details.
- 🌍 **Global Shipping Support**: Designed for shipping agents dealing with international logistics.
- 🔧 **Configurable Prompts**: Customize system behavior with prompt files to adjust the responses of the AI model.
## Why?
Shipping agents often face the challenge of shipping potentially risky items to different countries. If a prohibited or hazardous item is shipped, the shipping company may be held liable for customs violations or safety breaches. This API helps mitigate that risk by determining, based on input, whether an item is risky and providing advice accordingly.
## Running Locally
To run this API locally:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shipping-risk-ai-api.git
   cd shipping-risk-ai-api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environmental variables. Ensure you have the following environmental variables set in a .env file or in your shell:
- `API_KEY`
- `OPENAI_API_KEY`
- `SUPABASE_ANON_API_KEY`
- `SUPABASE_ANON_BEARER`
4. Configure the prompts and API settings in `config.yaml`.
5. Run the `app.py` python file or with Uvicorn:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```
6. Open your browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI where you can test the API endpoints directly from your browser.
