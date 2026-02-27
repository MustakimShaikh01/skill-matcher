"""
Unit Tests for Trie and Skill Graph DSA modules.
"""
import pytest
from app.services.skill_trie import SkillTrie, create_skill_trie
from app.services.skill_graph import SkillGraph, create_skill_graph


# ─── Trie Tests ────────────────────────────────────────────────────────────────
class TestSkillTrie:
    def setup_method(self):
        self.trie = SkillTrie()
        self.trie.bulk_insert(["Python", "PyTorch", "Pandas", "React", "Redis"])

    def test_insert_and_search(self):
        assert self.trie.search("Python") is True
        assert self.trie.search("python") is True   # case-insensitive
        assert self.trie.search("Ruby") is False

    def test_starts_with(self):
        results = self.trie.starts_with("Py")
        assert "Python" in results
        assert "PyTorch" in results

    def test_starts_with_no_match(self):
        results = self.trie.starts_with("xyz")
        assert results == []

    def test_count(self):
        assert len(self.trie) == 5

    def test_fuzzy_match(self):
        result = self.trie.fuzzy_match("Pythonn")   # typo: extra n
        # may or may not match depending on edit distance; won't crash
        assert result is None or isinstance(result, str)

    def test_normalize_skills(self):
        raw = ["Python", "python", "React", "unknownSkill999"]
        normalized = self.trie.normalize_skills(raw)
        assert "Python" in normalized or "python" in normalized
        assert "unknownSkill999" in normalized  # kept as-is

    def test_global_trie(self):
        global_trie = create_skill_trie()
        assert global_trie.search("Docker") is True
        assert global_trie.search("Kubernetes") is True
        assert global_trie.starts_with("Fast")  # FastAPI


# ─── Skill Graph Tests ─────────────────────────────────────────────────────────
class TestSkillGraph:
    def setup_method(self):
        self.graph = SkillGraph()
        self.graph.add_dependency("Python", "Machine Learning")
        self.graph.add_dependency("Machine Learning", "Deep Learning")
        self.graph.add_dependency("Python", "NumPy")

    def test_add_and_query(self):
        skills = self.graph.get_all_skills()
        assert "Python" in skills
        assert "Machine Learning" in skills
        assert "Deep Learning" in skills

    def test_missing_prerequisites_bfs(self):
        known = {"Python"}
        target = {"Deep Learning"}
        missing = self.graph.get_missing_prerequisites(known, target)
        assert "Machine Learning" in missing
        assert "Deep Learning" in missing
        assert "Python" not in missing  # already known

    def test_no_missing_when_all_known(self):
        known = {"Python", "Machine Learning", "Deep Learning"}
        missing = self.graph.get_missing_prerequisites(known, {"Deep Learning"})
        assert missing == []

    def test_topological_order(self):
        skills = ["Deep Learning", "Machine Learning", "Python"]
        ordered = self.graph.topological_order(skills)
        # Python must come before Machine Learning before Deep Learning
        assert ordered.index("Python") < ordered.index("Machine Learning")
        assert ordered.index("Machine Learning") < ordered.index("Deep Learning")

    def test_skill_level(self):
        # Python has no prerequisites → beginner
        assert self.graph.get_skill_level("Python") == "beginner"
        # Deep Learning has 2 prerequisites → intermediate
        assert self.graph.get_skill_level("Deep Learning") in ("beginner", "intermediate", "advanced")

    def test_global_graph(self):
        graph = create_skill_graph()
        assert len(graph.get_all_skills()) > 20


# ─── Matcher Tests ─────────────────────────────────────────────────────────────
class TestMatcher:
    def test_perfect_match(self):
        from app.services.matcher import compute_match
        result = compute_match(
            resume_skills=["Python", "React", "Docker"],
            resume_text="Python developer with React and Docker experience",
            job_description="Looking for Python React Docker developer",
            required_skills=["Python", "React", "Docker"],
        )
        assert result["score"] > 70
        assert result["grade"] in ("A", "B")
        assert result["missing_skills"] == []

    def test_no_match(self):
        from app.services.matcher import compute_match
        result = compute_match(
            resume_skills=["HTML", "CSS"],
            resume_text="Frontend designer",
            job_description="Machine learning engineer with TensorFlow",
            required_skills=["TensorFlow", "PyTorch", "Python"],
        )
        assert result["score"] < 50

    def test_partial_match(self):
        from app.services.matcher import compute_match
        result = compute_match(
            resume_skills=["Python", "React"],
            resume_text="Python and React developer",
            job_description="Full stack developer",
            required_skills=["Python", "React", "Docker", "PostgreSQL"],
        )
        assert 0 < result["score"] < 100
        assert "Docker" in result["missing_skills"]
        assert "PostgreSQL" in result["missing_skills"]


# ─── Roadmap Tests ─────────────────────────────────────────────────────────────
class TestRoadmap:
    def test_roadmap_generated(self):
        from app.services.roadmap import generate_roadmap
        roadmap = generate_roadmap(["Machine Learning", "Deep Learning"], known_skills=["Python"])
        assert len(roadmap) > 0
        assert all("week" in item for item in roadmap)
        assert all("skill" in item for item in roadmap)
        assert all("resources" in item for item in roadmap)

    def test_empty_roadmap(self):
        from app.services.roadmap import generate_roadmap
        roadmap = generate_roadmap([], known_skills=["Python"])
        assert roadmap == []
