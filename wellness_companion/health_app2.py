from flask import Flask, request, render_template
from datetime import datetime
import requests

### FUNCTIONS ###

def get_health_guidelines():
    """
    Function to use OpenDemand's API to get public health guidelines for nutrition, sleep, exercise, and steps."""

    api_key = 'OFqVvzQwlLvgeVfbo0cLYbyMUd67NLRk'
    user_id = '123'

    create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
    create_session_headers = {
        'apikey': api_key
    }
    create_session_body = {
        "pluginIds": [],
        "externalUserId": user_id
    }

    response = requests.post(create_session_url, headers=create_session_headers, json=create_session_body)
    response_data = response.json()

    session_id = response_data['data']['id']

    submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
    submit_query_headers = {
        'apikey': api_key
    }
    submit_query_body_nutrition = {
        "endpointId": "predefined-openai-gpt4o",
        "query": "What are the recommended official guidelines for protein, fruit, vegetable, sugar, and fibre intake for adults? Please provide the output in 1 line per item, such as '30 grams of protein per day, 2 fruits per day, 2 vegetables per day (fruits and vegetables should be in serving number, not cups or grams), less than 50 grams of sugar per day, and 25 grams of fibre per day', each separated by a comma. Additionally, please provide the numerical values for each item as a combined list, after the initial response - with no header just numbers, eg [20,4,3,2].",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    submit_query_body_sleep = {
        "endpointId": "predefined-openai-gpt4o",
        "query": "What are the recommended official guidelines for hours of sleep for adults? Please provide the output in 1 line, such as 'at least 6h sleep per night'. Additionally, please provide the numerical value for this item, after the initial response.",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    submit_query_body_exercise = {
        "endpointId": "predefined-openai-gpt4o",
        "query": "What are the recommended official guidelines for minutes of exercise for adults? Please provide the output in 1 line, such as 'at least 150 minutes of moderate-intensity aerobic activity throughout the week'. Additionally, please provide the numerical values for each item as a combined list, after the initial response",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    submit_query_body_steps = {
        "endpointId": "predefined-openai-gpt4o",
        "query": "What are the recommended official guidelines for step number for adults? Please provide the output in 1 line, such as '10,000 steps per day'. Additionally, please provide the numerical value for this after the initial response",
        "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
        "responseMode": "sync"
    }

    guidelines = {}

    response_nutrition = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body_nutrition)
    guidelines['nutrition'] = response_nutrition.json()

    response_sleep = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body_sleep)
    guidelines['sleep'] = response_sleep.json()

    response_exercise = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body_exercise)
    guidelines['exercise'] = response_exercise.json()

    response_steps = requests.post(submit_query_url, headers=submit_query_headers, json=submit_query_body_steps)
    guidelines['steps'] = response_steps.json()

    nut_rec, nut_vals = guidelines['nutrition']['data']['answer'].split('.')[0], eval(guidelines['nutrition']['data']['answer'].split('.')[1].strip().replace('\n', '') if '.' in guidelines['nutrition']['data']['answer'] else '')

    sleep_rec, sleep_vals = guidelines['sleep']['data']['answer'].split('.')[0], eval(guidelines['sleep']['data']['answer'].split('.')[1].strip().replace('\n', '') if '.' in guidelines['sleep']['data']['answer'] else '')

    exercise_rec, exercise_vals = guidelines['exercise']['data']['answer'].split('.')[0], eval(guidelines['exercise']['data']['answer'].split('.')[1].strip().replace('\n', '') if '.' in guidelines['exercise']['data']['answer'] else '')

    steps_rec, steps_vals = guidelines['steps']['data']['answer'].split('.')[0], eval(guidelines['steps']['data']['answer'].split('.')[1].strip().replace('\n', '') if '.' in guidelines['steps']['data']['answer'] else '')

 
    return guidelines, nut_rec.lower(), nut_vals, sleep_rec.lower(), sleep_vals, exercise_rec.lower(), exercise_vals, steps_rec.lower(), steps_vals

class WellnessApp:
    def __init__(self):
        self.user_data = {}
        self.recommendations = []
        self.feedback = []
        self.nutrition_agent = NutritionAgent()
        self.health_guidelines, self.nut_recs, self.nut_vals, self.sleep_recs, self.sleep_vals, self.exercise_recs, self.exercise_vals, self.step_recs, self.step_vals = get_health_guidelines()

    def input_user_data(self, user_id, sleep_hours, exercise_minutes, steps, mood, stress_level):
        """ Inputs user data from web app window."""
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id]['sleep'] = sleep_hours
        self.user_data[user_id]['exercise'] = exercise_minutes
        self.user_data[user_id]['exercise_steps'] = steps
        self.user_data[user_id]['mood'] = mood
        self.user_data[user_id]['stress_level'] = stress_level

    def generate_recommendations(self, user_id):
        """ Generates health recommendations based on user data and public health guidelines."""
        user = self.user_data.get(user_id)
        if not user:
            return "User not found"

        story = f'''Meet Alex, who's a lot like you. Today, Alex slept for {user['sleep']} hours, exercised for {user['exercise']} minutes, took {user['exercise_steps']} steps, and is feeling {user['mood']} with a stress level of {user['stress_level']}.

'''

        if user['sleep'] < 7:
            story += f'''Alex noticed that getting only {user['sleep']} hours of sleep left them feeling a bit groggy. They remembered that the CDC recommends {self.sleep_recs}. Alex decided to try something new: setting a gentle reminder an hour before bedtime to start winding down. They dimmed the lights, put away their phone, and did some light stretching. The next morning, Alex woke up feeling more refreshed and ready to tackle the day.

'''
        
        if user['exercise'] < int(self.exercise_vals[0]) and user['exercise_steps'] < int(self.step_vals[0]):
            story += f'''Realizing they had only moved for {user['exercise']} minutes and walked {user['exercise_steps']} steps today, Alex recalled the recommendations of {self.exercise_recs} and {self.step_recs}. '''
        elif user['exercise'] < int(self.exercise_vals[0]):
            story += f'''Realizing they had only moved for {user['exercise']} minutes today, Alex recalled the recommendation of {self.exercise_recs}. They decided to start small by adding a 10-minute walk during their lunch break.'''
        elif user['exercise_steps'] < int(self.step_vals[1]):
            story += f'''Realizing they had only walked {user['exercise_steps']} steps today, Alex recalled the recommendation of {self.step_recs}. '''

        if user['exercise'] < int(self.exercise_vals[0]) or user['exercise_steps'] < int(self.step_vals[0]):
            story += f'''They decided to start small by adding a 10-minute walk during their lunch break. As they strolled through a nearby park, Alex noticed the tension in their shoulders melting away and their mood lifting.'''


        if user['mood'] in ['sad', 'anxious', 'angry', 'upset', 'stressed', 'worried']:
            story += f'''Feeling {user['mood']}, Alex remembered a technique their therapist taught them. They paused and did a quick grounding exercise: naming 5 things they could see, 4 they could touch, 3 they could hear, 2 they could smell, and 1 they could taste. By the end of the exercise, Alex felt more centered and in control of their emotions. '''

        if user['stress_level'] > 6:
            story += f'''With their stress level at {user['stress_level']}, Alex found a quiet spot and practiced deep breathing: inhaling slowly for 4 counts, holding for 4, and exhaling for 6. After repeating this 3 times, Alex felt their heart rate slow and their mind clear. They reminded themselves of past challenges they'd overcome, feeling more confident in their ability to handle the current situation.'''

        story += '''As the day went on, Alex felt proud of the small steps they'd taken to improve their well-being. They realized that each positive choice, no matter how small, was a step towards a healthier, happier life.'''

        return story

    def get_nutrition_recommendation(self, user_id, food_input):
        """ Function to pull nutrition recommendations from the NutritionAgent class, using OnDemand's KnowYourFood."""
        return self.nutrition_agent.knowyourfood(food_input, self.nut_recs, self.nut_vals)

class NutritionAgent:
    def knowyourfood(self, food_input, guidelines): 
        """ Function to use OpenDemand's API to get nutrition recommendations based on user's food input.
        Parameters
        ----------
        food_input : str
            Comma-separated string of food items eaten by the user.
        guidelines : str
            String of public health guidelines for nutrition.

        Returns
        -------
        story : str
            Story with nutrition recommendations for the user.

        """

        api_key = 'CqJ9NYoxyw4kZ9iR7wGg4WpoUbfW9fJs'
        user_id = '123'

        create_session_url = 'https://api.on-demand.io/chat/v1/sessions'
        headers = {
            'apikey': api_key
        }
        create_session_body = {
            "pluginIds": [],
            "externalUserId": user_id
        }

        response = requests.post(create_session_url, headers=headers, json=create_session_body)
        response_data = response.json()
        session_id = response_data['data']['id']

        food_items = [f.strip().lower() for f in food_input.split(',')]

        foods = ', '.join(food_items[:-1]) + (', and ' + food_items[-1] if len(food_items) > 1 else '') if food_items else ''

        submit_query_url = f'https://api.on-demand.io/chat/v1/sessions/{session_id}/query'
        submit_query_body = {
            "endpointId": "predefined-openai-gpt4o",
            "query": f'''Alex has eaten {foods} today. He has heard that the recommended guidelines for eating according to the CDC & WHO are: 
            {guidelines}.
            Have I eaten enough of everything or too much of something? What should I do to improve my diet? Please write the answer in third person past tense about someone called Alex, eg. Alex tried to incorporate more protein, so ate a bowl of greek yoghurt with 30g of protein or something similar. If the information already includes food suggestions, we don't need too many meal suggestions so it is not too much.''',
            "pluginIds": ["plugin-1712327325", "plugin-1713962163"],
            "responseMode": "sync"
        }
        
        response = requests.post(submit_query_url, headers=headers, json=submit_query_body)
        query_response_data = response.json()

        story = f"Alex decided to take a closer look at their diet. Today, they had {foods}.\n\n" \
                f"Analyzing their meal, Alex remembered the dietary guidelines for adults: {guidelines}. "

        nut_tip = query_response_data['data']['answer']
        story += nut_tip    

        story += ''' As Alex made these small changes to their diet, they noticed they felt more energized and satisfied throughout the day.'''

        return story

#### APP ####

app = Flask(__name__)
wellness_app = WellnessApp()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = '123' 
        sleep_hours = float(request.form['sleep'])
        exercise_minutes = int(request.form['exercise'])
        steps = int(request.form['steps'])
        mood = request.form['mood']
        stress_level = int(request.form['stress'])
        food_input = request.form['food']

        wellness_app.input_user_data(user_id, sleep_hours, exercise_minutes, steps, mood, stress_level)
        recommendations = wellness_app.generate_recommendations(user_id)
        nutrition_recs = wellness_app.get_nutrition_recommendation(user_id, food_input)

        return render_template('recommendations.html', recommendations=recommendations, nutrition_recs=nutrition_recs)
    
    return render_template('index.html')

if __name__ == '__main__':
    print("Starting the Wellness App server on port 8081...")
    app.run(host='0.0.0.0', port=8081)
