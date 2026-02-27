"""
Trie Data Structure for fast skill lookup and prefix matching.
Time Complexity: O(L) for insert, search, startsWith — where L is word length.
Space Complexity: O(N * L) — N skills, average length L
"""
from typing import List, Optional, Dict


class TrieNode:
    """Single node in the Trie."""
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.full_skill: Optional[str] = None  # store original casing


class SkillTrie:
    """
    Trie for storing, searching, and prefix-matching skills.
    All operations are case-insensitive internally.
    """

    def __init__(self):
        self.root = TrieNode()
        self._count = 0

    def insert(self, skill: str) -> None:
        """Insert a skill into the trie. O(L)"""
        node = self.root
        normalized = skill.lower().strip()
        for char in normalized:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if not node.is_end:
            node.is_end = True
            node.full_skill = skill  # keep original casing
            self._count += 1

    def search(self, skill: str) -> bool:
        """Check if exact skill exists. O(L)"""
        node = self._traverse(skill.lower().strip())
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> List[str]:
        """Return all skills starting with prefix. O(L + K) K=matches"""
        results: List[str] = []
        node = self._traverse(prefix.lower().strip())
        if node is None:
            return results
        self._dfs_collect(node, results)
        return results

    def fuzzy_match(self, skill: str, max_distance: int = 1) -> Optional[str]:
        """
        Simple fuzzy match — returns closest skill within edit distance.
        Returns None if no close match found.
        """
        skill_lower = skill.lower().strip()
        # First try exact
        if self.search(skill):
            return skill
        # Try prefix match
        prefix_results = self.starts_with(skill_lower[:3]) if len(skill_lower) >= 3 else []
        for candidate in prefix_results:
            if self._edit_distance(skill_lower, candidate.lower()) <= max_distance:
                return candidate
        return None

    def bulk_insert(self, skills: List[str]) -> None:
        """Insert multiple skills at once."""
        for skill in skills:
            self.insert(skill)

    def normalize_skills(self, raw_skills: List[str]) -> List[str]:
        """
        Given a list of extracted skills,
        normalise them against the trie to handle casing/typos.
        """
        normalized = []
        for skill in raw_skills:
            if self.search(skill):
                normalized.append(skill)
            else:
                fuzzy = self.fuzzy_match(skill)
                if fuzzy:
                    normalized.append(fuzzy)
                else:
                    normalized.append(skill)  # keep as-is
        return list(dict.fromkeys(normalized))  # deduplicate, preserve order

    def __len__(self) -> int:
        return self._count

    # ── Private helpers ────────────────────────────────────────────────────────

    def _traverse(self, key: str) -> Optional[TrieNode]:
        """Walk the trie following 'key'; return final node or None."""
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs_collect(self, node: TrieNode, results: List[str]) -> None:
        """DFS from a node to collect all complete skills."""
        if node.is_end and node.full_skill:
            results.append(node.full_skill)
        for child in node.children.values():
            self._dfs_collect(child, results)

    @staticmethod
    def _edit_distance(a: str, b: str) -> int:
        """Standard dynamic programming edit distance."""
        m, n = len(a), len(b)
        dp = list(range(n + 1))
        for i in range(1, m + 1):
            prev = dp[0]
            dp[0] = i
            for j in range(1, n + 1):
                temp = dp[j]
                if a[i - 1] == b[j - 1]:
                    dp[j] = prev
                else:
                    dp[j] = 1 + min(prev, dp[j], dp[j - 1])
                prev = temp
        return dp[n]


# ─── Singleton instance loaded with known skills ───────────────────────────────
KNOWN_SKILLS = [
    # Programming Languages
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "Go", "Rust",
    "Swift", "Kotlin", "Ruby", "PHP", "Scala", "R", "MATLAB", "Perl", "Haskell",
    # Web Frontend
    "React", "Vue.js", "Angular", "Next.js", "Svelte", "HTML", "CSS", "Tailwind CSS",
    "Bootstrap", "jQuery", "Redux", "Webpack", "Vite", "GraphQL",
    # Web Backend
    "Node.js", "Express.js", "FastAPI", "Django", "Flask", "Spring Boot", "Laravel",
    "Ruby on Rails", "ASP.NET", "NestJS",
    # Databases
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "Cassandra", "SQLite", "Oracle",
    "Elasticsearch", "DynamoDB", "Supabase", "Firebase",
    # DevOps / Cloud
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD", "GitHub Actions",
    "Terraform", "Ansible", "Linux", "Nginx", "Jenkins",
    # AI / ML
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Keras",
    "scikit-learn", "NLP", "Computer Vision", "OpenCV", "Pandas", "NumPy",
    "Matplotlib", "Seaborn", "Hugging Face", "LangChain", "spaCy",
    # DSA
    "Data Structures", "Algorithms", "Dynamic Programming", "Graph Theory",
    "Binary Search", "Sorting", "Recursion", "Trees", "Hash Tables", "Trie",
    # System Design
    "System Design", "Microservices", "REST API", "gRPC", "Message Queues",
    "Kafka", "RabbitMQ", "Load Balancing", "Caching",
    # Tools
    "Git", "GitHub", "Postman", "Jira", "Figma", "VS Code", "Linux", "Bash",
    # Soft Skills
    "Communication", "Teamwork", "Problem Solving", "Leadership", "Agile", "Scrum",
]


def create_skill_trie() -> SkillTrie:
    trie = SkillTrie()
    trie.bulk_insert(KNOWN_SKILLS)
    return trie


# Global trie instance
skill_trie = create_skill_trie()
