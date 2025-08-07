def generate_assessment(role, skills, difficulty):
    assessment = {
        "role": role,
        "skills": skills,
        "difficulty": difficulty,
        "sections": {},
        "coverage_summary": {
            "total_questions": 0,
            "per_skill": {},
            "by_type": {"MCQ": 0, "SAQ": 0, "Caselet": 0}
        }
    }

    for skill in skills:
        mcqs = [
            {
                "question_text": f"What is {skill} used for?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_option": 2,
                "explanation": f"{skill} helps with data tasks."
            }
        ]
        saqs = [
            {
                "question_text": f"Explain {skill} in one line.",
                "expected_answer": f"{skill} is useful for ..."
            }
        ]
        caselets = [
            {
                "scenario": f"You are using {skill} on a project. What would you do if the data is inconsistent?",
                "questions": [
                    "How would you detect inconsistency?",
                    "What steps would you take to clean the data?"
                ]
            }
        ]

        assessment["sections"][skill] = {
            "MCQs": mcqs,
            "SAQs": saqs,
            "Caselets": caselets
        }

        assessment["coverage_summary"]["total_questions"] += len(mcqs) + len(saqs) + len(caselets)
        assessment["coverage_summary"]["per_skill"][skill] = len(mcqs) + len(saqs) + len(caselets)
        assessment["coverage_summary"]["by_type"]["MCQ"] += len(mcqs)
        assessment["coverage_summary"]["by_type"]["SAQ"] += len(saqs)
        assessment["coverage_summary"]["by_type"]["Caselet"] += len(caselets)

    return assessment
