import time

# ---------- CONSTANTS ----------
CORRECT_MARKS = 4
WRONG_MARKS   = -1
MIN_QUESTIONS = 10
MAX_ATTEMPTS  = 3
ADMIN_USER, ADMIN_PASS   = "ecat_admin", "ecat@2024"
STUDENT_USER, STUDENT_PASS = "student", "student123"

# ---------- QUESTION BANK ----------
questions = [
    {"id":1,  "subject":"Mathematics",  "question":"Derivative of sin(x)?",
     "choices":{"A":"cos(x)","B":"-cos(x)","C":"-sin(x)","D":"tan(x)"},  "answer":"A"},
    {"id":2,  "subject":"Mathematics",  "question":"Integral of 1/x dx?",
     "choices":{"A":"x","B":"ln|x|+C","C":"1/x^2","D":"e^x"},            "answer":"B"},
    {"id":3,  "subject":"Mathematics",  "question":"If f(x)=x^2, what is f'(3)?",
     "choices":{"A":"9","B":"6","C":"3","D":"12"},                        "answer":"B"},
    {"id":4,  "subject":"Mathematics",  "question":"Value of sin(90)?",
     "choices":{"A":"0","B":"0.5","C":"1","D":"-1"},                      "answer":"C"},
    {"id":5,  "subject":"Physics",      "question":"SI unit of electric current?",
     "choices":{"A":"Volt","B":"Watt","C":"Ampere","D":"Ohm"},            "answer":"C"},
    {"id":6,  "subject":"Physics",      "question":"Newton's 2nd Law: F equals?",
     "choices":{"A":"mv","B":"ma","C":"m/a","D":"a/m"},                   "answer":"B"},
    {"id":7,  "subject":"Physics",      "question":"Speed of light in vacuum?",
     "choices":{"A":"3x10^6","B":"3x10^8","C":"3x10^10","D":"3x10^4"},   "answer":"B"},
    {"id":8,  "subject":"Chemistry",    "question":"Atomic number of Carbon?",
     "choices":{"A":"4","B":"8","C":"6","D":"12"},                        "answer":"C"},
    {"id":9,  "subject":"Chemistry",    "question":"Gas produced when acids react with metals?",
     "choices":{"A":"Oxygen","B":"Nitrogen","C":"Hydrogen","D":"CO2"},    "answer":"C"},
    {"id":10, "subject":"Chemistry",    "question":"pH of pure water at 25°C?",
     "choices":{"A":"5","B":"7","C":"9","D":"14"},                        "answer":"B"},
    {"id":11, "subject":"English",      "question":"Grammatically correct sentence?",
     "choices":{"A":"She don't like coffee.","B":"She doesn't likes coffee.",
                "C":"She doesn't like coffee.","D":"She not like coffee."}, "answer":"C"},
    {"id":12, "subject":"Intelligence", "question":"Complete: 2, 4, 8, 16, ___",
     "choices":{"A":"24","B":"30","C":"32","D":"18"},                     "answer":"C"},
]

1
all_results = []  # stores every student's exam result

# ---------- HELPERS ----------
def line(c="-"): print(c * 60)
def header(t):   line("="); print(" " * ((58 - len(t)) // 2) + t); line("=")
def pause():     time.sleep(1)

def get_grade(pct):
    if pct >= 80: return "EXCELLENT"
    elif pct >= 65: return "GOOD"
    elif pct >= 50: return "AVERAGE"
    else: return "BELOW AVERAGE"

# ---------- LOGIN (shared logic) ----------
def do_login(user, pwd, label):
    header(label)
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        u = input("  Username : ").strip()
        p = input("  Password : ").strip()
        if u == user and p == pwd:
            print("  [OK] Login successful!")
            pause()
            return True
        attempts += 1
        left = MAX_ATTEMPTS - attempts
        print(f"  [!!] Wrong credentials. {left} attempt(s) left.\n" if left else "  [!!] Account locked.\n")
    return False

# ============================================================
#  ADMIN PORTAL
# ============================================================

def view_questions():
    header("ALL QUESTIONS")
    if not questions:
        print("  No questions in bank."); input("\n  Enter to continue..."); return
    for i, q in enumerate(questions):
        print(f"\n  Q{i+1}. [{q['subject']}] {q['question']}")
        for opt in "ABCD":
            mark = "  <-- CORRECT" if opt == q["answer"] else ""
            print(f"    {opt}) {q['choices'][opt]}{mark}")
    line(); print(f"  Total: {len(questions)} questions")
    input("\n  Enter to continue...")

def add_question():
    header("ADD QUESTION")
    subject  = input("  Subject  : ").strip()
    question = input("  Question : ").strip()
    if not subject or not question:2
    print("  [!!] Cannot be empty."); pause(); return
    choices = {}
    for opt in "ABCD":
        choices[opt] = input(f"    {opt}) ").strip()
    while True:
        ans = input("  Correct answer (A/B/C/D) : ").strip().upper()
        if ans in "ABCD" and len(ans) == 1: break
        print("  [!!] Enter A, B, C, or D.")
    new_id = questions[-1]["id"] + 1 if questions else 1
    questions.append({"id":new_id,"subject":subject,"question":question,"choices":choices,"answer":ans})
    print(f"  [OK] Added! Bank now has {len(questions)} question(s)."); pause()

def delete_question():
    header("DELETE QUESTION")
    if not questions:
        print("  No questions to delete."); pause(); return
    for i, q in enumerate(questions):
        print(f"  {i+1}. [{q['subject']}] {q['question']}")
    try:
        choice = int(input("\n  Number to delete (0 to cancel): "))
    except ValueError:
        print("  [!!] Enter a valid number."); pause(); return
    if choice == 0: return
    if 1 <= choice <= len(questions):
        removed = questions.pop(choice - 1)
        print(f"  [OK] Deleted: {removed['question']}")
    else:
        print("  [!!] Number out of range.")
    pause()

def question_stats():
    header("QUESTION BANK STATISTICS")
    if not questions:
        print("  No questions in bank."); input("\n  Enter to continue..."); return
    count = {}
    for q in questions:
        count[q["subject"]] = count.get(q["subject"], 0) + 1
    print(f"  Total Questions: {len(questions)}\n")
    for subj, n in count.items():
        print(f"  {subj:<18} : {n} question(s)  {'#' * n}")
    input("\n  Enter to continue...")

def view_results():
    header("ALL STUDENT RESULTS")
    if not all_results:
        print("  No results yet."); input("\n  Enter to continue..."); return
    print(f"  {'#':<4} {'Name':<20} {'Roll':<18} {'Score':<8} {'%':<7} Grade")
    line()
    for i, r in enumerate(all_results):
        print(f"  {i+1:<4} {r['name']:<20} {r['roll']:<18} {r['score']}/{r['max']:<4} {r['pct']:.1f}%  {r['grade']}")
    input("\n  Enter to continue...")

def detailed_result():
    header("DETAILED STUDENT RESULT")
    if not all_results:
        print("  No results yet."); input("\n  Enter to continue..."); return
    for i, r in enumerate(all_results):
        print(f"  {i+1}. {r['name']} | {r['roll']} | {r['grade']} | {r['pct']:.1f}%")
    try:
        choice = int(input("\n  Enter attempt number (0 to cancel): "))
    except ValueError:
        print("  [!!] Enter a valid number."); pause(); return
    if choice == 0: return
    if not (1 <= choice <= len(all_results)):
        print("  [!!] Out of range."); pause(); return
    r = all_results[choice - 1]
    line()
    print(f"  Name: {r['name']}  |  Roll: {r['roll']}  |  Time: {r['time']}")
    print(f"  Score: {r['score']}/{r['max']}  |  {r['pct']:.1f}%  |  Grade: {r['grade']}")
    print(f"  Correct: {r['correct']}   Wrong: {r['wrong']}   Skipped: {r['skipped']}")
    line()
    print(f"  {'Q':<4} {'Subject':<15} {'Status':<10} {'Yours':<8} Correct")
    line()
    for b in r["breakdown"]:
        icon = "[+]" if b["status"]=="Correct" else ("[-]" if b["status"]=="Wrong" else "[S]")
        print(f"  {b['no']:<4} {b['sub']:<15} {icon+' '+b['status']:<12} {b['given']:<8} {b['correct']}")
    line()
    input("\n  Enter to continue...")

def class_stats():
    header("CLASS STATISTICS")
    if not all_results:
        print("  No results yet."); input("\n  Enter to continue..."); return
    scores = [r["score"] for r in all_results]
    pcts   = [r["pct"] for r in all_results]
    passed = sum(1 for p in pcts if p >= 50)
    print(f"  Total Attempts : {len(all_results)}")
    print(f"  Highest Score  : {max(scores)}")
    print(f"  Lowest Score   : {min(scores)}")
    print(f"  Average Score  : {sum(scores)/len(scores):.1f}")
    print(f"  Passed (>=50%) : {passed}  |  Failed: {len(all_results)-passed}")
    grades = {}
    for r in all_results:
        grades[r["grade"]] = grades.get(r["grade"], 0) + 1
    print("\n  Grade Distribution:")
    for g, n in grades.items():
        print(f"    {g:<15} : {n}")
    input("\n  Enter to continue...")

def admin_portal():
    if not do_login(ADMIN_USER, ADMIN_PASS, "ADMIN LOGIN"):
        return
    options = {"1": view_questions, "2": add_question,  "3": delete_question,
               "4": question_stats, "5": view_results,  "6": detailed_result,
               "7": class_stats}
    while True:
        header("ADMIN PORTAL")
        print("  1. View All Questions\n  2. Add Question\n  3. Delete Question")
        print("  4. Question Bank Statistics\n  5. View All Student Results")
        print("  6. View Detailed Result\n  7. Class Statistics\n  8. Logout")
        line()
        opt = input("  Choice (1-8) : ").strip()
        if opt in options: options[opt]()
        elif opt == "8":   print("  Logged out."); pause(); break
        else:              print("  [!!] Invalid option."); pause()

# ============================================================
#  STUDENT PORTAL
# ============================================================

def start_exam(name, roll):
    if len(questions) < MIN_QUESTIONS:
        print(f"  [!!] Need at least {MIN_QUESTIONS} questions. Bank has {len(questions)}."); pause(); return

    header(f"EXAM  |  {name}  |  {roll}")
    print("  A/B/C/D = answer  |  S = skip  |  SUBMIT = end early")
    line(); pause()

    answers, total = {}, len(questions)
    early = False

    for idx in range(total):
        q = questions[idx]
        line()
        print(f"\n  Q{idx+1}/{total}  [{q['subject']}]")
        print(f"  {q['question']}\n")
        for opt in "ABCD":
            print(f"    {opt}) {q['choices'][opt]}")

        while True:
            raw = input("\n  >> Answer : ").strip().upper()
            if raw == "SUBMIT":
                for r in range(idx, total):
                    if r not in answers: answers[r] = "S"
                early = True; break
            elif raw in list("ABCDS"):
                answers[idx] = raw; break
            else:
                print("  [!!] Type A/B/C/D, S, or SUBMIT.")

        if early: print("  Submitted early."); pause(); break

    # ---- calculate result ----
    correct = wrong = skipped = 0
    breakdown = []
    max_score = total * CORRECT_MARKS

    for idx in range(total):
        q   = questions[idx]
        ans = answers.get(idx, "S")
        if ans == "S":
            status = "Skipped"; skipped += 1
        elif ans == q["answer"]:
            status = "Correct"; correct += 1
        else:
            status = "Wrong";   wrong += 1
        breakdown.append({"no":idx+1,"sub":q["subject"],"status":status,"given":ans,"correct":q["answer"]})

    score = (correct * CORRECT_MARKS) + (wrong * WRONG_MARKS)
    pct   = (score / max_score) * 100 if max_score > 0 else 0
    grade = get_grade(pct)
    ts    = time.strftime("%d-%b-%Y %I:%M %p")

    all_results.append({"name":name,"roll":roll,"score":score,"max":max_score,"pct":pct,"grade":grade,
                        "correct":correct,"wrong":wrong,"skipped":skipped,"time":ts,"breakdown":breakdown})

    # ---- display result ----
    header("YOUR RESULT")
    print(f"  Name      : {name}  |  Roll: {roll}")
    print(f"  Submitted : {ts}")
    line()
    print(f"  Score     : {score} / {max_score}")
    print(f"  Percent   : {pct:.1f}%")
    print(f"  Grade     : {grade}")
    line()
    print(f"  Correct: {correct}   Wrong: {wrong}   Skipped: {skipped}")
    line()
    print(f"  {'Q':<4} {'Subject':<15} {'Status':<10} {'Yours':<8} Correct")
    line()
    for b in breakdown:
        icon = "[+]" if b["status"]=="Correct" else ("[-]" if b["status"]=="Wrong" else "[S]")
        print(f"  {b['no']:<4} {b['sub']:<15} {icon+' '+b['status']:<12} {b['given']:<8} {b['correct']}")
    line()
    input("\n  Enter to continue...")

def student_portal():
    if not do_login(STUDENT_USER, STUDENT_PASS, "STUDENT LOGIN"):
        return
    name = input("  Full Name : ").strip()
    roll = input("  Roll No   : ").strip()
    print("  Welcome,", name); pause()
    while True:
        header(f"STUDENT PORTAL  |  {name}")
        print("  1. Exam Rules\n  2. Start Exam\n  3. Logout")
        line()
        opt = input("  Choice (1-3) : ").strip()
        if opt == "1":
            print("\n  Correct=+4  |  Wrong=-1  |  Skip=0")
            print("  EXCELLENT>=80%  GOOD>=65%  AVERAGE>=50%  BELOW AVERAGE<50%")
            input("\n  Enter to continue...")
        elif opt == "2": start_exam(name, roll)
        elif opt == "3": print(f"  Goodbye, {name}!"); pause(); break
        else: print("  [!!] Invalid."); pause()

# ============================================================
#  MAIN
# ============================================================

def main():
    while True:
        line("=")
        print("    ECAT EXAM APPLICATION  |  DUAL PORTAL SYSTEM")
        print("    UET Lahore  |  CMPE-112L  |  CEA Lab #1  |  2026")
        line("=")
        print("\n  1. Admin Portal\n  2. Student Portal\n  3. Exit\n")
        line()
        opt = input("  Select (1/2/3) : ").strip()
        if   opt == "1": admin_portal()
        elif opt == "2": student_portal()
        elif opt == "3": print("  Goodbye!"); break
        else: print("  [!!] Enter 1, 2, or 3."); pause()

if __name__ == "__main__":
    main()