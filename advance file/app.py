import os
import base64
import json
import re
import urllib.parse
from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode('utf-8')

def get_youtube_search_url(recipe_name):
    query = f"{recipe_name} recipe cooking"
    encoded_query = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"

def analyze_food_image(base64_image, mime_type, language):
    prompt = f"""You are an expert chef and food analyst.

IMPORTANT: Give the entire response in {language} language.

Analyze this food image carefully and provide a complete recipe.

Please respond in the following JSON format ONLY (no extra text):

{{
  "dish_name": "Name of the dish",
  "cuisine": "Type of cuisine",
  "difficulty": "Easy / Medium / Hard",
  "prep_time": "X minutes",
  "cook_time": "X minutes",
  "servings": "X servings",
  "description": "Description",
  "ingredients": ["item 1", "item 2"],
  "instructions": ["Step 1", "Step 2"],
  "tips": ["Tip 1", "Tip 2"],
  "nutrition": {{
    "calories": "X kcal",
    "protein": "Xg",
    "carbs": "Xg",
    "fat": "Xg"
  }}
}}
"""

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        max_tokens=2048,
        temperature=0.7
    )

    response_text = response.choices[0].message.content.strip()

    json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
    if json_match:
        return json.loads(json_match.group())
    else:
        return json.loads(response_text)

@app.route('/')
def index():
    return render_template('animation.html')

@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():
    if 'image' not in request.files:
        return jsonify({'error': 'Koi image upload nahi hui'}), 400
    
    image_file = request.files['image']
    
    if image_file.filename == '':
        return jsonify({'error': 'Image select nahi ki gayi'}), 400
    
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    mime_type = image_file.content_type
    
    if mime_type not in allowed_types:
        return jsonify({'error': 'Sirf JPG, PNG, ya WEBP images allowed hain'}), 400
    
    try:
        language = request.form.get("language", "English")
        base64_image = encode_image(image_file)
        recipe_data = analyze_food_image(base64_image, mime_type, language)
        
        dish_name = recipe_data.get('dish_name', 'Unknown Dish')
        youtube_url = get_youtube_search_url(dish_name)
        recipe_data['youtube_url'] = youtube_url
        recipe_data['youtube_query'] = f"{dish_name} recipe"
        
        return jsonify({'success': True, 'recipe': recipe_data})
    
    except json.JSONDecodeError as e:
        return jsonify({'error': f'Recipe parse karne mein error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
