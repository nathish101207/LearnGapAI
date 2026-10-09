from flask import Flask, render_template, request, session
from datetime import date
from videos import VIDEO_LINKS
from questions import QUESTION_BANK

app = Flask(__name__)

app.secret_key = "learngap-demo-key"


# =========================================================
# DASHBOARD DATA
# =========================================================

def get_dashboard_data():

    name = session.get(
        "student_name",
        "Student"
    )

    first_score = session.get(
        "first_score",
        0
    )

    diagnostic_percentage = session.get(
        "diagnostic_percentage",
        (first_score / 6 * 100)
        if first_score else 0
    )

    practice_score = session.get(
        "practice_score",
        0
    )

    practice_total = session.get(
        "practice_total",
        0
    )

    practice_percentage = session.get(
        "practice_percentage",
        (practice_score / practice_total * 100)
        if practice_total else 0
    )

    final_score = session.get(
        "final_score",
        0
    )

    retest_total = session.get(
        "retest_total",
        0
    )

    retest_percentage = session.get(
        "retest_percentage",
        (final_score / retest_total * 100)
        if retest_total else 0
    )

    improvement = session.get(
        "improvement",
        retest_percentage - diagnostic_percentage
    )

    streak = session.get(
        "streak",
        0
    )

    weak_topics = session.get(
        "weak_topics",
        []
    )

    topic_scores = session.get(
        "topic_scores",
        {}
    )

    mistake_analysis = session.get(
        "mistake_analysis",
        []
    )

    xp = session.get(
        "xp",
        0
    )

    level = (
        xp // 100
    ) + 1

    level_xp = xp % 100

    # Daily learning goal
    daily_goal = 3

    completed_steps = 0

    if "first_score" in session:
        completed_steps += 1

    if "practice_score" in session:
        completed_steps += 1

    if "final_score" in session:
        completed_steps += 1

    goal_percentage = min(
        (completed_steps / daily_goal) * 100,
        100
    )

    return {

        "name": name,

        "score": first_score,

        "first_score": first_score,

        "diagnostic_percentage":
            diagnostic_percentage,

        "practice_score":
            practice_score,

        "practice_total":
            practice_total,

        "practice_percentage":
            practice_percentage,

        "final_score":
            final_score,

        "retest_total":
            retest_total,

        "retest_percentage":
            retest_percentage,

        "improvement":
            improvement,

        "streak":
            streak,

        "weak_topics":
            weak_topics,

        "topic_scores":
            topic_scores,

        "mistake_analysis":
            mistake_analysis,

        "xp":
            xp,

        "level":
            level,

        "level_xp":
            level_xp,

        "daily_goal":
            daily_goal,

        "completed_steps":
            completed_steps,

        "goal_percentage":
            goal_percentage
    }


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        session["student_name"] = request.form.get(
            "name",
            "Student"
        )

        session["email"] = request.form.get(
            "email",
            ""
        )

        return render_template(
            "dashboard.html",
            **get_dashboard_data()
        )

    return render_template(
        "login.html"
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        **get_dashboard_data()
    )


# =========================================================
# DIAGNOSTIC QUIZ
# =========================================================

@app.route("/quiz")
def quiz():

    return render_template(
        "quiz.html"
    )


# =========================================================
# DIAGNOSTIC SUBMIT
# =========================================================

@app.route(
    "/submit",
    methods=["POST"]
)
def submit():

    answers = {

        "q1": "int",

        "q2": "int",

        "q3": "if",

        "q4": "Yes",

        "q5": "for",

        "q6": "012"
    }

    topics = {

        "q1":
            "Variables and Data Types",

        "q2":
            "Variables and Data Types",

        "q3":
            "Conditional Statements",

        "q4":
            "Conditional Statements",

        "q5":
            "Loops",

        "q6":
            "Loops"
    }

    score = 0

    topic_scores = {}

    mistakes = []

    for question, correct_answer in answers.items():

        user_answer = request.form.get(
            question,
            ""
        )

        topic = topics[question]

        if topic not in topic_scores:

            topic_scores[topic] = {

                "correct": 0,

                "total": 0
            }

        topic_scores[topic]["total"] += 1

        if user_answer == correct_answer:

            score += 1

            topic_scores[topic]["correct"] += 1

        else:

            mistakes.append({

                "question":
                    question,

                "topic":
                    topic,

                "user_answer":
                    user_answer
                    or "Not answered",

                "correct_answer":
                    correct_answer
            })

    total = len(answers)

    diagnostic_percentage = (
        score / total
    ) * 100

    weak_topics = []

    for topic, result in topic_scores.items():

        percentage = (
            result["correct"]
            /
            result["total"]
        ) * 100

        if percentage < 70:

            weak_topics.append(
                topic
            )

    gap_explanations = {}

    for topic in weak_topics:

        if topic == "Variables and Data Types":

            gap_explanations[topic] = (
                "You need more practice "
                "with Python data types."
            )

        elif topic == "Conditional Statements":

            gap_explanations[topic] = (
                "You need more practice "
                "with if, else and conditions."
            )

        elif topic == "Loops":

            gap_explanations[topic] = (
                "You need more practice "
                "with for, while and range()."
            )

    session["first_score"] = score

    session["diagnostic_percentage"] = (
        diagnostic_percentage
    )

    session["topic_scores"] = (
        topic_scores
    )

    session["weak_topics"] = (
        weak_topics
    )

    session["mistake_analysis"] = (
        mistakes
    )

    session["gap_explanations"] = (
        gap_explanations
    )

    recommended_videos = {}

    for topic in weak_topics:

        if topic in VIDEO_LINKS:

            recommended_videos[topic] = (
                VIDEO_LINKS[topic]
            )

    return render_template(

        "result.html",

        score=score,

        total=total,

        diagnostic_percentage=
            diagnostic_percentage,

        topic_scores=
            topic_scores,

        weak_topics=
            weak_topics,

        gap_explanations=
            gap_explanations,

        mistake_analysis=
            mistakes,

        recommended_videos=
            recommended_videos
    )


# =========================================================
# LEARNING GAP ANALYSIS
# =========================================================

@app.route("/learning-gaps")
def learning_gaps():

    return render_template(

        "learning_gaps.html",

        diagnostic_percentage=
            session.get(
                "diagnostic_percentage",
                0
            ),

        topic_scores=
            session.get(
                "topic_scores",
                {}
            ),

        weak_topics=
            session.get(
                "weak_topics",
                []
            ),

        gap_explanations=
            session.get(
                "gap_explanations",
                {}
            ),

        mistake_analysis=
            session.get(
                "mistake_analysis",
                []
            )
    )


# =========================================================
# PRACTICE PAGE
# =========================================================

@app.route("/practice")
def practice():

    weak_topics = session.get(
        "weak_topics",
        []
    )

    # -----------------------------------------
    # NO MORE WEAK TOPICS
    # -----------------------------------------

    if not weak_topics:

        return render_template(

            "practice.html",

            practice_questions={},

            weak_topics=[],

            current_topic=None,

            all_completed=True
        )

    # -----------------------------------------
    # CURRENT TOPIC
    # -----------------------------------------

    current_topic = weak_topics[0]

    if current_topic not in QUESTION_BANK:

        return render_template(

            "practice.html",

            practice_questions={},

            weak_topics=[],

            current_topic=None,

            all_completed=True
        )

    questions = QUESTION_BANK[
        current_topic
    ]["practice"]

    practice_questions = {

        current_topic:
            questions
    }

    question_map = []

    for index, question in enumerate(
        questions,
        start=1
    ):

        question_map.append({

            "id":
                f"p{index}",

            "topic":
                current_topic,

            "question":
                question["question"],

            "answer":
                question["answer"]
        })

    # Save exact questions shown
    session["practice_question_map"] = (
        question_map
    )

    # Save current topic
    session["current_practice_topic"] = (
        current_topic
    )

    return render_template(

        "practice.html",

        practice_questions=
            practice_questions,

        weak_topics=
            weak_topics,

        current_topic=
            current_topic,

        all_completed=False
    )


# =========================================================
# PRACTICE RESULT
# =========================================================

@app.route(
    "/practice-result",
    methods=["POST"]
)
def practice_result():

    question_map = session.get(
        "practice_question_map",
        []
    )

    score = 0

    topic_scores = {}

    mistakes = []

    # -----------------------------------------
    # CHECK ANSWERS
    # -----------------------------------------

    for question in question_map:

        question_id = question["id"]

        topic = question["topic"]

        correct_answer = question["answer"]

        user_answer = request.form.get(
            question_id,
            ""
        )

        if topic not in topic_scores:

            topic_scores[topic] = {

                "correct": 0,

                "total": 0
            }

        topic_scores[topic]["total"] += 1

        if user_answer == correct_answer:

            score += 1

            topic_scores[topic]["correct"] += 1

        else:

            mistakes.append({

                "question":
                    question["question"],

                "topic":
                    topic,

                "user_answer":
                    user_answer
                    or "Not answered",

                "correct_answer":
                    correct_answer
            })

    total = len(question_map)

    if total:

        percentage = (
            score / total
        ) * 100

    else:

        percentage = 0

    # -----------------------------------------
    # SAVE PRACTICE RESULT
    # -----------------------------------------

    session["practice_score"] = (
        score
    )

    session["practice_total"] = (
        total
    )

    session["practice_percentage"] = (
        percentage
    )

    session["practice_topic_scores"] = (
        topic_scores
    )

    session["practice_mistakes"] = (
        mistakes
    )

    # -----------------------------------------
    # CURRENT PRACTICE TOPIC
    # -----------------------------------------

    current_topic = session.get(
        "current_practice_topic"
    )

    # -----------------------------------------
    # NEXT TOPIC LOGIC
    # -----------------------------------------

    weak_topics = session.get(
        "weak_topics",
        []
    )

    topic_passed = (
        percentage >= 70
    )

    if (
        topic_passed
        and current_topic
        and current_topic in weak_topics
    ):

        weak_topics.remove(
            current_topic
        )

    session["weak_topics"] = (
        weak_topics
    )

    # -----------------------------------------
    # XP
    # -----------------------------------------

    earned_xp = score * 10

    current_xp = (
        session.get(
            "xp",
            0
        )
        +
        earned_xp
    )

    session["xp"] = (
        current_xp
    )

    level = (
        current_xp // 100
    ) + 1

    session["level"] = (
        level
    )

    level_xp = (
        current_xp % 100
    )

    # -----------------------------------------
    # NEXT TOPIC
    # -----------------------------------------

    next_topic = (

        weak_topics[0]

        if weak_topics

        else None
    )

    # -----------------------------------------
    # RESULT PAGE
    # -----------------------------------------

    return render_template(

        "practice_result.html",

        score=score,

        total=total,

        practice_percentage=
            percentage,

        earned_xp=
            earned_xp,

        xp=
            current_xp,

        level=
            level,

        level_xp=
            level_xp,

        topic_scores=
            topic_scores,

        mistakes=
            mistakes,

        weak_topics=
            weak_topics,

        current_topic=
            current_topic,

        topic_passed=
            topic_passed,

        next_topic=
            next_topic
    )


# =========================================================
# RETEST PAGE
# =========================================================

@app.route("/retest")
def retest():

    weak_topics = session.get(
        "weak_topics",
        []
    )

    if not weak_topics:

        return render_template(

            "retest.html",

            retest_questions={},

            retest_topic=None
        )

    current_topic = weak_topics[0]

    if current_topic not in QUESTION_BANK:

        return render_template(

            "retest.html",

            retest_questions={},

            retest_topic=None
        )

    questions = QUESTION_BANK[
        current_topic
    ]["retest"]

    session["current_retest_topic"] = (
        current_topic
    )

    return render_template(

        "retest.html",

        retest_questions={

            current_topic:
                questions
        },

        retest_topic=
            current_topic
    )


# =========================================================
# RETEST RESULT
# =========================================================

@app.route(
    "/retest-result",
    methods=["POST"]
)
def retest_result():

    topic = session.get(
        "current_retest_topic"
    )

    if not topic:

        return render_template(

            "retest_result.html",

            first_score=0,

            final_score=0,

            total=0,

            diagnostic_percentage=0,

            retest_percentage=0,

            improvement=0,

            streak=session.get(
                "streak",
                0
            ),

            earned_xp=0,

            xp=session.get(
                "xp",
                0
            ),

            level=session.get(
                "level",
                1
            ),

            level_xp=session.get(
                "xp",
                0
            ) % 100
        )

    questions = QUESTION_BANK[
        topic
    ]["retest"]

    score = 0

    for index, question in enumerate(
        questions,
        start=1
    ):

        answer = request.form.get(
            f"r{index}",
            ""
        )

        if answer == question["answer"]:

            score += 1

    total = len(questions)

    percentage = (

        (score / total) * 100

        if total

        else 0
    )

    first_score = session.get(
        "first_score",
        0
    )

    diagnostic_percentage = session.get(

        "diagnostic_percentage",

        (
            first_score / 6 * 100
        )

        if first_score

        else 0
    )

    improvement = (

        percentage
        -
        diagnostic_percentage
    )

    weak_topics = session.get(
        "weak_topics",
        []
    )

    passed = (
        percentage >= 70
    )

    # -----------------------------------------
    # REMOVE PASSED TOPIC
    # -----------------------------------------

    if (
        passed
        and topic in weak_topics
    ):

        weak_topics.remove(
            topic
        )

    session["weak_topics"] = (
        weak_topics
    )

    # -----------------------------------------
    # SAVE RETEST RESULTS
    # -----------------------------------------

    session["final_score"] = (
        score
    )

    session["retest_total"] = (
        total
    )

    session["retest_percentage"] = (
        percentage
    )

    session["improvement"] = (
        improvement
    )

    # -----------------------------------------
    # LEARNING STREAK
    # -----------------------------------------

    today = str(
        date.today()
    )

    if session.get(
        "last_completed"
    ) != today:

        session["streak"] = (

            session.get(
                "streak",
                0
            )
            + 1
        )

        session["last_completed"] = (
            today
        )

    streak = session.get(
        "streak",
        0
    )

    # -----------------------------------------
    # XP
    # -----------------------------------------

    earned_xp = (
        score * 20
    )

    if passed:

        earned_xp += 25

    current_xp = (

        session.get(
            "xp",
            0
        )
        +
        earned_xp
    )

    session["xp"] = (
        current_xp
    )

    level = (
        current_xp // 100
    ) + 1

    level_xp = (
        current_xp % 100
    )

    session["level"] = (
        level
    )

    # -----------------------------------------
    # NEXT TOPIC
    # -----------------------------------------

    next_topic = (

        weak_topics[0]

        if weak_topics

        else None
    )

    # -----------------------------------------
    # RESULT
    # -----------------------------------------

    return render_template(

        "retest_result.html",

        first_score=
            first_score,

        final_score=
            score,

        total=
            total,

        diagnostic_percentage=
            diagnostic_percentage,

        retest_percentage=
            percentage,

        improvement=
            improvement,

        streak=
            streak,

        earned_xp=
            earned_xp,

        xp=
            current_xp,

        level=
            level,

        level_xp=
            level_xp,

        topic=
            topic,

        topic_passed=
            passed,

        remaining_topics=
            weak_topics,

        next_topic=
            next_topic
    )


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )