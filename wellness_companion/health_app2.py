from flask import Flask, request, jsonify, render_template_string
import json
from datetime import datetime

def get_health_guidelines():
    # This function fetches health guidelines from official websites
    # In a real scenario, you'd implement API calls here
    guidelines = {
        'sleep': {
            'source': 'https://www.cdc.gov/sleep/about_sleep/how_much_sleep.html',
            'recommendation': '7 or more hours per night for adults'
        },
        'exercise': {
            'source': 'https://www.who.int/news-room/fact-sheets/detail/physical-activity',
            'recommendation': 'at least 150 minutes of moderate-intensity aerobic activity throughout the week'
        },
        'nutrition': {
            'source': 'https://www.dietaryguidelines.gov/sites/default/files/2020-12/Dietary_Guidelines_for_Americans_2020-2025.pdf',
            'fruits': 2,  # cups per day
            'vegetables': 2.5,  # cups per day
            'grains': 6,  # ounces per day
            'protein': 5.5,  # ounces per day
            'dairy': 3,  # cups per day
        }
    }
    return guidelines

class WellnessApp:
    def __init__(self):
        self.user_data = {}
        self.recommendations = []
        self.feedback = []
        self.nutrition_agent = NutritionAgent()
        self.health_guidelines = get_health_guidelines()

    def input_user_data(self, user_id, sleep_hours, exercise_minutes, mood, stress_level):
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id]['sleep'] = sleep_hours
        self.user_data[user_id]['exercise'] = exercise_minutes
        self.user_data[user_id]['mood'] = mood
        self.user_data[user_id]['stress_level'] = stress_level

    def generate_recommendations(self, user_id):
        user = self.user_data.get(user_id)
        if not user:
            return "User not found"

        story = f'''Meet Alex, who's a lot like you. Today, Alex slept for {user['sleep']} hours, exercised for {user['exercise']} minutes, and is feeling {user['mood']} with a stress level of {user['stress_level']}.

'''

        sleep_rec = self.health_guidelines['sleep']['recommendation']
        if user['sleep'] < 7:
            story += f'''Alex noticed that getting only {user['sleep']} hours of sleep left them feeling a bit groggy. They remembered that the CDC recommends {sleep_rec}. Alex decided to try something new: setting a gentle reminder an hour before bedtime to start winding down. They dimmed the lights, put away their phone, and did some light stretching. The next morning, Alex woke up feeling more refreshed and ready to tackle the day.

'''
        
        exercise_rec = self.health_guidelines['exercise']['recommendation']
        if user['exercise'] < 30:
            story += f'''Realizing they had only moved for {user['exercise']} minutes today, Alex recalled the WHO recommendation of {exercise_rec}. They decided to start small by adding a 10-minute walk during their lunch break. As they strolled through a nearby park, Alex noticed the tension in their shoulders melting away and their mood lifting.

'''

        if user['mood'] in ['sad', 'anxious', 'angry']:
            story += f'''Feeling {user['mood']}, Alex remembered a technique their therapist taught them. They paused and did a quick grounding exercise: naming 5 things they could see, 4 they could touch, 3 they could hear, 2 they could smell, and 1 they could taste. By the end of the exercise, Alex felt more centered and in control of their emotions.

'''

        if user['stress_level'] > 7:
            story += f'''With their stress level at {user['stress_level']}, Alex found a quiet spot and practiced deep breathing: inhaling slowly for 4 counts, holding for 4, and exhaling for 6. After repeating this 3 times, Alex felt their heart rate slow and their mind clear. They reminded themselves of past challenges they'd overcome, feeling more confident in their ability to handle the current situation.

'''

        story += '''As the day went on, Alex felt proud of the small steps they'd taken to improve their well-being. They realized that each positive choice, no matter how small, was a step towards a healthier, happier life.'''

        return story

    def get_nutrition_recommendation(self, user_id, food_input):
        return self.nutrition_agent.generate_recommendation(food_input, self.health_guidelines['nutrition'])

    def provide_feedback(self, user_id, recommendation, helpful):
        self.feedback.append({
            'user_id': user_id,
            'recommendation': recommendation,
            'helpful': helpful,
            'timestamp': datetime.now().isoformat()
        })

class NutritionAgent:
    def generate_recommendation(self, food_input, guidelines):
        # Parse the food input
        foods = [f.strip().lower() for f in food_input.split(',')]
        
        # Start the story
        story = f'''Alex decided to take a closer look at their diet. Today, they had {', '.join(foods)}.

        Analyzing their meal, Alex remembered the dietary guidelines:
        - {guidelines['fruits']} cups of fruits per day
        - {guidelines['vegetables']} cups of vegetables per day
        - {guidelines['grains']} ounces of grains per day
        - {guidelines['protein']} ounces of protein per day
        - {guidelines['dairy']} cups of dairy per day
        '''

        fruit_count = sum(1 for food in foods if food in ['apple', 'banana', 'orange', 'berries'])
        veg_count = sum(1 for food in foods if food in ['broccoli', 'spinach', 'carrots', 'tomatoes'])
        grain_count = sum(1 for food in foods if food in ['bread', 'rice', 'pasta', 'cereal'])
        protein_count = sum(1 for food in foods if food in ['chicken', 'beef', 'fish', 'eggs', 'beans'])
        dairy_count = sum(1 for food in foods if food in ['milk', 'yogurt', 'cheese'])

        if fruit_count < guidelines['fruits']:
            story += f'''Alex realized they hadn't eaten much fruit today. Remembering that the Dietary Guidelines for Americans recommend {guidelines['fruits']} cups of fruits per day, they decided to add a colorful fruit to their next meal. They sliced a banana over their cereal and packed an apple for a snack, looking forward to the natural sweetness and energy boost.

'''
        if veg_count < guidelines['vegetables']:
            story += f'''Noticing a lack of vegetables in their meals, Alex recalled that {guidelines['vegetables']} cups of vegetables per day are suggested. They got creative and added some spinach to their sandwich and prepared some carrot sticks for a crunchy snack. The vibrant colors on their plate made the meal more appealing and satisfying.

'''
        if grain_count < guidelines['grains']:
            story += f'''Alex realized they hadn't had many grains today. Knowing that {guidelines['grains']} ounces of grains per day are recommended, they decided to try something new. They cooked some quinoa for dinner, enjoying its nutty flavor and the sustained energy it provided.

'''
        if protein_count < guidelines['protein']:
            story += f'''Thinking about their protein intake, Alex remembered the recommendation of {guidelines['protein']} ounces per day. They decided to add some beans to their salad at lunch, appreciating the variety and fullness it brought to their meal.

'''
        if dairy_count < guidelines['dairy']:
            story += f'''Realizing they hadn't had much dairy, Alex recalled the suggestion of {guidelines['dairy']} cups per day. Not being a big fan of milk, they opted for some Greek yogurt as an afternoon snack, enjoying its creamy texture and the calcium boost.

'''

        story += '''As Alex made these small changes to their diet, they noticed they felt more energized and satisfied throughout the day.'''

        return story

app = Flask(__name__)
wellness_app = WellnessApp()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = 'user1'  # In a real app, you'd have user authentication
        sleep_hours = float(request.form['sleep'])
        exercise_minutes = float(request.form['exercise'])
        mood = request.form['mood']
        stress_level = int(request.form['stress'])
        food_input = request.form['food']

        wellness_app.input_user_data(user_id, sleep_hours, exercise_minutes, mood, stress_level)
        recommendations = wellness_app.generate_recommendations(user_id)
        nutrition_recs = wellness_app.get_nutrition_recommendation(user_id, food_input)

        return render_template_string('''
            <h1>Your Wellness Recommendations</h1>
            <h2>General Wellness:</h2>
            <p>{{ recommendations|safe }}</p>
            <h2>Nutrition:</h2>
            <p>{{ nutrition_recs|safe }}</p>
            <a href="/">Back to Input</a>
        ''', recommendations=recommendations, nutrition_recs=nutrition_recs)

    return render_template_string('''
        <h1>Wellness Companion</h1>
        <form method="post">
            <label>Sleep hours: <input type="number" step="0.1" name="sleep" required></label><br>
            <label>Exercise minutes: <input type="number" name="exercise" required></label><br>
            <label>Mood: <input type="text" name="mood" required></label><br>
            <label>Stress level (1-10): <input type="number" min="1" max="10" name="stress" required></label><br>
            <label>Food eaten today (comma-separated): <input type="text" name="food" required></label><br>
            <input type="submit" value="Get Recommendations">
        </form>
    ''')

if __name__ == '__main__':
    print("Starting the Wellness App server on port 8080...")
    app.run(host='0.0.0.0', port=8080)
