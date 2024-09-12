# Product Shipping/Risk AI API 🧑‍💻🛒

## 💡 Features
- 🚚 **Shipping Risk Analysis**: Assists users in recognizing the risks of shipping certain products to their location.
- 📦 **AI-Powered Decisions**: Leverages AI to provide flexible responses to user queries that do not have to be hard coded.
- 🌍 **Global Shipping Support**: Designed for shipping agents dealing with international logistics, currently interfaces with [HaulBuy's](https://www.haulbuy.com) shipping API as an example.
- 🔧 **Configurable Prompts**: Customize system behavior with prompt files to adjust the responses of the AI model.

## 🤔 Why?

Shipping agents, who mostly act as middlemen, oftentimes bear a lot of legal risk when malicious users decide to violate their TOS by attempting to ship out prohibited or hazardous items. Frequently, these agents can be held liable for customs violations and safety breaches. This API's goal is to help mitigate that risk by determining, based on input, whether an item is risky or not and providing advice accordingly.

## 🌟 As Seen On
- **[HaulBuy](https://www.haulbuy.com)**: The first shipping agent to adopt and implement this technology, enhancing the safety of their shipping processes. As outlined in the Features section of this README, HaulBuy's shipping line API serves as a prime example, as they directly commissioned me to develop this solution for their platform. However, the product is versatile and can be applied across various platforms.

## 🧑‍💻 Running Locally

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

5. Run the `run.py` python file or with Uvicorn:
   ```bash
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

6. Open your browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI where you can test the API endpoints directly from your browser.
