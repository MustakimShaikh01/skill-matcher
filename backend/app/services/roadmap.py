"""
Roadmap Generator Service
==========================
Takes ordered missing skills → produces a weekly learning plan
with free resource links for each skill.
"""
from typing import List, Dict, Any
from app.services.skill_graph import skill_graph

# ── Free Learning Resources per Skill ─────────────────────────────────────────
RESOURCES: Dict[str, List[str]] = {
    "Python":           ["https://docs.python.org/3/tutorial/", "https://www.learnpython.org/", "https://realpython.com/"],
    "JavaScript":       ["https://javascript.info/", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"],
    "TypeScript":       ["https://www.typescriptlang.org/docs/", "https://www.totaltypescript.com/"],
    "Java":             ["https://dev.java/learn/", "https://www.w3schools.com/java/"],
    "C++":              ["https://www.learncpp.com/", "https://cppreference.com/"],
    "React":            ["https://react.dev/learn", "https://scrimba.com/learn/learnreact"],
    "Vue.js":           ["https://vuejs.org/guide/introduction.html"],
    "Angular":          ["https://angular.io/tutorial"],
    "Next.js":          ["https://nextjs.org/learn"],
    "Node.js":          ["https://nodejs.dev/en/learn/", "https://nodeschool.io/"],
    "Express.js":       ["https://expressjs.com/en/starter/installing.html"],
    "FastAPI":          ["https://fastapi.tiangolo.com/tutorial/"],
    "Django":           ["https://docs.djangoproject.com/en/stable/intro/tutorial01/"],
    "Flask":            ["https://flask.palletsprojects.com/en/latest/quickstart/"],
    "Machine Learning": ["https://www.coursera.org/learn/machine-learning", "https://ml-course.github.io/"],
    "Deep Learning":    ["https://www.deeplearning.ai/courses/", "https://d2l.ai/"],
    "TensorFlow":       ["https://www.tensorflow.org/tutorials"],
    "PyTorch":          ["https://pytorch.org/tutorials/"],
    "NLP":              ["https://www.nltk.org/book/", "https://huggingface.co/learn/nlp-course/"],
    "spaCy":            ["https://spacy.io/usage/101"],
    "scikit-learn":     ["https://scikit-learn.org/stable/tutorial/basic/tutorial.html"],
    "NumPy":            ["https://numpy.org/learn/"],
    "Pandas":           ["https://pandas.pydata.org/docs/getting_started/intro_tutorials/"],
    "Data Structures":  ["https://www.geeksforgeeks.org/data-structures/", "https://visualgo.net/"],
    "Algorithms":       ["https://www.khanacademy.org/computing/computer-science/algorithms", "https://visualgo.net/"],
    "Dynamic Programming": ["https://www.geeksforgeeks.org/dynamic-programming/", "https://leetcode.com/tag/dynamic-programming/"],
    "Graph Theory":     ["https://www.geeksforgeeks.org/graph-data-structure-and-algorithms/"],
    "System Design":    ["https://github.com/donnemartin/system-design-primer", "https://www.educative.io/courses/grokking-the-system-design-interview"],
    "Docker":           ["https://docs.docker.com/get-started/", "https://docker-curriculum.com/"],
    "Kubernetes":       ["https://kubernetes.io/docs/tutorials/kubernetes-basics/"],
    "AWS":              ["https://aws.amazon.com/getting-started/", "https://www.freecodecamp.org/news/pass-the-aws-developer-associate-exam/"],
    "GCP":              ["https://cloud.google.com/learn/training"],
    "Git":              ["https://git-scm.com/book/en/v2", "https://learngitbranching.js.org/"],
    "PostgreSQL":       ["https://www.postgresql.org/docs/current/tutorial.html"],
    "MongoDB":          ["https://learn.mongodb.com/"],
    "Redis":            ["https://redis.io/docs/getting-started/"],
    "HTML":             ["https://developer.mozilla.org/en-US/docs/Learn/HTML"],
    "CSS":              ["https://developer.mozilla.org/en-US/docs/Learn/CSS", "https://flexboxfroggy.com/"],
    "Tailwind CSS":     ["https://tailwindcss.com/docs/installation"],
    "SQL":              ["https://sqlzoo.net/", "https://mode.com/sql-tutorial/"],
    "Linux":            ["https://linuxjourney.com/", "https://ubuntu.com/tutorials/command-line-for-beginners"],
    "CI/CD":            ["https://docs.github.com/en/actions/learn-github-actions"],
    "GitHub Actions":   ["https://docs.github.com/en/actions"],
    "Microservices":    ["https://microservices.io/", "https://martinfowler.com/articles/microservices.html"],
    "REST API":         ["https://restfulapi.net/", "https://www.freecodecamp.org/news/rest-api-tutorial/"],
    "GraphQL":          ["https://graphql.org/learn/"],
    "Recursion":        ["https://www.geeksforgeeks.org/recursion/", "https://leetcode.com/tag/recursion/"],
    "Trees":            ["https://www.geeksforgeeks.org/binary-tree-data-structure/"],
    "Hash Tables":      ["https://www.geeksforgeeks.org/hashing-data-structure/"],
    "Trie":             ["https://www.geeksforgeeks.org/trie-insert-and-search/"],
    "Computer Vision":  ["https://opencv.org/courses/", "https://cs231n.github.io/"],
    "OpenCV":           ["https://docs.opencv.org/4.x/d9/df8/tutorial_root.html"],
    "Hugging Face":     ["https://huggingface.co/learn/nlp-course/"],
    "LangChain":        ["https://python.langchain.com/docs/get_started/introduction"],
    "Kafka":            ["https://kafka.apache.org/quickstart", "https://www.confluent.io/learn/kafka-tutorial/"],
    "Bash":             ["https://www.learnshell.org/", "https://www.gnu.org/software/bash/manual/"],
    "Agile":            ["https://www.agilealliance.org/agile101/"],
    "Scrum":            ["https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf"],
}

DEFAULT_RESOURCES = ["https://www.geeksforgeeks.org/", "https://www.freecodecamp.org/", "https://developer.mozilla.org/"]

SKILL_DESCRIPTIONS: Dict[str, str] = {
    "Python":           "Learn Python syntax, OOP, and standard libraries",
    "JavaScript":       "Master JS fundamentals, async/await, DOM manipulation",
    "React":            "Build component-based UIs with hooks and state management",
    "Machine Learning": "Study ML algorithms, model training, and evaluation",
    "Deep Learning":    "Neural networks, backpropagation, CNNs and RNNs",
    "Data Structures":  "Arrays, linked lists, stacks, queues, trees, graphs",
    "Algorithms":       "Sorting, searching, divide & conquer, greedy algorithms",
    "System Design":    "Scalable architecture, databases, caching, load balancing",
    "Docker":           "Containerise applications and manage images/volumes",
    "AWS":              "Cloud computing: EC2, S3, Lambda, RDS fundamentals",
    "SQL":              "Relational databases, joins, indexes, transactions",
    "Git":              "Version control: branching, merging, rebasing",
    "NLP":              "Text preprocessing, tokenization, embeddings, transformers",
}


def generate_roadmap(
    missing_skills: List[str],
    known_skills: List[str],
) -> List[Dict[str, Any]]:
    """
    Steps:
    1. Topological-sort missing skills via dependency graph (DFS)
    2. Assign each skill to a week (prerequisites first)
    3. Attach free learning resources and a description
    """
    if not missing_skills:
        return []

    # Topological order (DFS-based) — prerequisites come first
    ordered = skill_graph.topological_order(missing_skills)

    # If topological sort returns empty (skills not in graph), fallback
    if not ordered:
        ordered = missing_skills

    roadmap = []
    for i, skill in enumerate(ordered, start=1):
        level = skill_graph.get_skill_level(skill)
        resources = RESOURCES.get(skill, DEFAULT_RESOURCES)
        description = SKILL_DESCRIPTIONS.get(
            skill, f"Learn and practise {skill} concepts and apply in projects"
        )
        roadmap.append({
            "week":        i,
            "skill":       skill,
            "level":       level,
            "description": description,
            "resources":   resources[:3],   # max 3 links
        })

    return roadmap
