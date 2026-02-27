"""
Skill Dependency Graph — DSA Core Module
========================================
Directed Graph where:
  - Node  = Skill
  - Edge  = Dependency (A → B means "learn A before B")

Algorithms used:
  - BFS : detect all missing prerequisite chains
  - DFS (via topological sort) : order missing skills for the roadmap
"""
from typing import Dict, List, Set, Optional, Tuple
from collections import deque


class SkillGraph:
    """
    Directed Adjacency-List Graph for skill dependencies.
    Edge direction: prerequisite → dependant
      e.g. "Python" → "Machine Learning"
    """

    def __init__(self):
        # adjacency list: skill → list of skills that depend on it
        self._graph: Dict[str, List[str]] = {}
        # reverse map: skill → its prerequisites
        self._prerequisites: Dict[str, List[str]] = {}

    # ── Graph Construction ─────────────────────────────────────────────────────

    def add_skill(self, skill: str) -> None:
        """Add isolated skill node."""
        skill = skill.strip()
        if skill not in self._graph:
            self._graph[skill] = []
        if skill not in self._prerequisites:
            self._prerequisites[skill] = []

    def add_dependency(self, prerequisite: str, dependant: str) -> None:
        """prerequisite must be learned before dependant."""
        prerequisite = prerequisite.strip()
        dependant = dependant.strip()
        self.add_skill(prerequisite)
        self.add_skill(dependant)
        if dependant not in self._graph[prerequisite]:
            self._graph[prerequisite].append(dependant)
        if prerequisite not in self._prerequisites[dependant]:
            self._prerequisites[dependant].append(prerequisite)

    def bulk_load(self, dependencies: List[Tuple[str, str]]) -> None:
        """Load many (prerequisite, dependant) pairs at once."""
        for pre, dep in dependencies:
            self.add_dependency(pre, dep)

    # ── BFS: Missing Prerequisite Detection ───────────────────────────────────

    def get_missing_prerequisites(
        self,
        known_skills: Set[str],
        target_skills: Set[str],
    ) -> List[str]:
        """
        BFS from each target skill backwards through prerequisites.
        Returns all skills needed but not already known.
        Time: O(V + E)
        """
        known_lower = {s.lower() for s in known_skills}
        missing: Set[str] = set()
        visited: Set[str] = set()
        queue = deque(target_skills)

        while queue:
            skill = queue.popleft()
            if skill in visited:
                continue
            visited.add(skill)

            if skill.lower() not in known_lower:
                missing.add(skill)

            # traverse backwards through prerequisites
            for prereq in self._prerequisites.get(skill, []):
                if prereq not in visited:
                    queue.append(prereq)

        # Remove skills the user already has
        missing = {s for s in missing if s.lower() not in known_lower}
        return list(missing)

    # ── DFS / Topological Sort: Roadmap Ordering ──────────────────────────────

    def topological_order(self, skills: List[str]) -> List[str]:
        """
        DFS-based topological sort of a subset of skills.
        Returns skills in learning order (prerequisites first).
        Time: O(V + E)
        """
        skill_set = set(skills)
        visited: Set[str] = set()
        stack: List[str] = []
        in_recursion: Set[str] = set()

        def dfs(node: str) -> None:
            if node in in_recursion:
                return  # cycle guard
            if node in visited or node not in skill_set:
                return
            in_recursion.add(node)
            visited.add(node)
            for prereq in self._prerequisites.get(node, []):
                if prereq in skill_set:
                    dfs(prereq)
            in_recursion.discard(node)
            stack.append(node)

        for skill in skills:
            if skill not in visited:
                dfs(skill)

        return stack  # bottom of stack = prerequisites first

    def get_skill_level(self, skill: str) -> str:
        """Heuristic: more prerequisites → higher level."""
        prereq_count = len(self._prerequisites.get(skill, []))
        if prereq_count == 0:
            return "beginner"
        elif prereq_count <= 2:
            return "intermediate"
        else:
            return "advanced"

    def get_all_skills(self) -> List[str]:
        return list(self._graph.keys())

    def __repr__(self) -> str:
        return f"SkillGraph(nodes={len(self._graph)}, edges={sum(len(v) for v in self._graph.values())})"


# ── Pre-built Dependency Graph ─────────────────────────────────────────────────
SKILL_DEPENDENCIES: List[Tuple[str, str]] = [
    # Fundamentals → Languages
    ("Algorithms", "Data Structures"),
    ("Data Structures", "Dynamic Programming"),
    ("Data Structures", "Graph Theory"),
    ("Data Structures", "Trees"),
    ("Data Structures", "Hash Tables"),
    ("Data Structures", "Trie"),
    ("Algorithms", "Binary Search"),
    ("Algorithms", "Sorting"),
    ("Recursion", "Dynamic Programming"),
    ("Recursion", "Algorithms"),

    # Python ecosystem
    ("Python", "NumPy"),
    ("Python", "Pandas"),
    ("Python", "Flask"),
    ("Python", "FastAPI"),
    ("Python", "Django"),
    ("Python", "scikit-learn"),
    ("NumPy", "Pandas"),
    ("Pandas", "Matplotlib"),
    ("Pandas", "Seaborn"),

    # ML / AI chain
    ("Python", "Machine Learning"),
    ("scikit-learn", "Machine Learning"),
    ("Machine Learning", "Deep Learning"),
    ("Deep Learning", "TensorFlow"),
    ("Deep Learning", "PyTorch"),
    ("Deep Learning", "Keras"),
    ("Python", "NLP"),
    ("Machine Learning", "NLP"),
    ("NLP", "spaCy"),
    ("NLP", "Hugging Face"),
    ("NLP", "LangChain"),
    ("Python", "Computer Vision"),
    ("Deep Learning", "Computer Vision"),
    ("Computer Vision", "OpenCV"),

    # Web Frontend
    ("HTML", "CSS"),
    ("HTML", "JavaScript"),
    ("CSS", "Tailwind CSS"),
    ("CSS", "Bootstrap"),
    ("JavaScript", "TypeScript"),
    ("JavaScript", "React"),
    ("JavaScript", "Vue.js"),
    ("JavaScript", "Angular"),
    ("React", "Next.js"),
    ("React", "Redux"),
    ("JavaScript", "jQuery"),

    # Web Backend
    ("JavaScript", "Node.js"),
    ("Node.js", "Express.js"),
    ("Node.js", "NestJS"),
    ("Java", "Spring Boot"),
    ("PHP", "Laravel"),
    ("Ruby", "Ruby on Rails"),
    ("C#", "ASP.NET"),

    # Databases
    ("SQL", "PostgreSQL"),
    ("SQL", "MySQL"),
    ("SQL", "SQLite"),

    # System Design
    ("REST API", "System Design"),
    ("Microservices", "System Design"),
    ("Caching", "System Design"),
    ("Load Balancing", "System Design"),
    ("Message Queues", "System Design"),
    ("Message Queues", "Kafka"),
    ("Message Queues", "RabbitMQ"),

    # DevOps
    ("Linux", "Docker"),
    ("Docker", "Kubernetes"),
    ("Git", "CI/CD"),
    ("CI/CD", "GitHub Actions"),
    ("Docker", "AWS"),
    ("Kubernetes", "AWS"),
    ("Docker", "GCP"),
    ("Docker", "Azure"),
    ("CI/CD", "Terraform"),
    ("Linux", "Bash"),
    ("Linux", "Nginx"),

    # DSA → Interview
    ("Data Structures", "System Design"),
    ("Algorithms", "System Design"),
    ("Graph Theory", "System Design"),
]


def create_skill_graph() -> SkillGraph:
    graph = SkillGraph()
    graph.bulk_load(SKILL_DEPENDENCIES)
    return graph


# Global graph instance
skill_graph = create_skill_graph()
