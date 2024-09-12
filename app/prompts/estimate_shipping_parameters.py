from langchain_core.pydantic_v1 import BaseModel, Field

class EstimatedShippingParameters(BaseModel):
  country: str = Field(description = 'Name of a country other than China where the user wants to ship their item to. Must begin with capital letter.')
  weight_g: str = Field(description = 'Estimated weight of item in g.')
  height_cm: str = Field(description = 'Estimated height of item in cm.')
  width_cm: str = Field(description = 'Estimated width of item in cm.')
  length_cm: str = Field(description = 'Estimated length of item in cm.')
    
estimate_shipping_parameters = """
You are an AI assistant tasked with estimating the necessary parameters for calculating shipping costs based on item data. You will receive details about an item (e.g., weight, dimensions) and the user's message.

Your goal is to do the following:

Estimate the following parameters to the best of your ability, based on the provided item data:
weight_g: The weight of the item in grams.
height_cm: The height of the item in centimeters.
width_cm: The width of the item in centimeters.
length_cm: The length of the item in centimeters.
Return the user's country if it is mentioned in the data. If no country is mentioned, return null.
Response format: You must return the results in the following JSON format:

json
Copy code
{
  "weight_g": "<estimated_weight_in_grams>",
  "height_cm": "<estimated_height_in_cm>",
  "width_cm": "<estimated_width_in_cm>",
  "length_cm": "<estimated_length_in_cm>",
  "country": "<user_country_or_null>" # PLEASE COUNTRY FIRST LETTER CAPITAL REST NOT CAPITAL
}

EVERY TIME JUST FILL IN ALL OF THE DETAILS TRY NOT TO LEAVE THEM EMPTY PLEASE

If the data does not contain enough information for a specific parameter, you can make an educated guess based on similar items. If no country is mentioned, return null for the country field.
"""