import streamlit as st
import time

# --- App Configuration ---
st.set_page_config(
    page_title="Your Personal Fitness Coach",
    page_icon="✨",
    layout="wide"
)

# --- Custom Styling (CSS) ---
# This injects custom CSS for a more vibrant, animated, and readable app.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    /* Main background and font */
    .stApp {
        background: linear-gradient(to right top, #d4fc79, #96e6a1);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Title style */
    h1 {
        color: #004d40; /* Dark Teal */
        font-weight: 700;
        text-align: center;
    }
    
    /* Subheader style */
    h2, h3 {
        color: #00695c; /* Medium Teal */
    }

    /* Style for form labels */
    .form-label {
        font-size: 1.4rem !important;
        font-weight: 600;
        color: #004d40;
    }

    /* Custom styled boxes for recommendations with fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .custom-box {
        background-color: #FFFFFF;
        border-left: 10px solid #ffca28; /* Amber accent */
        border-radius: 10px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        animation: fadeIn 0.5s ease-out forwards;
    }
    .custom-box p, .custom-box ul {
        font-size: 1.1rem;
        color: #37474F;
    }

    /* Style for the new target panel */
    .target-box {
        background: #00796b; /* Teal Background */
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .target-box h3 {
        color: white;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .target-box p {
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* Button style */
    .stButton>button {
        background-color: #ff6f00;
        color: white;
        border-radius: 25px;
        padding: 12px 24px;
        font-size: 1.2rem;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)


# --- State Management ---
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "", "weight": 0.0, "height": 0.0, "diet": "Vegetarian",
        "living_situation": "With Family", "gender": "Female"
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

# --- Content Generation Functions (Expanded & Gender-Specific) ---

def get_diet_recommendations(category, diet_type, gender, name):
    title = f"### 🥗 Namaste {name}, Here's Your Personalized Nutrition Guide!"
    base_info = f"""
    <div class="custom-box">
    <p>Based on your <b>{category}</b> status, here are meal ideas for your <b>{diet_type}</b> preference. The goal is to nourish your body and build a healthy relationship with food!</p>
    <h4>🌟 Golden Rules of Mindful Eating:</h4>
    <ul>
        <li><b>Stay Hydrated:</b> Aim for 2-3 litres of water daily. It's the simplest and most effective habit!</li>
        <li><b>Portion Smarts:</b> Use a smaller plate. Fill half with vegetables/salad, a quarter with protein (dal/paneer/chicken), and a quarter with carbs (rice/roti).</li>
        <li><b>Smart Snacking:</b> For mid-meal hunger, grab a fruit, a handful of chana, or a bowl of dahi.</li>
    </ul>
    </div>
    """
    
    specific_advice = ""
    # --- OVERWEIGHT/OBESE ---
    if category in ["Overweight", "Obese"]:
        if gender == "Female":
            specific_advice += "<h4>🎯 Your Focus: Hormonal Balance & Fat Loss</h4><p>We'll focus on nutrient-dense foods that support hormonal health and encourage sustainable fat loss.</p>"
            if diet_type == "Vegetarian":
                specific_advice += "<ul><li><b>Breakfast:</b> Moong dal chilla or a small bowl of oats upma. Focus on protein.</li><li><b>Lunch:</b> 1-2 multigrain rotis, a large bowl of dal (like spinach dal for iron), sabzi, and a big salad.</li><li><b>Dinner:</b> Keep it light. Vegetable khichdi, paneer bhurji, or lentil soup. Avoid carbs late at night.</li></ul>"
            else: # Eggetarian/Non-Veg
                specific_advice += "<ul><li><b>Breakfast:</b> 2 boiled eggs or an egg omelet with veggies.</li><li><b>Lunch:</b> Add grilled fish/chicken (100g) to your vegetarian meal for lean protein.</li><li><b>Dinner:</b> A simple egg/chicken curry with 1 roti or a large bowl of chicken soup.</li></ul>"
        else: # Male
            specific_advice += "<h4>🎯 Your Focus: Building Muscle & Reducing Fat</h4><p>We'll prioritize protein to build muscle, which boosts your metabolism and helps burn fat more effectively.</p>"
            if diet_type == "Vegetarian":
                specific_advice += "<ul><li><b>Breakfast:</b> Paneer sandwich (2 slices brown bread) or a large bowl of poha with peanuts.</li><li><b>Lunch:</b> 2-3 rotis, a large bowl of high-protein dal (chana/rajma), sabzi, salad, and a bowl of dahi.</li><li><b>Dinner:</b> Soya chunks curry or paneer tikka (baked) with a large salad.</li></ul>"
            else: # Eggetarian/Non-Veg
                specific_advice += "<ul><li><b>Breakfast:</b> 3-4 egg whites (omelet/bhurji).</li><li><b>Lunch:</b> 150g grilled chicken/fish, a large salad, a small portion of brown rice, and dal.</li><li><b>Dinner:</b> Chicken/fish curry (homestyle) with lots of veggies, avoid rice/roti if possible.</li></ul>"
    
    # --- UNDERWEIGHT ---
    elif category == "Underweight":
        if gender == "Female":
            specific_advice += "<h4>🎯 Your Focus: Healthy Weight Gain & Strength</h4><p>We'll use nutrient-dense foods to build strength and gain weight in a healthy manner.</p><ul><li>Add healthy fats: Ghee on rotis, nuts, and seeds as snacks.</li><li>Include paneer, potatoes, sweet potatoes, and bananas.</li><li>A glass of milk with a pinch of turmeric before bed is excellent.</li></ul>"
        else: # Male
            specific_advice += "<h4>🎯 Your Focus: Muscle Gain & Calorie Surplus</h4><p>We need a healthy calorie surplus with a focus on protein to build muscle mass.</p><ul><li>Increase portion sizes for all meals.</li><li>Incorporate protein-rich snacks like a paneer sandwich, boiled eggs, or a chicken roll.</li><li>Add peanut butter to shakes or with brown bread. Sweet potato is your friend!</li></ul>"

    # --- HEALTHY WEIGHT ---
    else:
        specific_advice = f"<h4>🎯 Your Focus: Maintenance & Vitality</h4><p>You're doing great, {name}! Let's focus on maintaining this balance with variety and whole foods to keep you energized.</p><ul><li>Ensure a good mix of protein (dal, paneer, eggs, chicken), complex carbs (roti, brown rice), and colorful vegetables in every meal.</li></ul>"

    return f"{title}{base_info}<div class='custom-box'>{specific_advice}</div>"


def get_workout_recommendations(category, gender, name):
    title = f"### 🏃‍♀️ {name}, Let's Get Moving and Feel Amazing!"
    content = ""
    # --- OVERWEIGHT/OBESE ---
    if category in ["Overweight", "Obese"]:
        if gender == "Female":
            content = """
            <h4>Your Goal: Consistency & Stamina</h4>
            <p>Our focus is on building a consistent routine with activities that are gentle on the joints but effective for fat loss.</p>
            <ul>
                <li><b>Cardio (4-5 days/week):</b> Start with 30-45 minutes of brisk walking. You can also try cycling or Zumba for a fun alternative.</li>
                <li><b>Strength (2 days/week):</b> Bodyweight exercises are perfect. Try 3 sets of 12 reps of:
                    <ul><li>Chair Squats</li><li>Wall Push-ups</li><li>Glute Bridges</li></ul></li>
                <li><b>Flexibility:</b> Gentle stretching or beginner Yoga (like Surya Namaskar) daily.</li>
            </ul>
            """
        else: # Male
            content = """
            <h4>Your Goal: Burn Fat & Build a Strong Foundation</h4>
            <p>We'll combine cardio for fat loss with strength training to build muscle, which will supercharge your metabolism.</p>
            <ul>
                <li><b>Cardio (3-4 days/week):</b> Aim for 30 minutes of jogging, cycling, or skipping. High-Intensity Interval Training (HIIT) for 15-20 mins is also very effective.</li>
                <li><b>Strength (3 days/week):</b> Focus on compound movements. Try 3 sets of 10-12 reps of:
                    <ul><li>Bodyweight Squats</li><li>Push-ups (on knees if needed)</li><li>Plank (hold for 30-60 seconds)</li><li>Lunges</li></ul></li>
            </ul>
            """
    # --- UNDERWEIGHT ---
    elif category == "Underweight":
        content = """
        <h4>Your Goal: Build Muscle & Strength</h4>
        <p>The focus here is less on intense cardio and more on resistance training to build healthy muscle mass.</p>
        <ul>
            <li><b>Strength Training (3-4 days/week):</b> This is your priority. Focus on compound exercises like squats, push-ups, and lunges. If you have access to a gym, basic weight training is highly recommended.</li>
            <li><b>Light Cardio (1-2 days/week):</b> A 20-30 minute walk or a light jog is enough to keep your heart healthy without burning too many calories.</li>
        </ul>
        """
    # --- HEALTHY WEIGHT ---
    else:
        content = f"""
        <h4>Your Goal: Maintain Fitness & Feel Great, {name}!</h4>
        <p>You are in a great spot! Let's keep things interesting to ensure you stay consistent and strong.</p>
        <ul>
            <li><b>Your Routine:</b> Aim for 3-5 days of activity per week.</li>
            <li><b>Mix it Up:</b> A mix of cardio (running, swimming), strength (yoga, bodyweight exercises, gym), and a sport you enjoy (like badminton or cricket) is ideal to keep you motivated and fit.</li>
        </ul>
        """
    return f"{title}<div class='custom-box'>{content}</div>"


def get_habit_and_confidence_tips(name):
    title = f"### 💡 {name}, Let's Build Habits for a Confident You!"
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

# --- The App UI ---

st.title("✨ Welcome to Your Personal Wellness Coach!")
st.markdown("<h3>I'm here to guide you on your journey to a healthier, more confident you. Let's do this together!</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- Step 1: Collect User Info ---
if st.session_state.step == 0:
    with st.form("user_info_form"):
        st.header("First, Tell Me a Bit About Yourself")
        
        st.markdown('<p class="form-label">What is your name?</p>', unsafe_allow_html=True)
        name = st.text_input("Name", placeholder="e.g., Priya Sharma", label_visibility="collapsed")
        
        st.markdown('<p class="form-label">What is your gender?</p>', unsafe_allow_html=True)
        gender = st.selectbox("Gender", ("Female", "Male"), label_visibility="collapsed")
        
        st.markdown('<p class="form-label">What is your current weight (in kg)?</p>', unsafe_allow_html=True)
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 65.0, 0.5, label_visibility="collapsed")
        
        st.markdown('<p class="form-label">What is your height (in cm)?</p>', unsafe_allow_html=True)
        height = st.number_input("Height (cm)", 100.0, 250.0, 165.0, 1.0, label_visibility="collapsed")
        
        st.markdown('<p class="form-label">What is your dietary preference?</p>', unsafe_allow_html=True)
        diet = st.selectbox("Diet", ("Vegetarian", "Eggetarian", "Non-Vegetarian"), label_visibility="collapsed")
        
        st.markdown('<p class="form-label">How do you manage your meals?</p>', unsafe_allow_html=True)
        living_situation = st.selectbox("Meals", 
            ("I live with family and eat what's cooked", 
             "I cook for myself / control my meals", 
             "I live in a PG/Hostel and eat from a mess"), label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Create My Personalized Plan!")
        
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

# --- Step 2: Analyze and Show Plan ---
elif st.session_state.step == 1:
    user = st.session_state.user_data
    st.session_state.bmi = calculate_bmi(user['weight'], user['height'])
    st.session_state.bmi_category = classify_bmi(st.session_state.bmi)
    name = user['name'].split(" ")[0]
    
    with st.spinner(f'Crafting a personalized plan just for you, {name}...'):
        time.sleep(2)
    
    st.balloons() # Animation!
    
    st.header(f"Alright {name}, Here's Your Personalized Health Snapshot!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Your BMI Analysis")
        st.metric(label="Your Body Mass Index (BMI) is", value=st.session_state.bmi)
        st.write(f"This places you in the **'{st.session_state.bmi_category}'** category.")
    
    with col2:
        st.subheader("Your 20-Day Target")
        target_message = ""
        target_weight = 0
        if st.session_state.bmi_category in ["Overweight", "Obese"]:
            target_weight = user['weight'] - 2
            target_message = f"A healthy goal for the next 20 days is to aim for **{target_weight:.1f} kg**."
        elif st.session_state.bmi_category == "Underweight":
            target_weight = user['weight'] + 2
            target_message = f"A healthy goal for the next 20 days is to aim for **{target_weight:.1f} kg**."
        else:
            target_message = f"Your goal is to maintain your current weight of **{user['weight']:.1f} kg** and build strength."
        
        st.markdown(f'<div class="target-box"><h3>🎯 Your Achievable Goal</h3><p>{target_message}</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.header(f"Your Action Plan for a Healthier, More Confident You!")
    
    tab1, tab2, tab3 = st.tabs(["🥗 Diet Plan", "🏃‍♀️ Workout Plan", "💡 Habits & Confidence"])

    with tab1: st.markdown(get_diet_recommendations(st.session_state.bmi_category, user['diet'], user['gender'], name), unsafe_allow_html=True)
    with tab2: st.markdown(get_workout_recommendations(st.session_state.bmi_category, user['gender'], name), unsafe_allow_html=True)
    with tab3: st.markdown(get_habit_and_confidence_tips(name), unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
