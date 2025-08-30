import streamlit as st
import time

# --- App Configuration ---
st.set_page_config(
    page_title="Your Personal Fitness Coach",
    page_icon="✨",
    layout="wide"
)

# --- Custom Styling (CSS) ---
# This injects custom CSS to make the app more colorful and lively.
st.markdown("""
<style>
    /* Main background and font */
    .stApp {
        background-color: #000000; /* Set background to black */
        font-family: 'Poppins', sans-serif;
        color: #FFFFFF; /* Set default text to white */
    }
    
    /* Title style */
    h1 {
        color: #FF6F00; /* A vibrant orange for the main title */
        font-weight: 700;
    }

    /* Subheader style */
    h2, h3 {
        color: #00BCD4; /* A lighter, vibrant teal for headers on dark background */
    }

    /* Custom styled boxes for recommendations */
    .custom-box {
        background-color: #272727; /* Dark grey for a subtle contrast */
        border-left: 10px solid #FFC107; /* A cheerful yellow accent */
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .custom-box p {
        font-size: 1.1rem; /* Slightly larger font size for readability */
        color: #FFFFFF; /* Changed to white */
    }
    .custom-box ul {
        font-size: 1.1rem;
        color: #FFFFFF; /* Changed to white */
    }
    .custom-box h4 {
        color: #FFC107; /* Match the yellow accent for sub-titles inside boxes */
    }

    /* Button style */
    .stButton>button {
        background-color: #FF6F00;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
    }
</style>
""", unsafe_allow_html=True)


# --- State Management ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "", "weight": 0.0, "height": 0.0, "diet": "Vegetarian",
        "living_situation": "With Family", "feeling": "Not Sure", "gender": "Female"
    }
if 'bmi' not in st.session_state: st.session_state.bmi = 0
if 'bmi_category' not in st.session_state: st.session_state.bmi_category = ""


# --- Helper Functions ---
def calculate_bmi(weight_kg, height_cm):
    if height_cm > 0:
        return round(weight_kg / ((height_cm / 100) ** 2), 1)
    return 0

def classify_bmi(bmi):
    if bmi < 18.5: return "Underweight"
    if 18.5 <= bmi <= 24.9: return "Healthy Weight"
    if 25.0 <= bmi <= 29.9: return "Overweight"
    return "Obese"

# --- Content Generation Functions (Expanded & Styled) ---
# NOTE: Titles changed from Markdown '###' to HTML '<h3>' to fix rendering bug.
def get_diet_recommendations(category, diet_type, living_situation, name):
    title = f"<h3>🥗 Namaste {name}, Let's Nourish Your Body!</h3>"
    base_info = f"""
    <div class="custom-box">
    <p>Based on your <b>{category}</b> status, here are some simple, balanced meal ideas that fit your <b>{diet_type}</b> preference. Think of this as a friendly guide, not a strict rulebook. The goal is to build a healthy relationship with food!</p>
    <h4>🌟 Golden Rules of Mindful Eating:</h4>
    <ul>
        <li><b>Stay Hydrated:</b> Aim for 2-3 litres of water daily. It's the simplest and most effective habit!</li>
        <li><b>Portion Smarts:</b> Use a smaller plate. When eating a thali, fill half your plate with vegetables/salad, a quarter with dal/protein, and a quarter with rice/roti.</li>
        <li><b>Eat Slowly:</b> Savor each bite. It takes 20 minutes for your brain to register fullness.</li>
        <li><b>Smart Snacking:</b> For mid-meal hunger, grab a fruit, a handful of chana, or a bowl of dahi.</li>
    </ul>
    </div>
    """
    
    specific_advice = ""
    if category in ["Overweight", "Obese"]:
        specific_advice = """
        <h4>🎯 Your Focus: Nutrient-Dense Foods</h4>
        <p>We want foods that are high in nutrients but moderate in calories.</p>
        """
        if diet_type == "Vegetarian":
            specific_advice += "<ul><li><b>Breakfast:</b> Oats upma, moong dal chilla, or poha with lots of veggies.</li><li><b>Lunch:</b> 2 multigrain rotis, a large bowl of dal, sabzi, and a big salad.</li><li><b>Dinner:</b> Keep it light! Vegetable khichdi, paneer bhurji, or a large bowl of lentil soup (dal).</li></ul>"
        elif diet_type == "Eggetarian":
            specific_advice += "<ul><li><b>Breakfast:</b> 2 boiled eggs or a simple egg bhurji with less oil.</li><li><b>Lunch:</b> Add boiled eggs to your veg thali for a protein boost.</li><li><b>Dinner:</b> A simple egg curry with 1-2 rotis.</li></ul>"
        else:  # Non-Vegetarian
            specific_advice += "<ul><li><b>Breakfast:</b> Egg bhurji or 2 boiled eggs.</li><li><b>Lunch:</b> 100g grilled chicken/fish with a large salad and a small portion of brown rice or one roti.</li><li><b>Dinner:</b> Homestyle chicken/fish curry (thin gravy) with lots of veggies.</li></ul>"

    elif category == "Underweight":
        specific_advice = "<h4>🎯 Your Focus: Healthy Weight Gain</h4><p>We need nutrient-dense and calorie-rich foods to build strength.</p><ul><li>Add healthy fats like ghee to your rotis and dal.</li><li>Include paneer, potatoes, sweet potatoes, and nuts.</li><li>For non-vegetarians and eggetarians, eggs and chicken are excellent for muscle building.</li></ul>"
    
    else: # Healthy Weight
        specific_advice = "<h4>🎯 Your Focus: Maintenance & Vitality</h4><p>You're doing great! Let's focus on maintaining this balance with variety and whole foods.</p><ul><li>Ensure a good mix of protein (dal, paneer, eggs, chicken), complex carbs (roti, brown rice), and colorful vegetables.</li></ul>"

    living_advice = ""
    if living_situation == "Cook Alone":
        living_advice = "<h4>💡 Tip for You:</h4><p>One-pot meals are your best friend! Think vegetable pulao, dal khichdi, or a quick paneer/chicken stir-fry. Easy, quick, and nutritious.</p>"
    elif living_situation == "PG/Hostel":
        living_advice = "<h4>💡 Making Smart Choices in the Mess:</h4><p>You can still eat healthy!<ul><li>Always take the salad if it's available.</li><li>Ask for an extra serving of dal and sabzi instead of a second helping of rice or puri.</li><li>Avoid fried items like pakoras or papad when you can.</li><li>Drink a glass of water before your meal to control your appetite.</li></ul></p>"
    else: # With Family
        living_advice = "<h4>💡 Eating with Family:</h4><p>No need for a separate meal! Just adjust your portions. Take a larger serving of sabzi and dal, and a smaller one of rice or roti. You're still sharing the meal and love, just in a way that serves your goals.</p>"

    return f"{title}{base_info}<div class='custom-box'>{specific_advice}{living_advice}</div>"


def get_workout_recommendations(category, name):
    title = f"<h3>🏃‍♀️ {name}, Let's Get Moving and Feel Amazing!</h3>"
    content = ""
    if category in ["Overweight", "Obese"]:
        content = """
        <h4>Your Goal: Build Consistency & Joyful Movement</h4>
        <ul>
            <li><b>Week 1: The Foundation.</b> Let's begin with a 30-minute brisk walk every day. Put on some music, listen to a podcast, and enjoy this time for yourself!</li>
            <li><b>Week 2: Building Stamina.</b> Increase your walk to 45 minutes. Focus on your breathing. You're building a powerful habit!</li>
            <li><b>Week 3: Adding Strength.</b> After your walk, let's add 2 sets of 10 simple squats and 10 wall push-ups. This will start building muscle, which boosts metabolism.</li>
            <li><b>Beyond:</b> We'll slowly increase the duration and add more fun exercises. The goal is to find movement you love!</li>
        </ul>
        """
    # ... (similar expansions for other categories) ...
    else:
        content = """
        <h4>Your Goal: Maintain Fitness & Build Strength</h4>
        <ul>
            <li><b>Your Routine:</b> Aim for 3-5 days of activity per week. A mix of cardio (walking, jogging, cycling) and strength training (yoga, bodyweight exercises) is ideal.</li>
            <li><b>Try Something New:</b> Explore online dance workouts, try Surya Namaskar for flexibility, or find a sport you enjoy. Keeping it fun is the key to consistency.</li>
        </ul>
        """
    return f"{title}<div class='custom-box'>{content}</div>"

def get_habit_and_confidence_tips(name):
    title = f"<h3>💡 {name}, Let's Build Habits for a Confident You!</h3>"
    content = f"""
    <h4>Small Steps, Giant Leaps</h4>
    <ul>
        <li><b>The 80/20 Rule:</b> Eat healthy 80% of the time, and allow yourself treats 20% of the time. This isn't about restriction; it's about balance.</li>
        <li><b>Listen to Your Body:</b> Eat when you're hungry, stop when you're satisfied (not stuffed). Your body is incredibly smart!</li>
        <li><b>Healthy Swaps:</b> Switch to whole wheat roti, use jaggery instead of sugar, and opt for baked/roasted snacks over fried ones.</li>
    </ul>
    <h4>💖 Building Unshakable Confidence:</h4>
    <ul>
        <li><b>Celebrate Non-Scale Victories:</b> Did your clothes fit better? Did you have more energy? Did you walk further than last week? Celebrate these wins! They matter more than the number on the scale.</li>
        <li><b>Positive Self-Talk:</b> Speak to yourself like you would a dear friend. Instead of "I have to work out," try "I get to move my body and feel strong."</li>
        <li><b>You Are More Than a Number:</b> Your weight does not define your worth. This journey is about health, strength, and feeling good in your own skin. You are already amazing, and you've got this!</li>
    </ul>
    """
    return f"{title}<div class='custom-box'>{content}</div>"
    
def get_gender_specific_tips(gender, category, name):
    title = f"<h3>🌟 Personalized Insights Just for You, {name}</h3>"
    content = ""
    if gender == "Female":
        content = """
        <h4>Health Focus for Women:</h4>
        <ul>
            <li><b>Iron & Calcium are Key:</b> Ensure your diet is rich in iron (spinach, lentils, beans) and calcium (dairy, ragi, sesame seeds) for bone health and energy levels.</li>
            <li><b>Hormonal Harmony:</b> Regular exercise and a balanced diet can significantly help with managing PMS and maintaining hormonal balance.</li>
            <li><b>Stress & Weight:</b> For many women, stress can lead to weight gain, especially around the midsection. Our stress management tips are extra important for you!</li>
        </ul>
        """
    elif gender == "Male":
        content = """
        <h4>Health Focus for Men:</h4>
        <ul>
            <li><b>Protein for Muscle:</b> To build and maintain muscle mass, ensure adequate protein intake from sources like dal, paneer, eggs, or lean meats with every meal.</li>
            <li><b>Heart Health:</b> Focus on a diet low in unhealthy fats and high in fiber (vegetables, whole grains) to keep your heart strong.</li>
            <li><b>Mind the Belly:</b> For many men, excess weight tends to accumulate around the abdomen. Consistent cardio and a clean diet are the best tools to manage this.</li>
        </ul>
        """
    else: # Prefer not to say / Other
        content = """
        <h4>A Holistic Approach to Your Health:</h4>
        <ul>
            <li><b>Listen to Your Body:</b> Your body gives you unique signals. Pay attention to your energy levels, sleep quality, and mood. These are your best indicators of health.</li>
            <li><b>Balanced Nutrition is Universal:</b> A diet rich in a variety of whole foods—vegetables, proteins, healthy fats, and complex carbs—is the foundation of good health for everyone.</li>
            <li><b>Consistency is Your Power:</b> Building a routine that you can stick with is more important than any single diet or workout.</li>
        </ul>
        """
    return f"{title}<div class='custom-box'>{content}</div>"

def get_stress_management_tips(name):
    title = f"<h3>🧘‍♀️ {name}, Let's Talk About Stress & Wellness</h3>"
    content = """
    <p>Stress is a normal part of life, but managing it is crucial for your health and weight management goals. High stress can lead to poor food choices and weight gain.</p>
    <h4>Simple Techniques to Find Your Calm:</h4>
    <ul>
        <li><b>5-Minute Breathing:</b> When feeling overwhelmed, sit quietly and focus on your breath. Inhale for 4 seconds, hold for 4, and exhale for 6. Repeat for 5 minutes.</li>
        <li><b>Digital Detox:</b> Try to set aside 30 minutes every day where you put your phone away. Go for a walk, listen to music, or just sit with your thoughts.</li>
        <li><b>Schedule 'Me-Time':</b> Just like a meeting, block out time in your calendar for a hobby or activity you love. It's non-negotiable!</li>
        <li><b>Get Quality Sleep:</b> Aim for 7-8 hours of sleep. A well-rested mind is a less-stressed mind. Poor sleep can seriously impact your health goals.</li>
    </ul>
    """
    return f"{title}<div class='custom-box'>{content}</div>"

# --- The App UI ---

st.title("✨ Welcome to Your Personal Wellness Coach!")
st.markdown("<h3>I'm here to guide you on your journey to a healthier, more confident you. Let's do this together!</h3>", unsafe_allow_html=True)

# --- Step 0: Collect User Info ---
if st.session_state.step == 0:
    with st.form("user_info_form"):
        st.header("First, Tell Me a Bit About Yourself")
        
        name = st.text_input("What is your name?", placeholder="e.g., Priya Sharma")
        gender = st.selectbox("What is your gender?", ("Female", "Male", "Prefer not to say / Other"))
        
        weight_option = st.radio("What's your current weight (in kg)?", ('Enter exact weight', 'Not sure, pick a range'), horizontal=True)
        weight = 0.0
        if weight_option == 'Enter exact weight':
            weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0, 0.5)
        else:
            weight_range = st.select_slider("Select your approximate weight range (kg)", ['30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100', '100+'], '60-70')
            weight = 105.0 if weight_range == '100+' else (int(weight_range.split('-')[0]) + int(weight_range.split('-')[1])) / 2.0
        
        height = st.number_input("What is your height (in cm)?", 100.0, 250.0, 165.0, 1.0)
        diet = st.selectbox("What is your dietary preference?", ("Vegetarian", "Eggetarian", "Non-Vegetarian"))
        living_situation = st.selectbox("How do you manage your meals?", 
            ("I live with family and eat what's cooked", 
             "I cook for myself / control my meals", 
             "I live in a PG/Hostel and eat from a mess"))
        
        submitted = st.form_submit_button("Preview My Plan!")
        
        if submitted:
            if not name:
                st.error("Please enter your name to continue.")
            else:
                st.session_state.user_data = {
                    "name": name, "weight": weight, "height": height, "diet": diet,
                    "living_situation": "With Family" if "family" in living_situation else ("PG/Hostel" if "PG/Hostel" in living_situation else "Cook Alone"),
                    "gender": gender
                }
                st.session_state.step = 1
                st.rerun()

# --- Step 1: Preview and Confirmation ---
elif st.session_state.step == 1:
    user = st.session_state.user_data
    st.session_state.bmi = calculate_bmi(user['weight'], user['height'])
    st.session_state.bmi_category = classify_bmi(st.session_state.bmi)
    name = user['name'].split(" ")[0]
    
    with st.spinner(f'Analyzing your details, {name}...'):
        time.sleep(1)

    st.header(f"Alright {name}, Here's Your Personalized Health Snapshot!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your BMI Analysis")
        st.metric(label="Your Body Mass Index (BMI) is", value=st.session_state.bmi)
        st.write(f"This places you in the **'{st.session_state.bmi_category}'** category.")
    
    with col2:
        st.subheader("My Message to You")
        if st.session_state.bmi_category == "Healthy Weight":
            st.success(f"**This is fantastic, {name}!** You're in a great place. Our goal is to help you feel strong, energized, and maintain this healthy balance.")
        else:
            st.warning(f"**Thank you for sharing, {name}.** Remember, this number is just a data point, not a definition of you. It gives us a starting line for an amazing journey of self-care we're about to begin together. I'm here with you!")

    st.info("This is a preview of your analysis. When you're ready, unlock your full plan below.")

    if st.button("Unlock My Full Personalized Plan"):
        st.session_state.step = 2
        st.rerun()

    if st.button("Start Over", key="start_over_preview"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# --- Step 2: The Full Plan ---
elif st.session_state.step == 2:
    user = st.session_state.user_data
    name = user['name'].split(" ")[0]
    
    st.header(f"Your Action Plan for a Healthier, More Confident You!")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🥗 Diet Plan", "🏃‍♀️ Workout Plan", "💡 Habits & Confidence", "🌟 Personalized Insights", "🧘‍♀️ Stress & Wellness"])

    with tab1: st.markdown(get_diet_recommendations(st.session_state.bmi_category, user['diet'], user['living_situation'], name), unsafe_allow_html=True)
    with tab2: st.markdown(get_workout_recommendations(st.session_state.bmi_category, name), unsafe_allow_html=True)
    with tab3: st.markdown(get_habit_and_confidence_tips(name), unsafe_allow_html=True)
    with tab4: st.markdown(get_gender_specific_tips(user['gender'], st.session_state.bmi_category, name), unsafe_allow_html=True)
    with tab5: st.markdown(get_stress_management_tips(name), unsafe_allow_html=True)

    st.divider()

    st.subheader("🔔 Motivational Reminders")
    if st.toggle("Enable motivational notifications"):
        st.success("Awesome! I'll be your cheerleader. Imagine getting friendly nudges like these:")
        st.info(f"Hey {name}, have you had a glass of water yet? Stay hydrated! 💧")
        st.info(f"You're doing great, {name}! Just a quick reminder that you are strong and capable. Keep going! 💪")

    if st.button("Start Over"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

