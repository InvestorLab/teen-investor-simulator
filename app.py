import streamlit as st
import yfinance as yf
import pandas as pd
import copy
import uuid
from supabase import create_client

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------

st.set_page_config(
    page_title="Teen Investor Simulator",
    layout="centered"
)
st.markdown("""
<style>

/* Main page */
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #f3f0ff 100%);
}

/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Headings */
h1, h2, h3 {
    color: #1f2937;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #f7f9fc;
    border-right: 1px solid #e5e7eb;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0px 6px 16px rgba(99, 102, 241, 0.25);
}

/* Metric cards */
div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.06);
}

/* Radio options */
div[role="radiogroup"] > label {
    background: white;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    border: 1px solid #e5e7eb;
}

/* Info boxes */
div[data-testid="stAlert"] {
    border-radius: 14px;
}
.level-card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #E5E7EB;
    min-height: 245px;
    transition: all 0.25s ease;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.04);
}

.level-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 14px 30px rgba(79,70,229,0.12);
    border-color: #C7D2FE;
}

.level-icon {
    font-size: 38px;
    margin-bottom: 15px;
}

.level-number {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #6366F1;
}

.skill-tag {
    display: inline-block;
    background: #EEF2FF;
    color: #4F46E5;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}
/* Achievement cards */
.achievement-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 12px;
    min-height: 145px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.04);
}

.achievement-card.unlocked {
    border: 2px solid #6366F1;
    background: linear-gradient(135deg, #FFFFFF, #F5F3FF);
}

.achievement-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.achievement-title {
    font-size: 16px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 5px;
}

.achievement-description {
    font-size: 13px;
    color: #6B7280;
    margin-bottom: 12px;
}

.achievement-unlocked {
    font-size: 11px;
    font-weight: 700;
    color: #4F46E5;
    letter-spacing: 1px;
}

.achievement-locked {
    font-size: 11px;
    font-weight: 700;
    color: #9CA3AF;
    letter-spacing: 1px;
}
/* -------------------------------------------------
   HOME PROGRESS CARDS
------------------------------------------------- */


.progress-card {
    background: rgba(255, 255, 255, 0.88);
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 22px;
    min-height: 290px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.045);
    transition: all 0.25s ease;
}


.progress-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 26px rgba(79,70,229,0.10);
    border-color: #C7D2FE;
}


.progress-card-icon {
    font-size: 30px;
    margin-bottom: 8px;
}


.progress-card-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.4px;
    color: #6366F1;
    margin-bottom: 6px;
}


.progress-card-title {
    font-size: 21px;
    font-weight: 700;
    color: #111827;
    margin-bottom: 18px;
}


.progress-item {
    font-size: 15px;
    color: #374151;
    margin: 11px 0;
    line-height: 1.45;
}


.progress-complete {
    color: #059669;
}


.progress-locked {
    color: #9CA3AF;
}


.progress-active {
    color: #4F46E5;
    font-weight: 600;
}


.progress-summary {
    margin-top: 22px;
    margin-bottom: 8px;
    font-size: 14px;
    color: #6B7280;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

default_values = {
    "panic_resistance": 5,
    "fomo_resistance": 5,
    "diversification": 5,
    "risk_awareness": 5,
    "long_term_thinking": 5,

    "level1_complete": False,
    "level2_complete": False,
    "level3_complete": False,

    "module1_complete": False,
"module1_score": 0,
"module2_complete": False,
"module2_score": 0,

"module3_complete": False,
"module3_score": 0,

"module4_complete": False,
"module4_score": 0,
"module5_complete": False,
"module5_score": 0,
    "choice1": None,
    "choice1_reason": None,
    "choice2": None,
    "choice3": None,
    "trade_history": [],
    "market_cash": 10000.0,
    "achievements": [],
"market_week": 1,

"market_prices": {
    "TechCore": 100.0,
    "GreenGrid": 80.0,
    "HealthPlus": 60.0,
    "RetailCo": 40.0,
    "Bond Fund": 100.0
},

"market_holdings": {
    "TechCore": 0.0,
    "GreenGrid": 0.0,
    "HealthPlus": 0.0,
    "RetailCo": 0.0,
    "Bond Fund": 0.0
},

"market_news": "The simulated market is open.",
"market_history": [10000.0],

"benchmark_history": [10000.0],

"market_last_changes": {
    "TechCore": 0.0,
    "GreenGrid": 0.0,
    "HealthPlus": 0.0,
    "RetailCo": 0.0,
    "Bond Fund": 0.0
}
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value
# -------------------------------------------------
# ANALYTICS
# -------------------------------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if "analytics_session_id" not in st.session_state:
    st.session_state.analytics_session_id = str(uuid.uuid4())


def log_event(event_name, event_value=None):
    try:
        response = supabase.table("events").insert(
    {
        "session_id": st.session_state.analytics_session_id,
        "event_name": event_name,
        "event_value": event_value
    },
    returning="minimal"
).execute()

    

    except Exception as e:
        print("Analytics error:", e)
if "session_logged" not in st.session_state:
    log_event("session_started")
    st.session_state.session_logged = True
# -------------------------------------------------
# DOWNLOAD HISTORICAL DATA
# -------------------------------------------------

@st.cache_data
def get_history(ticker, start, end):
    stock = yf.Ticker(ticker)
    data = stock.history(
        start=start,
        end=end,
        auto_adjust=True
    )

    return data


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def clamp_scores():
    score_names = [
        "panic_resistance",
        "fomo_resistance",
        "diversification",
        "risk_awareness",
        "long_term_thinking"
    ]

    for score in score_names:
        st.session_state[score] = max(
            0,
            min(10, st.session_state[score])
        )


def score_bar(score):
    return "█" * score + "░" * (10 - score)


def reset_game():
    for key, value in default_values.items():
        st.session_state[key] = copy.deepcopy(value)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.image("investor_lab_logo.png", width=260)

sidebar_options = [
    "Home",
    "Learn: Market Crashes",
    "Learn: FOMO",
    "Learn: Diversification",
    "Learn: Researching a Company",
    "Learn: News & Markets",
    "Level 1: The Crash"
]
if st.session_state.level1_complete:
    sidebar_options.append("Level 2: FOMO")
else:
    sidebar_options.append("LOCKED - Level 2: FOMO")

if st.session_state.level2_complete:
    sidebar_options.append("Level 3: Diversification")
else:
    sidebar_options.append("LOCKED - Level 3: Diversification")


sidebar_options.append("Market Mode")

sidebar_options.append("Investor Profile")

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"
if "pending_page" in st.session_state:
    st.session_state.nav_page = st.session_state.pending_page
    del st.session_state.pending_page

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"
page = st.sidebar.radio(
    "Choose a section",
    sidebar_options,
    key="nav_page"
)
if page == "LOCKED - Level 2: FOMO":
    st.title("Level 2: FOMO")
    st.warning("Complete Level 1 first to unlock this level.")
    st.stop()

if page == "LOCKED - Level 3: Diversification":
    st.title("Level 3: Diversification")
    st.warning("Complete Level 2 first to unlock this level.")
    st.stop()
# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

if page == "Home":

    st.title("Investor Lab: Teen Investor Simulator")

    st.write(
        "Learn investing through interactive lessons, real historical market "
        "scenarios, and a simulated portfolio (without risking real money)."
    )

    if st.button(
        "Start Learning →",
        type="primary",
        use_container_width=True
    ):
        log_event("program_started")
        st.session_state.pending_page = "Learn: Market Crashes"
        st.rerun()
 # progress stuff
    # achievements stuff


    # -------------------------------------------------
    # PROGRESSION SYSTEM
    # -------------------------------------------------

    st.subheader("Your Progress")

    completed_steps = 0
    total_steps = 10

    module_states = [
        st.session_state.module1_complete,
        st.session_state.module2_complete,
        st.session_state.module3_complete,
        st.session_state.module4_complete,
        st.session_state.module5_complete,
    ]

    level_states = [
        st.session_state.level1_complete,
        st.session_state.level2_complete,
        st.session_state.level3_complete,
    ]

    completed_steps += sum(module_states)
    completed_steps += sum(level_states)

    if st.session_state.market_week >= 12:
        completed_steps += 1

    final_report_complete = (
        all(module_states)
        and all(level_states)
        and st.session_state.market_week >= 12
    )

    if final_report_complete:
        completed_steps += 1

    def progress_item(label, complete=False, locked=False, active=False):
        if complete:
            css_class = "progress-complete"
            icon = "✅"
        elif locked:
            css_class = "progress-locked"
            icon = "🔒"
        elif active:
            css_class = "progress-active"
            icon = "●"
        else:
            css_class = ""
            icon = "⬜"

        return (
            f'<div class="progress-item {css_class}">'
            f'{icon} {label}'
            f'</div>'
        )

    # -------------------------------------------------
    # LEARN CARD
    # -------------------------------------------------

    learn_html = ""
    learn_html += progress_item(
        "Market Crashes",
        complete=st.session_state.module1_complete
    )
    learn_html += progress_item(
        "FOMO & Emotional Investing",
        complete=st.session_state.module2_complete
    )
    learn_html += progress_item(
        "Diversification & Risk",
        complete=st.session_state.module3_complete
    )
    learn_html += progress_item(
        "Researching a Company",
        complete=st.session_state.module4_complete
    )
    learn_html += progress_item(
        "News & Markets",
        complete=st.session_state.module5_complete
    )

    # -------------------------------------------------
    # PRACTICE CARD
    # -------------------------------------------------

    practice_html = ""
    practice_html += progress_item(
        "Survive the Crash",
        complete=st.session_state.level1_complete,
        locked=not st.session_state.module1_complete
    )
    practice_html += progress_item(
        "Fight the FOMO",
        complete=st.session_state.level2_complete,
        locked=not st.session_state.level1_complete
    )
    practice_html += progress_item(
        "Diversification Challenge",
        complete=st.session_state.level3_complete,
        locked=not st.session_state.level2_complete
    )

    # -------------------------------------------------
    # SIMULATION CARD
    # -------------------------------------------------

    if st.session_state.market_week >= 12:
        market_html = progress_item(
            "12-Week Simulation Complete",
            complete=True
        )
    else:
        market_html = progress_item(
            f"Week {st.session_state.market_week} of 12",
            active=True
        )

    profile_html = progress_item(
        "Investor Profile",
        complete=final_report_complete,
        locked=not final_report_complete
    )

    # -------------------------------------------------
    # DISPLAY PROGRESS CARDS
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="progress-card">
                <div class="progress-card-icon">📚</div>
                <div class="progress-card-label">LEARN</div>
                <div class="progress-card-title">Build Your Knowledge</div>
                {learn_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="progress-card">
                <div class="progress-card-icon">🎯</div>
                <div class="progress-card-label">PRACTICE</div>
                <div class="progress-card-title">Test Your Decisions</div>
                {practice_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="progress-card">
                <div class="progress-card-icon">📈</div>
                <div class="progress-card-label">SIMULATE</div>
                <div class="progress-card-title">Run the Market</div>
                {market_html}
                {profile_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------------------------
    # OVERALL PROGRESS
    # -------------------------------------------------

    progress = completed_steps / total_steps

    st.markdown(
        '<div class="progress-summary">Overall progress</div>',
        unsafe_allow_html=True
    )
    st.progress(progress)
    st.caption(f"{completed_steps} of {total_steps} stages complete")

    st.divider()

    # -------------------------------------------------
    # ACHIEVEMENTS
    # -------------------------------------------------

    st.subheader("Achievements")

    achievement_list = {
        "First Trade": {
            "icon": "🏅",
            "description": "Make your first trade"
        },
        "Diversifier": {
            "icon": "🌐",
            "description": "Own at least 3 investments"
        },
        "Market Beater": {
            "icon": "📈",
            "description": "Finish Market Mode above the market"
        },
        "Risk Manager": {
            "icon": "🛡️",
            "description": "Keep your largest position at 50% or less"
        },
        "Investor Lab Graduate": {
            "icon": "🎓",
            "description": "Complete Investor Lab"
        }
    }

    achievement_cols = st.columns(3)

    for i, (name, info) in enumerate(achievement_list.items()):
        unlocked = name in st.session_state.achievements

        if unlocked:
            card_class = "achievement-card unlocked"
            status_class = "achievement-unlocked"
            status = "✓ UNLOCKED"
        else:
            card_class = "achievement-card"
            status_class = "achievement-locked"
            status = "🔒 LOCKED"

        with achievement_cols[i % 3]:
            html = (
                f'<div class="{card_class}">'
                f'<div class="achievement-icon">{info["icon"]}</div>'
                f'<div class="achievement-title">{name}</div>'
                f'<div class="achievement-description">{info["description"]}</div>'
                f'<div class="{status_class}">{status}</div>'
                f'</div>'
            )

            st.markdown(
                html,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("About Investor Lab")

    st.write(
        """
        Investor Lab is a student-created financial literacy project designed to help
        teenagers learn investing through experience rather than memorization.

        Students learn core investing concepts, make decisions during real historical
        market events, and apply what they learn in an interactive market simulation,
        without getting lost in complicated financial jargon.

        Investor Lab is free to use and is designed for educational purposes only.
        """
    )
# -------------------------------------------------
# MODULE 1 — MARKET CRASHES
# -------------------------------------------------

if page == "Learn: Market Crashes":

    st.title("Module 1: Market Crashes")

    st.write(
        """
        Before you survive your first market crash,
        let's learn what actually happens when markets fall.
        """
    )

    st.divider()

    st.subheader("1. What is a market crash?")

    st.write(
        """
        A market crash is a large and rapid decline in stock prices.

        Crashes can happen because investors become worried about things like:

        - recessions
        - wars
        - financial crises
        - pandemics
        - unexpected economic events

        When many investors try to sell at the same time,
        prices can fall very quickly.
        """
    )

    st.subheader("2. What is a drawdown?")

    st.write(
        """
        A **drawdown** measures how far an investment has fallen
        from its previous highest value.

        Example:

        You invest **$1,000**.

        Your investment grows to **$1,200**.

        Then it falls to **$900**.

        The drop from $1,200 to $900 is a **25% drawdown**.
        """
    )

    st.subheader("3. Temporary loss vs. permanent loss")

    st.write(
        """
        Seeing your portfolio fall does not always mean the loss is permanent.

        If your investment falls from $1,000 to $700,
        its current value is lower.

        But if you immediately sell at $700,
        you lock in that loss.

        If the investment later recovers and you stayed invested,
        the decline may have only been temporary.
        """
    )

    st.warning(
        """
        This does NOT mean you should always hold every investment.

        The important question is:

        **Did the reason you invested change, or are you reacting only because the price fell?**
        """
    )

    st.divider()

    st.header("Quick Quiz")

    q1 = st.radio(
        "1. Your $1,000 investment falls to $750. What is the approximate decline?",
        [
            "10%",
            "25%",
            "50%",
            "75%"
        ],
        key="module1_q1"
    )

    q2 = st.radio(
        "2. Which is the best reason to reconsider an investment?",
        [
            "The price fell yesterday",
            "Your friends are selling",
            "The original reason you invested is no longer true",
            "You saw scary headlines"
        ],
        key="module1_q2"
    )

    if st.button("Submit Quiz", key="module1_submit"):

        score = 0

        if q1 == "25%":
            score += 1

        if q2 == "The original reason you invested is no longer true":
            score += 1

        st.session_state.module1_score = score

        if score == 2:
            st.success("🎉 2/2 — Great job!")
            st.session_state.module1_complete = True
            log_event("module_completed", "Market Crashes")
        elif score == 1:
            st.warning("You got 1/2. Review the lesson and try again.")

        else:
            st.error("You got 0/2. Review the lesson and try again.")

    if st.session_state.module1_complete:

        st.divider()

        st.success("✅ Module Complete")

        st.write(
            f"Knowledge Score: {st.session_state.module1_score}/2"
        )

        st.write(
            """
            You're ready to test what you learned during a real historical crash.
            """
        )

        st.info("Next: Level 1 — Survive the Crash")


# -------------------------------------------------
# MODULE 2 — FOMO & EMOTIONAL INVESTING
# -------------------------------------------------

elif page == "Learn: FOMO":

    st.title("Module 2: FOMO & Emotional Investing")

    st.write(
        """
        Investors do not always make decisions based only on facts.

        Emotions, recent price movements, social media, and what other
        people are doing can influence investment decisions.
        """
    )

    st.divider()

    # -------------------------------------------------
    # SECTION 1
    # -------------------------------------------------

    st.subheader("1. What is FOMO?")

    st.write(
        """
        **FOMO** means **Fear Of Missing Out**.

        In investing, FOMO can happen when you see an investment rising
        quickly and become afraid that everyone else is making money
        while you are missing the opportunity.

        This can make someone buy an investment mainly because its price
        has recently increased.
        """
    )

    st.info(
        """
        Example:

        TechCore rises 25% in three weeks.

        Your friends are buying it and people online are talking about it.

        You suddenly feel like you need to buy before the price goes even higher.

        That feeling is FOMO.
        """
    )

    # -------------------------------------------------
    # SECTION 2
    # -------------------------------------------------

    st.subheader("2. Why can FOMO be dangerous?")

    st.write(
        """
        A rising price does not automatically mean an investment is a good value.

        When investors chase an investment only because it has recently gone up,
        they may:

        - buy after a large price increase
        - ignore the company's risks
        - invest more money than they normally would
        - become too concentrated in one investment
        """
    )

    st.warning(
        """
        A better question is not:

        **"Is everyone else buying?"**

        It is:

        **"Why do I believe this investment is worth owning?"**
        """
    )

    # -------------------------------------------------
    # SECTION 3
    # -------------------------------------------------

    st.subheader("3. Other emotional investing mistakes")

    st.write(
        """
        FOMO is only one example of how emotions can affect investing.

        **Panic selling**
        Selling mainly because prices are falling and you are scared.

        **Herd behavior**
        Copying what other investors are doing without doing your own research.

        **Recency bias**
        Assuming something that has performed well recently will continue
        performing well.

        **Overconfidence**
        Believing you can predict investment outcomes more accurately than
        you actually can.
        """
    )

    st.divider()

    # -------------------------------------------------
    # QUIZ
    # -------------------------------------------------

    st.header("Quick Quiz")

    q1 = st.radio(
        "1. Which situation is the best example of FOMO?",
        [
            "Researching a company's debt before buying",
            "Buying a stock mainly because everyone is talking about it",
            "Holding a diversified portfolio",
            "Comparing two companies' profit margins"
        ],
        key="module2_q1"
    )

    q2 = st.radio(
        "2. A stock has risen 30% recently. What is the best next step?",
        [
            "Buy immediately before it rises more",
            "Put all your money into it",
            "Research why it has risen and whether the investment still makes sense",
            "Buy because your friends bought it"
        ],
        key="module2_q2"
    )

    q3 = st.radio(
        "3. What is herd behavior?",
        [
            "Investing for the long term",
            "Buying several different investments",
            "Copying what other investors are doing without doing your own research",
            "Selling an investment because its business has weakened"
        ],
        key="module2_q3"
    )

    if st.button(
        "Submit Quiz",
        key="module2_submit"
    ):

        score = 0

        if q1 == "Buying a stock mainly because everyone is talking about it":
            score += 1

        if q2 == "Research why it has risen and whether the investment still makes sense":
            score += 1

        if q3 == "Copying what other investors are doing without doing your own research":
            score += 1

        st.session_state.module2_score = score

        if score == 3:

            st.success("🎉 3/3 — Great job!")

            st.session_state.module2_complete = True
            log_event("module_completed", "FOMO & Emotional Investing")

        elif score == 2:

            st.warning(
                "You got 2/3. Review the lesson and try again."
            )

        else:

            st.error(
                f"You got {score}/3. Review the lesson and try again."
            )

    if st.session_state.module2_complete:

        st.divider()

        st.success("✅ Module Complete")

        st.write(
            f"Knowledge Score: {st.session_state.module2_score}/3"
        )

        st.info(
            "Next: Level 2 — Fight the FOMO"
        )

# -------------------------------------------------
# MODULE 3 — DIVERSIFICATION & RISK
# -------------------------------------------------

elif page == "Learn: Diversification":

    st.title("Module 3: Diversification & Risk")

    st.write(
        """
        Diversification means spreading your money across different investments
        instead of depending too heavily on just one.

        The goal is not to eliminate risk.

        The goal is to reduce the damage that one bad investment can cause
        to your entire portfolio.
        """
    )

    st.divider()

    # -------------------------------------------------
    # SECTION 1
    # -------------------------------------------------

    st.subheader("1. What is concentration risk?")

    st.write(
        """
        **Concentration risk** happens when too much of your money is invested
        in one company or one type of investment.

        Example:

        You have **$10,000** and invest all of it in TechCore.

        If TechCore falls **30%**, your portfolio falls from:

        **$10,000 → $7,000**
        """
    )

    st.warning(
        """
        The more dependent your portfolio is on one investment,
        the more damage that investment can cause if it performs badly.
        """
    )

    # -------------------------------------------------
    # SECTION 2
    # -------------------------------------------------

    st.subheader("2. How does diversification help?")

    st.write(
        """
        Now imagine instead that you divide your $10,000 across four investments:

        - $2,500 in TechCore
        - $2,500 in HealthPlus
        - $2,500 in RetailCo
        - $2,500 in a Bond Fund

        If TechCore falls 30%, only part of your portfolio is directly affected.

        Your entire portfolio does **not** automatically fall 30%.
        """
    )

    st.info(
        """
        Diversification reduces how dependent your portfolio is
        on the success or failure of one investment.
        """
    )

    # -------------------------------------------------
    # SECTION 3
    # -------------------------------------------------

    st.subheader("3. Diversification does not remove all risk")

    st.write(
        """
        Diversification can reduce company-specific risk,
        but it cannot protect you from every possible loss.

        During major market declines, many investments can fall at the same time.

        Different investments can also react differently to economic events.

        For example:

        - technology stocks may be more sensitive to interest rates
        - retail companies may be more sensitive to consumer spending
        - healthcare may have more stable demand
        - bonds may behave differently from stocks
        """
    )

    st.warning(
        """
        Diversification is about managing risk,
        not guaranteeing profits.
        """
    )

    # -------------------------------------------------
    # SECTION 4
    # -------------------------------------------------

    st.subheader("4. Correlation and Diversification")

    st.write(
        """
        Owning several investments does **not automatically**
        mean your portfolio is well diversified.

        Another important idea is **correlation**.

        Correlation describes how closely two investments
        tend to move together.
        """
    )

    st.write(
        """
        **High positive correlation**

        Two investments often rise and fall together.

        **Low correlation**

        The investments do not consistently move together.

        **Negative correlation**

        The investments tend to move in opposite directions.
        """
    )

    st.info(
        """
        Imagine you own four different technology stocks.

        You technically own four companies, but they may all react
        similarly to interest rates, technology spending, or problems
        affecting the technology industry.

        Your portfolio may look diversified on paper while still
        being exposed to many of the same risks.
        """
    )

    st.write(
        """
        Compare that with a portfolio containing:

        - Technology
        - Healthcare
        - Consumer companies
        - Bonds

        These investments may respond differently to the same
        economic event.

        That can make diversification more effective.
        """
    )

    st.warning(
        """
        **The goal is not necessarily to find investments that always
        move in opposite directions.**

        Even investments with low or moderate correlation can improve
        diversification.

        The important idea is to avoid having everything in your
        portfolio move almost exactly the same way.
        """
    )

    st.success(
        """
        **Key idea:**

        Good diversification is not just about how many investments
        you own.

        It is also about owning investments that are exposed to
        different risks and do not all behave the same way.
        """
    )

    st.divider()

    # -------------------------------------------------
    # QUIZ
    # -------------------------------------------------


    st.header("Quick Quiz")

    q1 = st.radio(
        "1. What is concentration risk?",
        [
            "Owning several different investments",
            "Having too much of your portfolio in one investment",
            "Keeping some money in cash",
            "Investing for the long term"
        ],
        key="module3_q1"
    )

    q2 = st.radio(
        "2. What is the main benefit of diversification?",
        [
            "It guarantees that you will make money",
            "It eliminates all investment risk",
            "It reduces how dependent your portfolio is on one investment",
            "It makes every investment rise at the same time"
        ],
        key="module3_q2"
    )

    q3 = st.radio(
        "3. Which portfolio is the most diversified?",
        [
            "100% TechCore",
            "80% TechCore and 20% cash",
            "50% TechCore and 50% GreenGrid",
            "25% TechCore, 25% HealthPlus, 25% RetailCo, 25% Bond Fund"
        ],
        key="module3_q3"
    )
    q4 = st.radio(
        "4. Why might owning four technology stocks still provide limited diversification?",
        [
            "Owning four stocks is always poorly diversified",
            "Technology stocks can be highly correlated and react to many of the same risks",
            "Stocks cannot be diversified",
            "Diversification only works with bonds"
        ],
        key="module3_q4"
    )

    if st.button(
        "Submit Quiz",
        key="module3_submit"
    ):

        score = 0

        if q1 == "Having too much of your portfolio in one investment":
            score += 1

        if q2 == "It reduces how dependent your portfolio is on one investment":
            score += 1

        if q3 == "25% TechCore, 25% HealthPlus, 25% RetailCo, 25% Bond Fund":
            score += 1
        if q4 == "Technology stocks can be highly correlated and react to many of the same risks":
            score += 1
        st.session_state.module3_score = score

        if score == 4:

            st.success("🎉 4/4 — Great job!")

            st.session_state.module3_complete = True
            log_event("module_completed", "Diversification & Risk")

        elif score == 2:

            st.warning(
                "You got 2/4. Review the lesson and try again."
            )

        else:

            st.error(
                f"You got {score}/4. Review the lesson and try again."
            )

    if st.session_state.module3_complete:

        st.divider()

        st.success("✅ Module Complete")

        st.write(
            f"Knowledge Score: {st.session_state.module3_score}/4"
        )

        st.info(
            "Next: Level 3 — Diversification Challenge"
        )

# -------------------------------------------------
# MODULE 4 — RESEARCHING A COMPANY
# -------------------------------------------------

elif page == "Learn: Researching a Company":

    st.title("Module 4: Researching a Company")

    st.write(
        """
        Before buying a stock, investors often look at the company's
        business and financial characteristics.

        No single number tells you whether an investment is good or bad.

        The goal is to look at several factors together.
        """
    )

    st.divider()

    # -------------------------------------------------
    # SECTION 1
    # -------------------------------------------------

    st.subheader("1. Revenue Growth")

    st.write(
        """
        **Revenue** is the money a company earns from selling its
        products or services.

        **Revenue growth** measures how quickly those sales are increasing.

        Example:

        A company's revenue grows from $100 million to $120 million.

        That is approximately **20% revenue growth**.
        """
    )

    st.info(
        """
        Fast revenue growth can be a positive sign,
        but high growth does not automatically make a stock a good investment.
        """
    )

    # -------------------------------------------------
    # SECTION 2
    # -------------------------------------------------

    st.subheader("2. Profit Margin")

    st.write(
        """
        **Profit margin** tells you how much of a company's revenue
        becomes profit.

        Example:

        A company earns **$100 million in revenue**
        and keeps **$15 million as profit**.

        Its profit margin is approximately **15%**.
        """
    )

    st.write(
        """
        A higher profit margin can mean the company keeps more money
        from each dollar of sales.
        """
    )

    # -------------------------------------------------
    # SECTION 3
    # -------------------------------------------------

    st.subheader("3. Debt")

    st.write(
        """
        Companies sometimes borrow money to expand their businesses.

        Debt is not automatically bad.

        However, a company with a lot of debt may have more difficulty
        if interest rates rise or its profits fall.
        """
    )

    st.warning(
        """
        High debt can increase financial risk,
        especially during difficult economic conditions.
        """
    )

    # -------------------------------------------------
    # SECTION 4
    # -------------------------------------------------

    st.subheader("4. Valuation")

    st.write(
        """
        **Valuation** refers to how expensive an investment is
        compared with the business investors are buying.

        A strong company can still be a risky investment
        if investors are paying an extremely high price for it.

        Likewise, a cheap stock is not automatically a good investment.
        """
    )

    st.info(
        """
        A useful question is:

        **Does the company's growth and profitability justify its valuation?**
        """
    )

    # -------------------------------------------------
    # SECTION 5
    # -------------------------------------------------

    st.subheader("5. Putting the information together")

    st.write(
        """
        Imagine TechCore has:

        - Revenue Growth: 24%
        - Profit Margin: 18%
        - Debt: Low
        - Valuation: Expensive
        - Risk: High

        There are both strengths and risks.

        Strong growth and margins may be attractive,
        while an expensive valuation could mean investors already
        expect a lot from the company.
        """
    )

    st.warning(
        """
        Investing decisions usually involve trade-offs.

        You should not look at only one number.
        """
    )

    st.divider()

    # -------------------------------------------------
    # QUIZ
    # -------------------------------------------------

    st.header("Quick Quiz")

    q1 = st.radio(
        "1. What does revenue growth measure?",
        [
            "How quickly a company's sales are increasing",
            "How much debt the company has",
            "How expensive the stock is",
            "How much cash an investor owns"
        ],
        key="module4_q1"
    )

    q2 = st.radio(
        "2. Why can high debt increase risk?",
        [
            "Debt always causes a company to fail",
            "The company may have more difficulty if interest rates rise or profits fall",
            "Debt guarantees lower revenue",
            "Debt makes diversification impossible"
        ],
        key="module4_q2"
    )

    q3 = st.radio(
        "3. TechCore has strong growth, strong margins, low debt, but an expensive valuation. What is the best conclusion?",
        [
            "TechCore is guaranteed to rise",
            "TechCore has no investment risk",
            "TechCore has attractive strengths, but its valuation is also a risk to consider",
            "Valuation does not matter if revenue is growing"
        ],
        key="module4_q3"
    )

    if st.button(
        "Submit Quiz",
        key="module4_submit"
    ):

        score = 0

        if q1 == "How quickly a company's sales are increasing":
            score += 1

        if q2 == "The company may have more difficulty if interest rates rise or profits fall":
            score += 1

        if q3 == "TechCore has attractive strengths, but its valuation is also a risk to consider":
            score += 1

        st.session_state.module4_score = score

        if score == 3:

            st.success("🎉 3/3 — Great job!")

            st.session_state.module4_complete = True
            log_event("module_completed", "Researching a Company")

        elif score == 2:

            st.warning(
                "You got 2/3. Review the lesson and try again."
            )

        else:

            st.error(
                f"You got {score}/3. Review the lesson and try again."
            )

    if st.session_state.module4_complete:

        st.divider()

        st.success("✅ Module Complete")

        st.write(
            f"Knowledge Score: {st.session_state.module4_score}/3"
        )

        st.info(
            "Next: Learn how news and economic events can move markets."
        )

# -------------------------------------------------
# MODULE 5 — NEWS & MARKETS
# -------------------------------------------------

elif page == "Learn: News & Markets":

    st.title("Module 5: News & Markets")

    st.write(
        """
        Stock prices can react to economic news, company news,
        and changes in investor expectations.

        But the same news does not always affect every investment
        in the same way.
        """
    )

    st.divider()

    # -------------------------------------------------
    # SECTION 1
    # -------------------------------------------------

    st.subheader("1. Interest Rates")

    st.write(
        """
        Interest rates affect the cost of borrowing money.

        When interest rates rise:

        - borrowing becomes more expensive
        - companies with high debt may face higher costs
        - some high-growth stocks may become less attractive
        - bond prices can also react to changing rates

        When rates fall, borrowing becomes cheaper,
        which can help some businesses and investments.
        """
    )

    st.info(
        """
        Example:

        GreenGrid has high debt.

        If interest rates suddenly rise,
        GreenGrid may be affected more than a company with very little debt.
        """
    )

    # -------------------------------------------------
    # SECTION 2
    # -------------------------------------------------

    st.subheader("2. Inflation")

    st.write(
        """
        **Inflation** means prices for goods and services are increasing.

        High inflation can affect companies by increasing costs
        for materials, wages, transportation, and other expenses.

        Inflation can also influence interest-rate decisions.
        """
    )

    st.warning(
        """
        Economic news often affects investments indirectly.

        For example:

        Higher inflation → investors expect higher interest rates →
        some stocks may fall.
        """
    )

    # -------------------------------------------------
    # SECTION 3
    # -------------------------------------------------

    st.subheader("3. Recessions and Consumer Spending")

    st.write(
        """
        A **recession** is a period when economic activity weakens.

        During a weak economy:

        - consumers may spend less
        - businesses may reduce investment
        - some companies may experience lower sales

        Different industries can react differently.
        """
    )

    st.info(
        """
        Example:

        RetailCo depends heavily on consumer spending.

        If consumers become worried about the economy and spend less,
        RetailCo may be hurt more than a healthcare company
        with relatively stable demand.
        """
    )

    # -------------------------------------------------
    # SECTION 4
    # -------------------------------------------------

    st.subheader("4. Company-Specific News")

    st.write(
        """
        Sometimes news affects mainly one company rather than
        the entire market.

        Examples include:

        - winning a major contract
        - releasing a successful new product
        - reporting disappointing sales
        - taking on more debt
        - losing an important customer
        """
    )

    st.info(
        """
        Example:

        TechCore announces a major AI infrastructure contract.

        That news may strongly affect TechCore,
        while having little direct effect on HealthPlus or RetailCo.
        """
    )

    # -------------------------------------------------
    # SECTION 5
    # -------------------------------------------------

    st.subheader("5. The same news can affect investments differently")

    st.write(
        """
        Imagine the central bank unexpectedly raises interest rates.

        **TechCore**
        High-growth technology company with an expensive valuation.

        **GreenGrid**
        Growing company with high debt.

        **HealthPlus**
        Healthcare company with relatively stable demand.

        **RetailCo**
        Depends heavily on consumer spending.

        **Bond Fund**
        Lower-risk fixed-income investment.

        These investments may react differently even though
        they all receive the same economic news.
        """
    )

    st.warning(
        """
        The important question is not only:

        **"Is this good news or bad news?"**

        Also ask:

        **"Which investments are most exposed to this news, and why?"**
        """
    )

    st.divider()

    # -------------------------------------------------
    # QUIZ
    # -------------------------------------------------

    st.header("Quick Quiz")

    q1 = st.radio(
        "1. Interest rates suddenly rise. Which company may be especially vulnerable because of its high debt?",
        [
            "GreenGrid",
            "HealthPlus",
            "RetailCo",
            "Bond Fund"
        ],
        key="module5_q1"
    )

    q2 = st.radio(
        "2. Consumers sharply reduce spending because they are worried about a recession. Which company may be especially affected?",
        [
            "HealthPlus",
            "RetailCo",
            "Bond Fund",
            "None of them"
        ],
        key="module5_q2"
    )

    q3 = st.radio(
        "3. TechCore wins a major AI infrastructure contract. What is the best conclusion?",
        [
            "Every investment should rise equally",
            "The news is most directly relevant to TechCore",
            "Bond Fund should automatically rise more than TechCore",
            "Company-specific news never affects stock prices"
        ],
        key="module5_q3"
    )

    if st.button(
        "Submit Quiz",
        key="module5_submit"
    ):

        score = 0

        if q1 == "GreenGrid":
            score += 1

        if q2 == "RetailCo":
            score += 1

        if q3 == "The news is most directly relevant to TechCore":
            score += 1

        st.session_state.module5_score = score

        if score == 3:

            st.success("🎉 3/3 — Great job!")

            st.session_state.module5_complete = True
            log_event("module_completed", "News & Markets")

        elif score == 2:

            st.warning(
                "You got 2/3. Review the lesson and try again."
            )

        else:

            st.error(
                f"You got {score}/3. Review the lesson and try again."
            )

    if st.session_state.module5_complete:

        st.divider()

        st.success("✅ Module Complete")

        st.write(
            f"Knowledge Score: {st.session_state.module5_score}/3"
        )

        st.info(
            "You're ready for Market Mode!"
        )
# -------------------------------------------------
# LEVEL 1
# -------------------------------------------------

elif page == "Level 1: The Crash":

    st.title("Level 1: Survive the Crash")

    st.write(
        """
        **January 2020**

        You have **$10,000**.

        You decide to invest all of it in the S&P 500 using SPY.

        Everything seems normal...

        Then the market begins collapsing.
        """
    )

    try:

        spy = get_history(
            "SPY",
            "2020-01-01",
            "2021-01-05"
        )

        start_price = float(spy["Close"].iloc[0])

        crash_period = spy.loc[
            "2020-02-01":"2020-04-30"
        ]

        crash_price = float(
            crash_period["Close"].min()
        )

        end_price = float(
            spy.loc[:"2020-12-31"]["Close"].iloc[-1]
        )

        starting_money = 10000
        shares = starting_money / start_price

        crash_value = shares * crash_price
        end_value = shares * end_price

        decline = (
            crash_value / starting_money - 1
        ) * 100

        st.error("MARKET CRASH")

        st.metric(
            "Your Portfolio",
            f"${crash_value:,.0f}",
            f"{decline:.1f}%"
        )

        st.write(
            f"""
            Your **$10,000** investment has fallen to approximately
            **${crash_value:,.0f}**.

            You don't know what will happen next.
            """
        )

        choice1 = st.radio(
            "What do you do?",
            [
                "Sell everything",
                "Hold",
                "Invest another $1,000"
            ],
            key="level1_radio"
        )

        choice1_reason = st.radio(
            "What is the main reason for your decision?",
            [
                "The market is falling quickly and I'm worried about losing more money.",
                "I believe the reason I originally invested is still valid.",
                "I believe something fundamental about the investment has changed.",
                "My financial situation or ability to take risk has changed."
            ],
            key="level1_reason_radio"
        )

        if st.button(
            "Make My Decision",
            key="level1_button"
        ):

            if not st.session_state.level1_complete:

                st.session_state.choice1 = choice1
                st.session_state.choice1_reason = choice1_reason

                if choice1_reason == "The market is falling quickly and I'm worried about losing more money.":
                    st.session_state.panic_resistance -= 2
                    st.session_state.long_term_thinking -= 1

                elif choice1_reason == "I believe the reason I originally invested is still valid.":
                    st.session_state.panic_resistance += 2
                    st.session_state.long_term_thinking += 2

                elif choice1_reason == "I believe something fundamental about the investment has changed.":
                    st.session_state.risk_awareness += 2

                elif choice1_reason == "My financial situation or ability to take risk has changed.":
                    st.session_state.risk_awareness += 2

                if choice1 == "Invest another $1,000":
                    st.session_state.risk_awareness -= 1

                st.session_state.level1_complete = True

                log_event(
                    "level_completed",
                    f"Survive the Crash | {choice1} | {choice1_reason}"
                )

                clamp_scores()

        if st.session_state.level1_complete:

            choice = st.session_state.choice1
            reason = st.session_state.choice1_reason

            st.divider()

            st.header("Your Decision")

            st.write(f"**You chose:** {choice}")
            st.write(f"**Your reason:** {reason}")

            if reason == "The market is falling quickly and I'm worried about losing more money.":

                st.warning(
                    """
                    Your decision appears to be driven mainly by the market decline itself.

                    Falling prices can feel frightening, but price movement alone does not
                    necessarily tell you whether an investment is still worth owning.

                    A better question is whether the reason you originally invested has changed.
                    """
                )

            elif reason == "I believe the reason I originally invested is still valid.":

                st.success(
                    """
                    You're focusing on the reason you invested rather than reacting only
                    to short-term price movement.

                    That does not guarantee the investment will recover, but it is a more
                    disciplined way to evaluate a market decline.
                    """
                )

            elif reason == "I believe something fundamental about the investment has changed.":

                st.info(
                    """
                    Reconsidering an investment because something fundamental has changed
                    can be reasonable.

                    Selling after a decline is not automatically a mistake. What matters is
                    whether your investment thesis has changed, rather than simply reacting
                    to falling prices.
                    """
                )

            elif reason == "My financial situation or ability to take risk has changed.":

                st.info(
                    """
                    Your own financial situation matters.

                    Even if an investment still looks attractive, reducing risk can be reasonable
                    if you need the money sooner or can no longer tolerate the potential loss.
                    """
                )

            st.divider()

            st.header("What Happened Historically?")

            sell_value = crash_value
            hold_value = end_value

            extra_shares = 1000 / crash_price

            buy_more_value = (
                shares + extra_shares
            ) * end_price

            if choice == "Sell everything":

                st.metric(
                    "Value After Selling",
                    f"${sell_value:,.0f}"
                )

            elif choice == "Hold":

                st.metric(
                    "Value by the End of 2020",
                    f"${hold_value:,.0f}"
                )

            elif choice == "Invest another $1,000":

                st.metric(
                    "Value by the End of 2020",
                    f"${buy_more_value:,.0f}"
                )

            st.subheader("Compare All Three Decisions")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Sell",
                f"${sell_value:,.0f}"
            )

            col2.metric(
                "Hold",
                f"${hold_value:,.0f}"
            )

            col3.metric(
                "Buy More",
                f"${buy_more_value:,.0f}"
            )

            st.info(
                """
                **Historical outcome:** During the 2020 crash, the market eventually recovered,
                so holding or investing more produced a higher year-end value than selling
                during the decline.

                But knowing what happened afterward does not mean those choices were guaranteed
                to be correct at the time.

                **The key lesson is to evaluate why you are making a decision, not simply react
                to whether prices are rising or falling.**
                """
            )

    except Exception as e:

        st.error(
            "Historical market data could not be loaded."
        )

        st.write(e)

# -------------------------------------------------
# LEVEL 2
# -------------------------------------------------

elif page == "Level 2: FOMO":

    st.title("Level 2: The Hot Stock")

    st.write(
        """
        It's late **2020**.

        Tesla has been one of the hottest stocks in the market.

        Friends, social media, and investors everywhere are talking about it.

        You have **$5,000** available to invest.
        """
    )

    try:

        tsla = get_history(
            "TSLA",
            "2020-12-01",
            "2021-03-10"
        )

        buy_price = float(
            tsla["Close"].iloc[0]
        )

        future_price = float(
            tsla.loc[
                "2021-03-01":
            ]["Close"].iloc[0]
        )

        tsla_return = (
            future_price / buy_price - 1
        ) * 100

        st.warning(
            "Everyone seems to be buying TSLA."
        )

        choice2 = st.radio(
            "What do you do with your $5,000?",
            [
                "Put all $5,000 into TSLA",
                "Put $1,000 into TSLA and keep $4,000 in cash",
                "Don't buy TSLA"
            ],
            key="level2_radio"
        )

        if st.button(
            "Make My Decision",
            key="level2_button"
        ):

            if not st.session_state.level2_complete:

                st.session_state.choice2 = choice2

                if choice2 == "Put all $5,000 into TSLA":

                    st.session_state.fomo_resistance -= 2
                    st.session_state.diversification -= 2

                elif choice2 == "Put $1,000 into TSLA and keep $4,000 in cash":

                    st.session_state.fomo_resistance += 1
                    st.session_state.diversification += 1

                elif choice2 == "Don't buy TSLA":

                    st.session_state.fomo_resistance += 2

                st.session_state.level2_complete = True
                log_event("level_completed", "Fight the FOMO")

                clamp_scores()

        if st.session_state.level2_complete:

            st.divider()

            choice = st.session_state.choice2

            if choice == "Put all $5,000 into TSLA":

                shares = 5000 / buy_price
                final_value = shares * future_price

                st.metric(
                    "Your Money After ~3 Months",
                    f"${final_value:,.0f}"
                )

            elif choice == "Put $1,000 into TSLA and keep $4,000 in cash":

                shares = 1000 / buy_price

                final_value = (
                    shares * future_price
                    + 4000
                )

                st.metric(
                    "Your Money After ~3 Months",
                    f"${final_value:,.0f}"
                )

            else:

                final_value = 5000

                st.metric(
                    "Your Money After ~3 Months",
                    "$5,000"
                )

            st.write(
                f"""
                During this historical period, TSLA changed approximately
                **{tsla_return:.1f}%**.
                """
            )

            st.info(
                """
                **Lesson:** Whether a hot stock rises or falls afterward
                isn't the main point.

                Buying something simply because everyone else is buying it
                can expose you to **FOMO and concentration risk**.

                Ask yourself **why** you're buying it.
                """
            )

    except Exception as e:

        st.error(
            "Historical TSLA data could not be loaded."
        )

        st.write(e)


# -------------------------------------------------
# LEVEL 3
# -------------------------------------------------

elif page == "Level 3: Diversification":

    st.title("Level 3: Don't Put All Your Eggs in One Basket")

    st.write(
        """
        You have **$10,000**.

        You need to choose how concentrated your portfolio should be.

        Imagine making this decision near the end of 2021.
        """
    )

    choice3 = st.radio(
        "Choose your portfolio:",
        [
            "100% TSLA",
            "50% TSLA + 50% SPY",
            "100% SPY"
        ],
        key="level3_radio"
    )

    try:

        tsla3 = get_history(
            "TSLA",
            "2021-11-01",
            "2023-01-05"
        )

        spy3 = get_history(
            "SPY",
            "2021-11-01",
            "2023-01-05"
        )

        tsla_start = float(
            tsla3["Close"].iloc[0]
        )

        tsla_end = float(
            tsla3.loc[
                :"2022-12-30"
            ]["Close"].iloc[-1]
        )

        spy_start = float(
            spy3["Close"].iloc[0]
        )

        spy_end = float(
            spy3.loc[
                :"2022-12-30"
            ]["Close"].iloc[-1]
        )

        tsla_growth = (
            tsla_end / tsla_start
        )

        spy_growth = (
            spy_end / spy_start
        )

        all_tsla = (
            10000 * tsla_growth
        )

        mixed = (
            5000 * tsla_growth
            + 5000 * spy_growth
        )

        all_spy = (
            10000 * spy_growth
        )

        if st.button(
            "Build My Portfolio",
            key="level3_button"
        ):

            if not st.session_state.level3_complete:

                st.session_state.choice3 = choice3

                if choice3 == "100% TSLA":

                    st.session_state.diversification -= 2
                    st.session_state.risk_awareness -= 1

                elif choice3 == "50% TSLA + 50% SPY":

                    st.session_state.diversification += 1
                    st.session_state.risk_awareness += 1

                elif choice3 == "100% SPY":

                    st.session_state.diversification += 2
                    st.session_state.risk_awareness += 2

                st.session_state.level3_complete = True
                log_event("level_completed", "Diversification Challenge")

                clamp_scores()

        if st.session_state.level3_complete:

            st.divider()

            choice = st.session_state.choice3

            if choice == "100% TSLA":
                selected_value = all_tsla

            elif choice == "50% TSLA + 50% SPY":
                selected_value = mixed

            else:
                selected_value = all_spy

            st.metric(
                "Your Portfolio Value",
                f"${selected_value:,.0f}"
            )

            st.subheader("What Would Each Portfolio Have Done?")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "100% TSLA",
                f"${all_tsla:,.0f}"
            )

            col2.metric(
                "50/50",
                f"${mixed:,.0f}"
            )

            col3.metric(
                "100% SPY",
                f"${all_spy:,.0f}"
            )

            st.info(
                """
                **Lesson:** Diversification does not guarantee that you
                will make more money.

                It reduces how dependent your portfolio is on the success
                or failure of one company.

                Concentration can increase both potential gains
                **and potential losses**.
                """
            )

    except Exception as e:

        st.error(
            "Historical portfolio data could not be loaded."
        )

        st.write(e)

elif page == "Market Mode":

    if "market_started_logged" not in st.session_state:
        log_event("market_simulation_started")
        st.session_state.market_started_logged = True

    MAX_WEEKS = 12

    import random

    st.title("Simulated Market")
    st.write("""
    Manage a portfolio of fictional companies in a changing economy.

    Research companies, react to news, and try to outperform the market.
    No real money and no real stocks are used.
    """)
    if st.session_state.market_week > 1:
        if st.button("Restart Market Simulation"):

            log_event(
                "market_simulation_restarted",
                f"Restarted during week {st.session_state.market_week}"
            )

            st.session_state.market_week = 1
            st.session_state.market_cash = 10000.0
            st.session_state.trade_history = []
         
            st.session_state.market_prices = {
                "TechCore": 100.0,
                "GreenGrid": 80.0,
                "HealthPlus": 60.0,
                "RetailCo": 40.0,
                "Bond Fund": 100.0
            }

            st.session_state.market_holdings = {
                "TechCore": 0.0,
                "GreenGrid": 0.0,
                "HealthPlus": 0.0,
                "RetailCo": 0.0,
                "Bond Fund": 0.0
            }

            st.session_state.market_news = "The simulated market is open."
            st.session_state.market_history = [10000.0]
            st.session_state.benchmark_history = [10000.0]

            st.session_state.market_last_changes = {
                "TechCore": 0.0,
                "GreenGrid": 0.0,
                "HealthPlus": 0.0,
                "RetailCo": 0.0,
                "Bond Fund": 0.0
            }

            st.rerun()
    # -------------------------------------------------
    # COMPANY INFORMATION
    # -------------------------------------------------

    company_info = {

        "TechCore": {
            "industry": "Technology",
            "growth": "24%",
            "margin": "18%",
            "debt": "Low",
            "valuation": "Expensive",
            "risk": "High",
            "risk_noise": 0.035,
            "description":
                "A fast-growing company focused on AI infrastructure and enterprise software.",
            "question":
                "Is its rapid growth strong enough to justify its expensive valuation?"
        },

        "GreenGrid": {
            "industry": "Clean Energy",
            "growth": "16%",
            "margin": "8%",
            "debt": "High",
            "valuation": "Moderate",
            "risk": "High",
            "risk_noise": 0.035,
            "description":
                "Builds renewable-energy systems, battery storage, and electrical-grid infrastructure.",
            "question":
                "Can its growth overcome its high debt and sensitivity to interest rates?"
        },

        "HealthPlus": {
            "industry": "Healthcare",
            "growth": "8%",
            "margin": "15%",
            "debt": "Low",
            "valuation": "Moderate",
            "risk": "Low",
            "risk_noise": 0.015,
            "description":
                "Sells medical products and healthcare services with relatively stable demand.",
            "question":
                "Would slower but more stable growth improve the risk of your portfolio?"
        },

        "RetailCo": {
            "industry": "Consumer Retail",
            "growth": "5%",
            "margin": "6%",
            "debt": "Medium",
            "valuation": "Cheap",
            "risk": "Medium",
            "risk_noise": 0.025,
            "description":
                "A large retailer whose profits depend heavily on consumer spending.",
            "question":
                "Is the cheap valuation worth the company's sensitivity to the economy?"
        },

        "Bond Fund": {
            "industry": "Fixed Income",
            "growth": "N/A",
            "margin": "N/A",
            "debt": "N/A",
            "valuation": "N/A",
            "risk": "Low",
            "risk_noise": 0.007,
            "description":
                "A diversified bond fund designed to provide stability rather than rapid growth.",
            "question":
                "Could a lower-return asset reduce your portfolio's overall risk?"
        }
    }

    # -------------------------------------------------
    # CURRENT PORTFOLIO
    # -------------------------------------------------

    prices = st.session_state.market_prices
    holdings = st.session_state.market_holdings
    cash = st.session_state.market_cash

    stock_value = sum(
        holdings[name] * prices[name]
        for name in prices
    )

    total_value = cash + stock_value

    benchmark_value = st.session_state.benchmark_history[-1]

    portfolio_return = (
        total_value / 10000 - 1
    ) * 100

    benchmark_return = (
        benchmark_value / 10000 - 1
    ) * 100

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Week",
        st.session_state.market_week
    )

    col2.metric(
        "Cash",
        f"${cash:,.2f}"
    )

    col3.metric(
        "Portfolio",
        f"${total_value:,.2f}",
        f"{portfolio_return:.1f}%"
    )

    col4.metric(
        "Market Index",
        f"${benchmark_value:,.2f}",
        f"{benchmark_return:.1f}%"
    )
    # -------------------------------------------------
    # PORTFOLIO ALLOCATION
    # -------------------------------------------------

    st.divider()

    st.subheader("Portfolio Allocation")

    allocation_data = {}

    for name in prices:
        position_value = holdings[name] * prices[name]

        if total_value > 0:
            allocation_data[name] = (
                position_value / total_value * 100
            )

    if total_value > 0:
        allocation_data["Cash"] = (
            cash / total_value * 100
        )

    allocation_df = pd.DataFrame(
        list(allocation_data.items()),
        columns=["Investment", "Allocation"]
    )

    allocation_df["Allocation"] = (
        allocation_df["Allocation"]
        .round(1)
        .astype(str)
        + "%"
    )

    st.dataframe(
        allocation_df,
        use_container_width=True,
        hide_index=True
    )

    for name in prices:
        position_value = holdings[name] * prices[name]

        if total_value > 0:
            weight = position_value / total_value

            if weight > 0.50:
                st.warning(
                    f"⚠️ {weight * 100:.0f}% of your portfolio "
                    f"is invested in {name}. "
                    f"Your portfolio is highly concentrated."
                )
 # -------------------------------------------------
    # DIVERSIFIER ACHIEVEMENT
    # -------------------------------------------------

    active_investments = sum(
        1
        for name in prices
        if holdings[name] > 0
    )

    if active_investments >= 3:

        if "Diversifier" not in st.session_state.achievements:

            st.session_state.achievements.append(
                "Diversifier"
            )
    # -------------------------------------------------
    # PERFORMANCE CHART
    # -------------------------------------------------

    st.divider()

    st.subheader("Performance")

    history_length = len(
        st.session_state.market_history
    )

    performance_data = pd.DataFrame({
        "Week": range(1, history_length + 1),
        "Your Portfolio":
            st.session_state.market_history,
        "Market Index":
            st.session_state.benchmark_history
    })

    performance_data = performance_data.set_index("Week")

    st.line_chart(performance_data)

    if portfolio_return > benchmark_return:

        st.success(
            f"You are outperforming the market by "
            f"{portfolio_return - benchmark_return:.1f} percentage points."
        )

    elif portfolio_return < benchmark_return:

        st.warning(
            f"You are trailing the market by "
            f"{benchmark_return - portfolio_return:.1f} percentage points."
        )

    else:

        st.info(
            "Your portfolio is currently matching the market."
        )

      # -------------------------------------------------
    # MARKET NEWS
    # -------------------------------------------------

    st.divider()

    st.subheader("Market News")

    st.markdown(f"""
    <div class="news-card">
        <div class="news-label">📰 MARKET NEWS</div>
        <div class="news-headline">
            {st.session_state.market_news}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # MARKET TABLE
    # -------------------------------------------------

    st.divider()

    st.subheader("Market")
    # -------------------------------------------------
    # MARKET TABLE
    # -------------------------------------------------
    header1, header2, header3, header4 = st.columns(
        [2, 1, 1, 2]
    )

    header1.write("**Investment**")
    header2.write("**Price**")
    header3.write("**Week**")
    header4.write("**Position**")

    for name, price in prices.items():

        shares = holdings[name]

        position_value = (
            shares * price
        )

        change = (
            st.session_state
            .market_last_changes[name]
        )

        c1, c2, c3, c4 = st.columns(
            [2, 1, 1, 2]
        )

        c1.write(name)

        c2.write(
            f"${price:,.2f}"
        )

        c3.write(
            f"{change:+.1f}%"
        )

        c4.write(
            f"${position_value:,.2f}"
        )

    # -------------------------------------------------
    # COMPANY RESEARCH
    # -------------------------------------------------

    st.divider()

    st.subheader("Research an Investment")

    research_stock = st.selectbox(
        "Choose an investment to research",
        list(company_info.keys()),
        key="research_stock"
    )

    info = company_info[
        research_stock
    ]

    st.markdown(
        f"""
        ### {research_stock}

        **Industry:** {info["industry"]}

        {info["description"]}
        """
    )

    r1, r2, r3 = st.columns(3)

    r1.metric(
        "Revenue Growth",
        info["growth"]
    )

    r2.metric(
        "Profit Margin",
        info["margin"]
    )

    r3.metric(
        "Risk",
        info["risk"]
    )

    r4, r5 = st.columns(2)

    r4.write(
        f"**Debt:** {info['debt']}"
    )

    r5.write(
        f"**Valuation:** {info['valuation']}"
    )

    st.info(
        f"Investor question: {info['question']}"
    )

    # -------------------------------------------------
    # TRADING
    # -------------------------------------------------

    st.divider()

    st.subheader("Trade")

    selected_stock = st.selectbox(
        "Choose an investment",
        list(prices.keys()),
        key="trade_stock"
    )

    action = st.radio(
        "Action",
        ["Buy", "Sell"],
        horizontal=True,
        key="trade_action"
    )

    dollar_amount = st.number_input(
        "Dollar amount",
        min_value=0.0,
        value=500.0,
        step=100.0,
        key="trade_amount"
    )

    if st.button(
        "Execute Trade",
        key="execute_trade"
    ):

        current_price = prices[
            selected_stock
        ]

        if action == "Buy":

            if (
                dollar_amount >
                st.session_state.market_cash
            ):

                st.error(
                    "You do not have enough cash."
                )

            elif dollar_amount <= 0:

                st.warning(
                    "Enter an amount greater than zero."
                )

            else:

                shares_to_buy = (
                    dollar_amount
                    / current_price
                )

                st.session_state.market_holdings[
                    selected_stock
                ] += shares_to_buy

                st.session_state.market_cash -= (
                    dollar_amount
                )
                st.session_state.trade_history.append({
    "Week": st.session_state.market_week,
    "Action": "Buy",
    "Investment": selected_stock,
    "Amount": dollar_amount,
    "Price": current_price
})
                if "First Trade" not in st.session_state.achievements:
                    st.session_state.achievements.append("First Trade")

                st.success(
                    f"You invested ${dollar_amount:,.2f} "
                    f"in {selected_stock}."
                )

                st.rerun()

        else:

            shares_owned = (
                st.session_state
                .market_holdings[
                    selected_stock
                ]
            )

            shares_to_sell = (
                dollar_amount
                / current_price
            )

            if shares_to_sell > shares_owned:

                st.error(
                    "You do not own enough shares."
                )

            elif dollar_amount <= 0:

                st.warning(
                    "Enter an amount greater than zero."
                )

            else:

                st.session_state.market_holdings[
                    selected_stock
                ] -= shares_to_sell

                st.session_state.market_cash += (
                    dollar_amount
                )
                st.session_state.trade_history.append({
    "Week": st.session_state.market_week,
    "Action": "Sell",
    "Investment": selected_stock,
    "Amount": dollar_amount,
    "Price": current_price
})
                if "First Trade" not in st.session_state.achievements:
                    st.session_state.achievements.append("First Trade")

                st.success(
                    f"You sold ${dollar_amount:,.2f} "
                    f"of {selected_stock}."
                )

                st.rerun()
    # -------------------------------------------------
    # TRADE HISTORY
    # -------------------------------------------------

    st.divider()

    st.subheader("Trade History")

    if len(st.session_state.trade_history) == 0:

        st.info("No trades yet.")

    else:

        trade_df = pd.DataFrame(
            st.session_state.trade_history
        )

        trade_df["Amount"] = trade_df["Amount"].apply(
            lambda x: f"${x:,.2f}"
        )

        trade_df["Price"] = trade_df["Price"].apply(
            lambda x: f"${x:,.2f}"
        )

        st.dataframe(
            trade_df,
            use_container_width=True,
            hide_index=True
        )
    # -------------------------------------------------
    # EVENTS
    # -------------------------------------------------

    st.divider()

    st.subheader("Move the Market Forward")

    st.write(
        """
        Advance one week to receive new economic or company news.

        Different investments will react differently depending on
        their industry, valuation, debt, and risk.
        """
    )

    if st.session_state.market_week < MAX_WEEKS:

        if st.button(
            f"Advance to Week {st.session_state.market_week + 1} →",
            type="primary",
            use_container_width=True,
            key="advance_market"
        ):

            events = [

                {
                    "headline":
                        "Technology spending accelerates as companies increase AI investment.",

                    "effects": {
                        "TechCore": 0.07,
                        "GreenGrid": 0.01,
                        "HealthPlus": 0.00,
                        "RetailCo": 0.01,
                        "Bond Fund": -0.005
                    }
                },

                {
                    "headline":
                        "The central bank unexpectedly raises interest rates.",

                    "effects": {
                        "TechCore": -0.07,
                        "GreenGrid": -0.06,
                        "HealthPlus": -0.01,
                        "RetailCo": -0.03,
                        "Bond Fund": -0.025
                    }
                },

                {
                    "headline":
                        "Inflation falls faster than expected and investors expect lower interest rates.",

                    "effects": {
                        "TechCore": 0.06,
                        "GreenGrid": 0.05,
                        "HealthPlus": 0.02,
                        "RetailCo": 0.03,
                        "Bond Fund": 0.025
                    }
                },

                {
                    "headline":
                        "Consumers reduce spending as recession fears increase.",

                    "effects": {
                        "TechCore": -0.03,
                        "GreenGrid": -0.02,
                        "HealthPlus": 0.01,
                        "RetailCo": -0.09,
                        "Bond Fund": 0.025
                    }
                },

                {
                    "headline":
                        "New government incentives increase investment in clean energy.",

                    "effects": {
                        "TechCore": 0.01,
                        "GreenGrid": 0.10,
                        "HealthPlus": 0.00,
                        "RetailCo": 0.00,
                        "Bond Fund": 0.00
                    }
                },

                {
                    "headline":
                        "Healthcare demand remains strong even as economic growth slows.",

                    "effects": {
                        "TechCore": -0.01,
                        "GreenGrid": -0.01,
                        "HealthPlus": 0.07,
                        "RetailCo": -0.03,
                        "Bond Fund": 0.01
                    }
                },

                {
                    "headline":
                        "Consumer confidence jumps and households increase spending.",

                    "effects": {
                        "TechCore": 0.02,
                        "GreenGrid": 0.01,
                        "HealthPlus": 0.01,
                        "RetailCo": 0.08,
                        "Bond Fund": -0.01
                    }
                },

                {
                    "headline":
                        "TechCore announces a major new AI infrastructure contract.",

                    "effects": {
                        "TechCore": 0.12,
                        "GreenGrid": 0.00,
                        "HealthPlus": 0.00,
                        "RetailCo": 0.00,
                        "Bond Fund": 0.00
                    }
                },

                {
                    "headline":
                        "GreenGrid reports that higher borrowing costs are hurting expansion plans.",

                    "effects": {
                        "TechCore": 0.00,
                        "GreenGrid": -0.11,
                        "HealthPlus": 0.00,
                        "RetailCo": 0.00,
                        "Bond Fund": 0.00
                    }
                }
            ]

            event = random.choice(events)

            st.session_state.market_news = (
                event["headline"]
            )

            weekly_returns = {}

            for name in st.session_state.market_prices:

                base_effect = (
                    event["effects"][name]
                )

                risk_noise = (
                    company_info[name]["risk_noise"]
                )

                random_noise = random.uniform(
                    -risk_noise,
                    risk_noise
                )

                weekly_return = (
                    base_effect
                    + random_noise
                )

                # Prevent absurd one-week moves
                weekly_return = max(
                    -0.20,
                    min(
                        0.20,
                        weekly_return
                    )
                )

                weekly_returns[name] = (
                    weekly_return
                )

                current_price = (
                    st.session_state.market_prices[name]
                )

                new_price = (
                    current_price
                    * (1 + weekly_return)
                )

                st.session_state.market_prices[name] = max(
                    1,
                    round(
                        new_price,
                        2
                    )
                )

                st.session_state.market_last_changes[name] = (
                    weekly_return * 100
                )

            # -----------------------------------------
            # UPDATE FAKE MARKET INDEX
            # -----------------------------------------

            benchmark_weekly_return = (
                sum(weekly_returns.values())
                / len(weekly_returns)
            )

            previous_benchmark = (
                st.session_state.benchmark_history[-1]
            )

            new_benchmark = (
                previous_benchmark
                * (1 + benchmark_weekly_return)
            )

            st.session_state.benchmark_history.append(
                new_benchmark
            )

            # -----------------------------------------
            # UPDATE USER PORTFOLIO HISTORY
            # -----------------------------------------

            updated_stock_value = sum(
                st.session_state.market_holdings[name]
                * st.session_state.market_prices[name]
                for name in st.session_state.market_prices
            )

            updated_portfolio = (
                st.session_state.market_cash
                + updated_stock_value
            )

            st.session_state.market_history.append(
                updated_portfolio
            )

            st.session_state.market_week += 1


            if st.session_state.market_week >= MAX_WEEKS:
                log_event("market_simulation_completed", "12 weeks")

            st.rerun()

    else:
        st.success("🏆 The 12-week simulation is complete!")

        final_value = st.session_state.market_history[-1]
        final_market = st.session_state.benchmark_history[-1]
        st.success("🏆 The 12-week simulation is complete!")

        final_value = st.session_state.market_history[-1]
        final_market = st.session_state.benchmark_history[-1]

        final_return = (
            final_value / 10000 - 1
        ) * 100

        market_return = (
            final_market / 10000 - 1
        ) * 100

        # -----------------------------------------
        # FINAL RESULTS
        # -----------------------------------------

        st.subheader("Final Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Final Portfolio",
            f"${final_value:,.2f}",
            f"{final_return:+.1f}%"
        )

        col2.metric(
            "Market Index",
            f"${final_market:,.2f}",
            f"{market_return:+.1f}%"
        )

        difference = (
            final_return - market_return
        )
        if difference > 0:

            if "Market Beater" not in st.session_state.achievements:

                st.session_state.achievements.append(
                    "Market Beater"
                )
        col3.metric(
            "Vs. Market",
            f"{difference:+.1f}%"
        )

        # -----------------------------------------
        # PERFORMANCE SCORE
        # -----------------------------------------

        if final_return >= 15:
            performance_score = 10

        elif final_return >= 10:
            performance_score = 9

        elif final_return >= 5:
            performance_score = 8

        elif final_return >= 0:
            performance_score = 7

        elif final_return >= -5:
            performance_score = 5

        else:
            performance_score = 3

        # -----------------------------------------
        # MARKET SCORE
        # -----------------------------------------

        if difference >= 5:
            market_score = 10

        elif difference >= 2:
            market_score = 9

        elif difference >= 0:
            market_score = 8

        elif difference >= -3:
            market_score = 6

        else:
            market_score = 4

        # -----------------------------------------
        # DIVERSIFICATION SCORE
        # -----------------------------------------

        position_values = {
            name: st.session_state.market_holdings[name]
            * st.session_state.market_prices[name]
            for name in st.session_state.market_prices
        }

        invested_value = sum(
            position_values.values()
        )

        active_investments = sum(
            1
            for value in position_values.values()
            if value > 0
        )

        if active_investments >= 4:
            diversification_score = 10

        elif active_investments == 3:
            diversification_score = 8

        elif active_investments == 2:
            diversification_score = 6

        elif active_investments == 1:
            diversification_score = 3

        else:
            diversification_score = 1

        # -----------------------------------------
        # RISK MANAGEMENT SCORE
        # -----------------------------------------

        if final_value > 0:

            largest_position = max(
                position_values.values()
            )

            largest_weight = (
                largest_position / final_value
            )

        else:
            largest_weight = 1
            # RISK MANAGER ACHIEVEMENT
        if largest_weight <= 0.50:

            if "Risk Manager" not in st.session_state.achievements:

                st.session_state.achievements.append(
                    "Risk Manager"
                )

        if largest_weight <= 0.30:
            risk_score = 10

        elif largest_weight <= 0.40:
            risk_score = 8

        elif largest_weight <= 0.50:
            risk_score = 6

        elif largest_weight <= 0.70:
            risk_score = 4

        else:
            risk_score = 2

            # -----------------------------------------
        # INVESTOR LAB GRADUATE ACHIEVEMENT
        # -----------------------------------------

        if (
            st.session_state.module1_complete
            and st.session_state.level1_complete
            and st.session_state.level2_complete
            and st.session_state.level3_complete
            and st.session_state.market_week >= 12
        ):

            if (
                "Investor Lab Graduate"
                not in st.session_state.achievements
            ):

                st.session_state.achievements.append(
                    "Investor Lab Graduate"
                )

        # -----------------------------------------
        # FINAL SCORE
        # -----------------------------------------

        final_score = (
            performance_score * 0.35
            + market_score * 0.25
            + diversification_score * 0.20
            + risk_score * 0.20
        ) * 10

        st.divider()

        st.subheader("Investor Score")

        score1, score2, score3, score4 = st.columns(4)

        score1.metric(
            "Performance",
            f"{performance_score}/10"
        )

        score2.metric(
            "Vs. Market",
            f"{market_score}/10"
        )

        score3.metric(
            "Diversification",
            f"{diversification_score}/10"
        )

        score4.metric(
            "Risk Management",
            f"{risk_score}/10"
        )

        st.metric(
            "Final Score",
            f"{final_score:.0f}/100"
        )

        # -----------------------------------------
        # INVESTOR RATING
        # -----------------------------------------

        if final_score >= 90:
            rating = "🏆 Elite Investor"

        elif final_score >= 80:
            rating = "📈 Disciplined Investor"

        elif final_score >= 70:
            rating = "🧠 Thoughtful Investor"

        elif final_score >= 60:
            rating = "🌱 Developing Investor"

        else:
            rating = "⚠️ High-Risk Investor"

        st.header(rating)

        if difference > 0:
            st.success(
                f"You beat the market by "
                f"{difference:.1f} percentage points."
            )

        elif difference < 0:
            st.warning(
                f"You finished "
                f"{abs(difference):.1f} percentage points "
                f"behind the market."
            )

        else:
            st.info(
                "You finished exactly even with the market."
            )
# -------------------------------------------------
# INVESTOR PROFILE
# -------------------------------------------------

elif page == "Investor Profile":


    st.title("Your Investor Profile")


    completed = sum([
        st.session_state.level1_complete,
        st.session_state.level2_complete,
        st.session_state.level3_complete
    ])


    if completed < 3:


        st.warning(
            f"You've completed {completed}/3 levels."
        )


        st.write(
            """
            Complete all three scenarios to get your full investor profile.
            """
        )

    else:

        clamp_scores()

        scores = {
            "Panic Resistance":
                st.session_state.panic_resistance,

            "FOMO Resistance":
                st.session_state.fomo_resistance,

            "Diversification":
                st.session_state.diversification,

            "Risk Awareness":
                st.session_state.risk_awareness,

            "Long-Term Thinking":
                st.session_state.long_term_thinking
        }

        for name, score in scores.items():

            st.write(f"**{name}**")

            st.code(
                f"{score_bar(score)} {score}/10",
                language=None
            )

        st.divider()

        strongest = max(
            scores,
            key=scores.get
        )

        weakest = min(
            scores,
            key=scores.get
        )

        average_score = (
            sum(scores.values())
            / len(scores)
        )

        # INVESTOR TYPE

        if (
            st.session_state.fomo_resistance <= 4
            and st.session_state.diversification <= 4
        ):

            investor_type = "The Momentum Chaser"

            description = (
                "You are attracted to exciting investments "
                "and may take concentrated risks."
            )

        elif (
            st.session_state.panic_resistance >= 7
            and st.session_state.long_term_thinking >= 7
        ):

            investor_type = "The Calm Long-Term Investor"

            description = (
                "You tend to stay patient during volatility "
                "and think beyond short-term market moves."
            )

        elif (
            st.session_state.diversification >= 7
            and st.session_state.risk_awareness >= 7
        ):

            investor_type = "The Risk-Aware Diversifier"

            description = (
                "You think carefully about downside risk "
                "and avoid depending too heavily on one investment."
            )

        elif average_score >= 7:

            investor_type = "The Disciplined Investor"

            description = (
                "You generally make balanced and thoughtful decisions."
            )

        else:

            investor_type = "The Developing Investor"

            description = (
                "You're still developing your investing habits "
                "and learning how you respond to risk."
            )

        st.header(investor_type)

        st.write(description)

        st.divider()

        feedback = {

            "Panic Resistance":
                "You tend to stay calm when markets fall instead of immediately reacting.",

            "FOMO Resistance":
                "You are less likely to chase an investment simply because it is popular.",

            "Diversification":
                "You understand the value of spreading risk across investments.",

            "Risk Awareness":
                "You think about what you could lose, not just what you could gain.",

            "Long-Term Thinking":
                "You focus more on long-term outcomes than short-term price movements."
        }

        improvement = {

            "Panic Resistance":
                "Before selling during a decline, ask whether something fundamental actually changed.",

            "FOMO Resistance":
                "Before buying a hot investment, ask whether your reasoning goes beyond its recent price increase.",

            "Diversification":
                "Think about what would happen to your portfolio if one company performed very badly.",

            "Risk Awareness":
                "Consider the downside before focusing on potential profit.",

            "Long-Term Thinking":
                "Try evaluating investments over longer periods instead of reacting to every short-term move."
        }

        st.subheader("💪 Biggest Strength")
        st.success(strongest)
        st.write(feedback[strongest])

        st.subheader("🎯 Area to Improve")
        st.warning(weakest)
        st.write(improvement[weakest])

        st.divider()

        st.caption(
            "This simulator is for financial education and does not provide investment advice."
        )
        # -------------------------------------------------
# FEEDBACK SURVEY
# -------------------------------------------------

full_program_complete = (
    st.session_state.module1_complete
    and st.session_state.module2_complete
    and st.session_state.module3_complete
    and st.session_state.module4_complete
    and st.session_state.module5_complete
    and st.session_state.level1_complete
    and st.session_state.level2_complete
    and st.session_state.level3_complete
    and st.session_state.market_week >= 12
)
if full_program_complete and "program_complete_logged" not in st.session_state:
    log_event("program_completed")
    st.session_state.program_complete_logged = True

if full_program_complete:

    st.divider()

    st.subheader("Help Improve Investor Lab")

    st.write(
        "You've completed Investor Lab! This short, anonymous survey takes about "
        "60 seconds and helps us understand what you learned and how we can improve "
        "Investor Lab for future students."
    )

    st.link_button(
        "Give Feedback",
        "https://docs.google.com/forms/d/e/1FAIpQLSe6Fsha-k_3h86lTEXJs0e9OM5bKglFaD72gNHCeUapdRFjzg/viewform?usp=dialog",
        use_container_width=True
    )
