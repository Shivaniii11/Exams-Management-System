import mysql.connector
import threading
import time

# ================= DB CONNECTION =================
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",
    database="exam_system"
)

cursor = db.cursor(dictionary=True)

# ================= MAIN LOOP =================
while True:
    print("\n===== ONLINE EXAM SYSTEM =====")
    print("1. Register")
    print("2. Login & Start Exam")
    print("3. Admin Panel")
    print("4. Exit")

    try:
        choice = int(input("Enter choice: "))
    except:
        print("❌ Invalid input!")
        continue

    # ================= REGISTER =================
    if choice == 1:
        username = input("Enter username: ")
        password = input("Enter password: ")

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            print("❌ User already exists!")
        else:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
            db.commit()
            print("✅ Registration successful!")

        continue

    # ================= LOGIN + EXAM =================
    elif choice == 2:
        username = input("Enter username: ")
        password = input("Enter password: ")

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if not user:
            print("❌ Invalid credentials!")
            continue

        print(f"\n✅ Welcome {username}!")

        # ================= SUBJECT =================
        subjects = ["Python", "SQL", "Computer Networks", "DBMS", "OS"]

        print("\nAvailable Subjects:")
        for i, sub in enumerate(subjects, 1):
            print(f"{i}. {sub}")

        sub_choice = int(input("Select Subject: "))
        selected_subject = subjects[sub_choice - 1]

        # ================= INSTRUCTION =================
        print("\n📢 Exam duration is 1 minute for 15 questions.")
        input("Press Enter to start...")

        # ================= FETCH QUESTIONS =================
        cursor.execute("""
        SELECT * FROM questions
        WHERE subject=%s
        ORDER BY RAND()
        LIMIT 15
        """, (selected_subject,))

        questions = cursor.fetchall()

        score = 0
        time_up = False
        user_answers = []

        # ================= TIMER =================
        def timer():
            global time_up
            time.sleep(60)
            time_up = True
            print("\n⏰ Time's up! Auto submitting...\n")

        threading.Thread(target=timer).start()

        # ================= EXAM =================
        for i, q in enumerate(questions, 1):
            if time_up:
                break

            print(f"\nQ{i}: {q['question']}")
            print("1.", q['option1'])
            print("2.", q['option2'])
            print("3.", q['option3'])

            try:
                ans = int(input("Answer: "))
            except:
                ans = 0

            user_answers.append(ans)

            if ans == q['correct_option']:
                score += 1

        # ================= RESULT =================
        percentage = (score / 15) * 100

        print("\n===== RESULT =====")
        print(f"Score: {score}/15")
        print(f"Percentage: {percentage:.2f}%")

        # ================= ANSWER REVIEW =================
        print("\n===== ANSWER REVIEW =====")

        for i, q in enumerate(questions):
            correct = q['correct_option']
            user_ans = user_answers[i] if i < len(user_answers) else "Not Answered"

            print(f"\nQ{i+1}: {q['question']}")
            print(f"Your Answer: {user_ans}")
            print(f"Correct Answer: {correct}")

        # ================= SAVE RESULT =================
        cursor.execute("""
        INSERT INTO results (username, subject, score, total, percentage)
        VALUES (%s, %s, %s, %s, %s)
        """, (username, selected_subject, score, 15, percentage))

        db.commit()

        print("\n✅ Result saved!")

        continue   # 🔥 BACK TO MAIN MENU AFTER EXAM

    # ================= ADMIN PANEL =================
    elif choice == 3:
        print("\n===== ADMIN PANEL =====")

        cursor.execute("SELECT COUNT(*) AS total_users FROM users")
        print(f"👥 Total Users: {cursor.fetchone()['total_users']}")

        cursor.execute("SELECT * FROM results ORDER BY exam_time DESC")
        for r in cursor.fetchall():
            print(f"""
User: {r['username']}
Subject: {r['subject']}
Score: {r['score']}/{r['total']}
Percentage: {r['percentage']:.2f}%
Time: {r['exam_time']}
---------------------------
""")

        continue

    # ================= EXIT =================
    elif choice == 4:
        print("\n👋 Exiting system...")
        break

    else:
        print("❌ Invalid choice!")

# ================= CLOSE =================
cursor.close()
db.close()