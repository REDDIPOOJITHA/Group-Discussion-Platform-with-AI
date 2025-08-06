# from flask import Flask, render_template, request, session, jsonify, make_response
# import google.generativeai as genai
# import os
# import time
# import random

# app = Flask(__name__)
# app.secret_key = "bkheifogihgregbeboeiebnvoegijroekegiehgorjgoergh"

# # Configure Gemini API
# genai.configure(api_key="ENTER YOUR API KEY HERE")  # Replace with your Gemini API key

# # List of random names for bots
# BOT_NAMES = [
#     "Alex", "Sofia", "Liam", "Emma", "Noah", "Olivia", "Ava", "Ethan",
#     "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Isabella"
# ]

# # List of suggested topics
# SUGGESTED_TOPICS = [
#     "Social Media Impacts on Students",
#     "Climate Change",
#     "Artificial Intelligence in Society",
#     "Education System Reforms"
# ]

# @app.route('/index')
# def index():
#     return render_template("index.html", suggested_topics=SUGGESTED_TOPICS)

# @app.route('/')
# def topic_selection():
#     return render_template("main.html")

# @app.route('/start', methods=['POST'])
# def start():
#     user_name = request.form.get('user_name')
#     topic_select = request.form.get('topicSelect')
#     topic = request.form.get('topic') if topic_select == 'Custom' else topic_select
#     if not topic:
#         topic = 'General Discussion'
#     # Always 4 bots + 1 user
#     bot_count = 4
#     # Randomly select 4 unique bot names, ensuring Noah and Emma are included
#     bots = random.sample([name for name in BOT_NAMES if name not in ['Noah', 'Emma']], bot_count - 2) + ['Noah', 'Emma']
#     participants = [user_name] + bots  # User is first, followed by bots
#     session['start_time'] = time.time()
#     session['user_timestamps'] = [[] for _ in participants]
#     session['participants'] = participants
#     session['topic'] = topic
#     session['conversation'] = []  # Store conversation for download
#     session['user_score'] = 0  # Initialize user score
#     return render_template("discussion.html", participants=participants, topic=topic)

# @app.route('/bot-reply', methods=['POST'])
# def bot_reply():
#     data = request.get_json()
#     user_input = data.get('prompt', '')
#     topic = session.get('topic', 'General Discussion')
#     participants = session.get('participants', [])

#     # Store user input in conversation history
#     if '[System]' not in user_input:
#         session['conversation'].append(f"{participants[0]}: {user_input}")
#         session['user_score'] = session.get('user_score', 0) + 1  # Increment score for each user input
#         session.modified = True

#     # Construct a topic-specific prompt
#     prompt = (
#         f"You are part of a group discussion on the topic: '{topic}'. "
#         f"A participant just said: '{user_input}'. "
#         f"Respond in one sentence, either supporting, opposing, or adding to the point, "
#         f"while staying relevant to the topic and addressing the previous speaker or the group."
#     )

#     try:
#         model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite-preview-06-17')
#         response = model.generate_content(prompt)
#         reply = response.text.strip() if response.text else "[No reply generated]"
#         # Store bot reply in conversation history
#         session['conversation'].append(f"Bot: {reply}")
#         session.modified = True
#         return jsonify({'reply': reply})
#     except Exception as e:
#         return jsonify({'reply': f"[Error: {str(e)}]"}), 500

# @app.route('/record-timestamp', methods=['POST'])
# def record_timestamp():
#     data = request.get_json()
#     user_index = data.get('user_index')
#     start = data.get('start')
#     end = data.get('end')

#     if 'user_timestamps' not in session:
#         session['user_timestamps'] = [[] for _ in session['participants']]

#     session['user_timestamps'][user_index].append((start, end))
#     session['user_score'] = session.get('user_score', 0) + 0.5  # Add 0.5 to score for speaking time
#     session.modified = True
#     return jsonify({"status": "recorded"})

# @app.route('/download-transcript')
# def download_transcript():
#     conversation = session.get('conversation', [])
#     transcript = "\n".join(conversation)
#     response = make_response(transcript)
#     response.headers["Content-Disposition"] = "attachment; filename=discussion_transcript.txt"
#     response.headers["Content-Type"] = "text/plain"
#     return response

# @app.route('/results')
# def show_results():
#     participants = session.get('participants', [])
#     timestamps = session.get('user_timestamps', [[] for _ in participants])
#     start_time = session.get('start_time', time.time())
#     user_score = session.get('user_score', 0)

#     current_time = time.time()
#     total_gd_minutes = (current_time - start_time) / 60

#     caution = None
#     if total_gd_minutes < 10:
#         caution = "⚠️ Group Discussion was less than 10 minutes."

#     scores = []
#     feedback = []

#     for ts in timestamps:
#         total_spoken_time = sum(e - s for s, e in ts) if ts else 0
#         spoken_minutes = total_spoken_time / 60
#         turns = len(ts)

#         # Normalized scoring
#         time_score = min(5, (spoken_minutes / total_gd_minutes) * 5)  # max 5 for time
#         turn_score = min(5, (turns / 10) * 5)  # max 5 for 10+ turns

#         final_score = int(time_score + turn_score)

#         if turns == 0:
#             final_score = 0
#             tip = "You didn’t speak at all. Try to express your thoughts next time!"
#         elif final_score >= 8:
#             tip = "Excellent contribution with good clarity!"
#         elif final_score >= 5:
#             tip = "Try to elaborate more with relevant points."
#         else:
#             tip = "You can contribute more actively next time."

#         scores.append(final_score)
#         feedback.append(tip)

#     return render_template("results.html", participants=participants, scores=scores, feedback=feedback, caution=caution, user_score=user_score)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request, session, jsonify, make_response, redirect, url_for
import google.generativeai as genai
import os
import time
import random
import json
from datetime import datetime
app = Flask(__name__)
app.secret_key = "bkheifogihgregbeboeiebnvoegijroekegiehgorjgoergh"
# Configure Gemini API
genai.configure(api_key="AIzaSyBZ7yEoHQDtcicboCpULLmYA9bxcbCdKEQ")  # Replace with your actual Gemini API key
# List of random names for bots
BOT_NAMES = [
    "Alex", "Sofia", "Liam", "Emma", "Noah", "Olivia", "Ava", "Ethan",
    "Mia", "James", "Charlotte", "Benjamin", "Amelia", "Lucas", "Isabella"
]
# List of suggested topics
SUGGESTED_TOPICS = [
    "Social Media Impacts on Students",
    "Climate Change Solutions",
    "Artificial Intelligence in Education",
    "Remote Work vs Office Work",
    "Mental Health Awareness",
    "Sustainable Living Practices",
    "Technology Addiction in Youth",
    "Education System Reforms"
]
# Store for managing bot response context
bot_response_context = {}
@app.route('/')
def home():
    return redirect(url_for('topic_selection'))
@app.route('/index')
def index():
    return render_template("index.html", suggested_topics=SUGGESTED_TOPICS)
@app.route('/main')
def topic_selection():
    return render_template("main.html", suggested_topics=SUGGESTED_TOPICS)
@app.route('/start', methods=['POST'])
def start():
    try:
        user_name = request.form.get('user_name', 'User').strip()
        if not user_name:
            user_name = 'User'
        
        topic_select = request.form.get('topicSelect', '')
        custom_topic = request.form.get('topic', '').strip()
        
        # Determine the topic
        if topic_select == 'Custom' and custom_topic:
            topic = custom_topic
        elif topic_select and topic_select != 'Custom':
            topic = topic_select
        else:
            topic = 'General Discussion'
        
        # Always 4 bots + 1 user
        bot_count = 4
        
        # Randomly select 4 unique bot names
        available_bots = BOT_NAMES.copy()
        random.shuffle(available_bots)
        bots = available_bots[:bot_count]
        
        # User is first, followed by bots
        participants = [user_name] + bots
        
        # Initialize session data
        session['start_time'] = time.time()
        session['user_timestamps'] = [[] for _ in participants]
        session['participants'] = participants
        session['topic'] = topic
        session['conversation'] = []  # Store conversation for download
        session['user_score'] = 0
        session['bot_response_count'] = 0
        session['discussion_started'] = False
        session.modified = True
        
        # Initialize bot context
        global bot_response_context
        bot_response_context[session.get('session_id', id(session))] = {
            'previous_responses': set(),
            'conversation_history': [],
            'last_user_message': '',
            'response_count': 0
        }
        
        return render_template("discussion.html", participants=participants, topic=topic)
    
    except Exception as e:
        print(f"Error in start route: {e}")
        return redirect(url_for('topic_selection'))
@app.route('/bot-reply', methods=['POST'])
def bot_reply():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'reply': '[No data received]'}), 400
            
        user_input = data.get('prompt', '').strip()
        if not user_input:
            return jsonify({'reply': '[Empty prompt]'}), 400
        
        topic = session.get('topic', 'General Discussion')
        participants = session.get('participants', ['User', 'Bot1', 'Bot2', 'Bot3', 'Bot4'])
        
        # Get or create session context
        session_id = session.get('session_id', id(session))
        global bot_response_context
        if session_id not in bot_response_context:
            bot_response_context[session_id] = {
                'previous_responses': set(),
                'conversation_history': [],
                'last_user_message': '',
                'response_count': 0
            }
        
        context = bot_response_context[session_id]
        
        # Store user input in conversation history if it's not a system message
        if not any(marker in user_input for marker in ['[System]', '[Discussion resumed]', '[Nudge', 'raised hand but was quiet']):
            session['conversation'].append({
                'timestamp': datetime.now().isoformat(),
                'speaker': participants[0],
                'message': user_input,
                'type': 'user'
            })
            session['user_score'] = session.get('user_score', 0) + 1
            session.modified = True
            
            context['conversation_history'].append(f"{participants[0]}: {user_input}")
            context['last_user_message'] = user_input
        
        # Increment response count
        context['response_count'] += 1
        
        # Create context-aware prompt
        conversation_context = "\n".join(context['conversation_history'][-5:]) if context['conversation_history'] else ""
        
        # Determine response style based on context
        response_styles = ['support', 'oppose', 'question', 'expand', 'counter']
        weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Favor supportive and opposing responses
        response_style = random.choices(response_styles, weights=weights)[0]
        
        # Create enhanced prompt
        if 'raised hand but was quiet' in user_input:
            prompt = f"""You are participating in a group discussion about "{topic}". 
Someone raised their hand but didn't speak. Encourage them to share their thoughts in a friendly, supportive way. 
Keep your response to 15-25 words and speak directly to them."""
        elif '[Discussion resumed]' in user_input:
            prompt = f"""The discussion about "{topic}" just resumed. 
Make a brief comment to re-engage the group. Keep it to 15-25 words."""
        else:
            # Regular response
            if response_style == 'support':
                action_phrase = "agreeing with and building on their point"
            elif response_style == 'oppose':
                action_phrase = "respectfully disagreeing and presenting a counter-perspective"
            elif response_style == 'question':
                action_phrase = "asking a thoughtful follow-up question"
            elif response_style == 'expand':
                action_phrase = "adding more details or examples"
            else:  # counter
                action_phrase = "presenting an alternative viewpoint"
            
            prompt = f"""You are participating in a group discussion about "{topic}".
            
Recent conversation:
{conversation_context}
The last person said: "{user_input}"
Respond by {action_phrase}. Keep your response:
- 15-25 words maximum
- Conversational and natural
- Directly relevant to what was just said
- Engaging to continue the discussion
Don't repeat points already made. Make it sound like natural speech."""
        
        # Generate response using Gemini
        try:
            model = genai.GenerativeModel(model_name='gemini-2.0-flash-exp')
            response = model.generate_content(prompt)
            reply = response.text.strip() if response.text else "[No reply generated]"
            
            # Clean up the response
            reply = reply.replace('"', '').replace('\n', ' ').strip()
            
            # Ensure uniqueness
            attempts = 0
            while reply in context['previous_responses'] and attempts < 3:
                alternative_prompt = prompt + f" (Provide a different response, attempt {attempts + 2})"
                response = model.generate_content(alternative_prompt)
                reply = response.text.strip() if response.text else f"[Alternative response {attempts + 2}]"
                reply = reply.replace('"', '').replace('\n', ' ').strip()
                attempts += 1
            
            # Fallback responses if API fails
            if not reply or reply == "[No reply generated]" or len(reply) < 5:
                fallback_responses = [
                    f"That's an interesting point about {topic}. I'd like to add that we should consider different perspectives.",
                    f"I understand your view on {topic}. However, there might be other factors to consider.",
                    f"Good point! Can you elaborate more on how this relates to {topic}?",
                    f"I see your perspective. From another angle, {topic} also involves various stakeholder interests."
                ]
                reply = random.choice(fallback_responses)
            
            # Store response to avoid repetition
            context['previous_responses'].add(reply)
            
            # Store bot reply in conversation history
            session['conversation'].append({
                'timestamp': datetime.now().isoformat(),
                'speaker': 'Bot',
                'message': reply,
                'type': 'bot'
            })
            session['bot_response_count'] = session.get('bot_response_count', 0) + 1
            session.modified = True
            
            context['conversation_history'].append(f"Bot: {reply}")
            
            # Keep conversation history manageable
            if len(context['conversation_history']) > 20:
                context['conversation_history'] = context['conversation_history'][-15:]
            
            return jsonify({'reply': reply})
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Provide contextual fallback based on the input
            if 'climate' in user_input.lower() or 'climate' in topic.lower():
                fallback = "Climate action requires both individual and collective efforts. What specific steps do you think are most important?"
            elif 'social media' in user_input.lower() or 'social media' in topic.lower():
                fallback = "Social media definitely has both positive and negative impacts. How do you think we can maximize the benefits?"
            elif 'education' in user_input.lower() or 'education' in topic.lower():
                fallback = "Education systems need to evolve with changing times. What changes would you prioritize?"
            else:
                fallback = f"That's a thought-provoking point about {topic}. Can you share more about your perspective?"
            
            return jsonify({'reply': fallback})
    
    except Exception as e:
        print(f"Error in bot_reply: {e}")
        return jsonify({'reply': '[System error - please try again]'}), 500
@app.route('/record-timestamp', methods=['POST'])
def record_timestamp():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data received"}), 400
            
        user_index = data.get('user_index')
        start = data.get('start')
        end = data.get('end')
        
        if user_index is None or start is None or end is None:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        # Initialize user_timestamps if not exists
        if 'user_timestamps' not in session:
            participants_count = len(session.get('participants', []))
            session['user_timestamps'] = [[] for _ in range(participants_count)]
        
        # Ensure the user_index is valid
        if user_index >= len(session['user_timestamps']):
            return jsonify({"status": "error", "message": "Invalid user index"}), 400
        
        # Record the timestamp
        duration = (end - start) / 1000  # Convert to seconds
        session['user_timestamps'][user_index].append((start, end))
        
        # Update score based on speaking duration
        score_increment = min(2.0, duration * 0.1)  # Max 2 points per speaking session
        session['user_score'] = session.get('user_score', 0) + score_increment
        session.modified = True
        
        return jsonify({"status": "recorded", "duration": duration, "score_increment": score_increment})
        
    except Exception as e:
        print(f"Error in record_timestamp: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
@app.route('/download-transcript')
def download_transcript():
    try:
        conversation = session.get('conversation', [])
        topic = session.get('topic', 'Discussion')
        participants = session.get('participants', [])
        start_time = session.get('start_time')
        
        # Create formatted transcript
        transcript_lines = [
            f"GROUP DISCUSSION TRANSCRIPT",
            f"Topic: {topic}",
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Participants: {', '.join(participants)}",
            f"Duration: {time.time() - start_time:.1f} seconds" if start_time else "Duration: Unknown",
            "=" * 50,
            ""
        ]
        
        for entry in conversation:
            if isinstance(entry, dict):
                timestamp = entry.get('timestamp', 'Unknown time')
                speaker = entry.get('speaker', 'Unknown')
                message = entry.get('message', '')
                transcript_lines.append(f"[{timestamp}] {speaker}: {message}")
            else:
                # Handle old format (just strings)
                transcript_lines.append(str(entry))
        
        transcript = "\n".join(transcript_lines)
        
        response = make_response(transcript)
        filename = f"discussion_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-Type"] = "text/plain"
        return response
        
    except Exception as e:
        print(f"Error in download_transcript: {e}")
        return "Error generating transcript", 500
@app.route('/results')
def show_results():
    try:
        participants = session.get('participants', [])
        timestamps = session.get('user_timestamps', [[] for _ in participants])
        start_time = session.get('start_time', time.time())
        user_score = session.get('user_score', 0)
        bot_response_count = session.get('bot_response_count', 0)
        conversation_count = len(session.get('conversation', []))
        
        current_time = time.time()
        total_gd_duration = current_time - start_time
        total_gd_minutes = total_gd_duration / 60
        
        # Check for cautions
        cautions = []
        if total_gd_minutes < 5:
            cautions.append("⚠️ Group Discussion was very short (less than 5 minutes).")
        elif total_gd_minutes < 10:
            cautions.append("⚠️ Group Discussion was shorter than recommended (less than 10 minutes).")
        
        scores = []
        feedback = []
        
        for i, ts in enumerate(timestamps):
            total_spoken_time = sum((e - s) / 1000 for s, e in ts) if ts else 0  # Convert to seconds
            spoken_minutes = total_spoken_time / 60
            turns = len(ts)
            
            if i == 0:  # User
                # Enhanced scoring for user
                participation_rate = min(1.0, spoken_minutes / max(1, total_gd_minutes * 0.3))  # Target 30% participation
                turn_score = min(1.0, turns / 5)  # Target 5+ speaking turns
                consistency = min(1.0, turns / max(1, total_gd_minutes / 2))  # Regular participation
                
                final_score = int((participation_rate + turn_score + consistency) * 3.33)  # Scale to 10
                
                if turns == 0:
                    final_score = 0
                    tip = "You didn't participate in the discussion. Try to share your thoughts next time!"
                elif final_score >= 9:
                    tip = "Outstanding participation! You maintained great engagement throughout."
                elif final_score >= 7:
                    tip = "Excellent contribution with good balance of listening and speaking."
                elif final_score >= 5:
                    tip = "Good participation! Try to speak more frequently to improve engagement."
                elif final_score >= 3:
                    tip = "You participated, but there's room for more active involvement."
                else:
                    tip = "Consider being more active in discussions to share your valuable perspectives."
            
            else:  # Bots (for display purposes)
                # Simulated scores for bots
                final_score = random.randint(6, 9)
                tip = "AI participant - simulated performance"
            
            scores.append(final_score)
            feedback.append(tip)
        
        # Calculate additional metrics
        user_spoken_time = sum((e - s) / 1000 for s, e in timestamps[0]) if timestamps and timestamps[0] else 0
        participation_percentage = (user_spoken_time / total_gd_duration * 100) if total_gd_duration > 0 else 0
        
        metrics = {
            'total_duration': f"{total_gd_minutes:.1f} minutes",
            'user_speaking_time': f"{user_spoken_time:.1f} seconds",
            'participation_percentage': f"{participation_percentage:.1f}%",
            'speaking_turns': len(timestamps[0]) if timestamps else 0,
            'messages_exchanged': conversation_count,
            'bot_responses': bot_response_count
        }
        
        return render_template("results.html", 
                             participants=participants, 
                             scores=scores, 
                             feedback=feedback, 
                             cautions=cautions, 
                             user_score=user_score,
                             metrics=metrics)
    
    except Exception as e:
        print(f"Error in show_results: {e}")
        return render_template("results.html", 
                             participants=['User'], 
                             scores=[0], 
                             feedback=["Error calculating results"], 
                             cautions=["Error in result calculation"], 
                             user_score=0,
                             metrics={})
# Clean up bot context periodically (for memory management)
@app.before_request
def cleanup_context():
    global bot_response_context
    # Remove old contexts (older than 1 hour)
    current_time = time.time()
    to_remove = []
    for session_id, context in bot_response_context.items():
        if not hasattr(context, 'last_accessed'):
            context['last_accessed'] = current_time
        elif current_time - context.get('last_accessed', 0) > 3600:  # 1 hour
            to_remove.append(session_id)
    
    for session_id in to_remove:
        del bot_response_context[session_id]
# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('topic_selection'))
@app.errorhandler(500)
def internal_error(error):
    return redirect(url_for('topic_selection'))
if __name__ == '__main__':
    # Ensure static folder exists
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    
    # Ensure templates folder exists  
    templates_folder = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_folder):
        os.makedirs(templates_folder)
    
    print("Starting Group Discussion App...")
    print("Make sure you have:")
    print("1. Set your Gemini API key")
    print("2. Created templates/ folder with HTML files") 
    print("3. Created static/ folder with robot images")
    print("4. Installed required packages: flask, google-generativeai")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
