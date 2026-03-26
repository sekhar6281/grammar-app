from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('grammar.db')
    cursor = conn.cursor()
    # Clean start: drop existing tables to ensure the latest data is loaded
    cursor.execute('DROP TABLE IF EXISTS topics')
    cursor.execute('DROP TABLE IF EXISTS questions')
    
    cursor.execute('''CREATE TABLE topics (
        key TEXT PRIMARY KEY, title TEXT, definition TEXT, examples TEXT, color TEXT)''')
    
    cursor.execute('''CREATE TABLE questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, topic_key TEXT, 
        question TEXT, options TEXT, answer INTEGER)''')

    # Content for the 4 modules
    topics = [
        ('tenses', 
         'Verb Tenses', 
         'Tenses indicate the time of an action. They are categorized into Past, Present, and Future.', 
         'Past: I walked. | Present: I walk. | Future: I will walk.', 
         '#2196F3'),
        
        ('prepositions', 
         'Prepositions', 
         'Words used to link nouns to other words, showing relationship in space or time.', 
         'On the table, At noon, Under the bridge.', 
         '#FF9800'),
        
        ('voice', 
         'Active & Passive', 
         'Active voice focuses on the doer. Passive voice focuses on the action being received.', 
         'Active: The chef cooked. | Passive: The meal was cooked by the chef.', 
         '#4CAF50'),
        
        ('parts', 
         'The 8 Parts of Speech', 
         '1. NOUN: Names a person, place, thing, or idea.\n2. PRONOUN: Replaces a noun.\n3. VERB: Shows action.\n4. ADJECTIVE: Describes a noun.\n5. ADVERB: Modifies a verb.\n6. PREPOSITION: Shows relationship.\n7. CONJUNCTION: Joins words.\n8. INTERJECTION: Expresses emotion.', 
         'Click "Start Quiz" to test your knowledge!', 
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

if __name__ == '__main__':
    # SELF-HEALING LOGIC: Detects malformed database and fixes it automatically
    try:
        init_db()
    except sqlite3.DatabaseError:
        if os.path.exists('grammar.db'):
            os.remove('grammar.db')
        init_db()
        print("Database repaired successfully!")

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
