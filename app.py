from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('grammar.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS topics')
    cursor.execute('DROP TABLE IF EXISTS questions')
    
    cursor.execute('''CREATE TABLE topics (
        key TEXT PRIMARY KEY, title TEXT, definition TEXT, examples TEXT, color TEXT)''')
    
    cursor.execute('''CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, topic_key TEXT, 
        question TEXT, options TEXT, answer INTEGER)''')

    # UPDATED: Only "Parts of Speech" changed with 1-line definitions and examples below
    topics = [
        ('tenses', 
         'Verb Tenses', 
         'Tenses indicate the time of an action or state of being. They are categorized into Past, Present, and Future, each having simple, continuous, perfect, and perfect continuous forms.', 
         'Past Simple: I walked to school. | Present Continuous: I am walking now. | Future Simple: I will walk tomorrow.', 
         '#2196F3'),
        
        ('prepositions', 
         'Prepositions', 
         'A preposition is a word used to link nouns, pronouns, or phrases to other words within a sentence. They act to connect the people, objects, time and locations of a sentence.', 
         'Place: The book is ON the table. | Time: We met AT noon. | Direction: She walked INTO the room.', 
         '#FF9800'),
        
        ('voice', 
         'Active & Passive', 
         'Voice describes the relationship between the action and the participants. In Active voice, the subject performs the action. In Passive voice, the subject receives the action, often using "to be" + past participle.', 
         'Active: The chef prepared the meal. | Passive: The meal was prepared by the chef.', 
         '#4CAF50'),
        
        ('parts', 
         'The 8 Parts of Speech', 
         '1. NOUN: A part of speech that names a person, place, thing, idea, quality, or action. They function as subjects or objects in a sentence.\nExamples: City, Paris, Love, Team, Teacher\n\n2. PRONOUN: A word that functions as a replacement for a noun or noun phrase.\nExamples: He, She, They, It, We\n\n3. VERB: A word used to describe an action, state, or occurrence.\nExamples: Run, Speak, Think, Is, Believe\n\n4. ADJECTIVE: A word that modifies or describes a noun or pronoun.\nExamples: Blue, Tall, Happy, Fast, Intelligent\n\n5. ADVERB: A word that modifies a verb, an adjective, or another adverb.\nExamples: Quickly, Very, Yesterday, Well, Often\n\n6. PREPOSITION: A word showing the relationship of a noun to another word in the sentence.\nExamples: In, On, Under, Between, Through\n\n7. CONJUNCTION: A word used to connect clauses or sentences or to coordinate words.\nExamples: And, But, Or, Because, Although\n\n8. INTERJECTION: An abrupt remark or exclamation used to express strong emotion.\nExamples: Wow, Ouch, Hey, Oops, Oh', 
         'Click "Start Quiz" to test your knowledge of these 8 parts!', 
         '#9C27B0')
    ]
    cursor.executemany('INSERT INTO topics VALUES (?,?,?,?,?)', topics)

    # 5 Questions per topic
    questions = [
        ('tenses', 'I ____ to the gym yesterday.', 'go,went,gone', 1),
        ('tenses', 'She ____ her dinner right now.', 'eats,is eating,ate', 1),
        ('tenses', 'We ____ a party next week.', 'had,have,will have', 2),
        ('tenses', 'They ____ soccer every Sunday.', 'play,plays,played', 0),
        ('tenses', 'The sun ____ in the east.', 'rise,rises,rising', 1),
        
        ('prepositions', 'The keys are ____ the drawer.', 'on,in,at', 1),
        ('prepositions', 'The bird flew ____ the house.', 'over,under,in', 0),
        ('prepositions', 'I am waiting ____ the bus stop.', 'on,in,at', 2),
        ('prepositions', 'Put the plate ____ the table.', 'on,into,at', 0),
        ('prepositions', 'He sat ____ the two trees.', 'among,between,with', 1),

        ('voice', '"The mouse was caught" is...', 'Active,Passive', 1),
        ('voice', '"She sang a song" is...', 'Active,Passive', 0),
        ('voice', 'Passive: "He invited me" is...', 'I am invited,I was invited by him', 1),
        ('voice', '"The car is being fixed" is...', 'Active,Passive', 1),
        ('voice', '"The cat chased the ball" is...', 'Active,Passive', 0),

        ('parts', 'Identify the Noun:', 'Run,Beautiful,London', 2),
        ('parts', 'Identify the Verb:', 'Apple,Speak,Slowly', 1),
        ('parts', 'Identify the Adjective:', 'Tall,He,Jump', 0),
        ('parts', 'Which is a Proper Noun?', 'Boy,Country,India', 2),
        ('parts', 'Which word describes a Noun?', 'Adverb,Adjective,Verb', 1)
    ]
    cursor.executemany('INSERT INTO questions (topic_key, question, options, answer) VALUES (?,?,?,?)', questions)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('grammar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM topics')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', topics=data)

@app.route('/lesson/<topic_key>')
def lesson(topic_key):
    conn = sqlite3.connect('grammar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM topics WHERE key = ?', (topic_key,))
    t = cursor.fetchone()
    conn.close()
    return render_template('lesson.html', t=t)

@app.route('/api/questions/<topic_key>')
def get_questions(topic_key):
    conn = sqlite3.connect('grammar.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question, options, answer FROM questions WHERE topic_key = ?', (topic_key,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"q": r[0], "o": r[1].split(','), "a": r[2]} for r in rows])

# --- UPDATED START LOGIC FOR RENDER ---
if __name__ == '__main__':
    # Initialize the database
    init_db()
    
    # Get port from environment variable (Render) or default to 5000 (Local)
    port = int(os.environ.get("PORT", 5000))
    
    # Use 0.0.0.0 to make the server accessible externally
    app.run(host='0.0.0.0', port=port)
