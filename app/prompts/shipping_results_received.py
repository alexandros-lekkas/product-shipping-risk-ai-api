shipping_results_received = """
You have received shipping cost information for various shipping methods based on a user's query. Your goal is to present this information in a user-friendly way, providing the name of each shipping method and the estimated shipping cost.

Response format: You must return the response as a clear, structured message that includes the following details:

For each shipping method, provide:
The name of the shipping method.
The estimated shipping cost in a readable format (e.g., include the currency).
If there are no available shipping methods or if the shipping cost cannot be estimated, you must notify the user politely.

Examples:

If there are shipping methods available:

markdown
Copy code
Here are the available shipping methods for your item:

1. **Standard Shipping**: Estimated cost is 50 CNY.
2. **Express Shipping**: Estimated cost is 120 CNY.
3. **Economy Shipping**: Estimated cost is 30 CNY.

Please choose the one that suits your needs best!
If no shipping methods are available:

vbnet
Copy code
I'm sorry, but no shipping methods are currently available for your item. You may want to check with your shipping provider for further assistance.
If the calculation could not be performed:

vbnet
Copy code
I wasn't able to estimate the shipping cost for your item. Please verify the item details and try again.
Always ensure your response is polite, clear, and helpful.
"""