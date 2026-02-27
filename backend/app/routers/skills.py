from fastapi import APIRouter
from app.services.skill_trie import skill_trie, KNOWN_SKILLS
from app.services.skill_graph import skill_graph

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.get("/", summary="List all known skills")
async def list_skills():
    return {"skills": sorted(KNOWN_SKILLS), "count": len(KNOWN_SKILLS)}


@router.get("/search/{prefix}", summary="Prefix search skills via Trie")
async def search_skills(prefix: str):
    results = skill_trie.starts_with(prefix)
    return {"prefix": prefix, "matches": results, "count": len(results)}


@router.get("/dependencies/{skill}", summary="Get prerequisites for a skill")
async def skill_dependencies(skill: str):
    from app.services.skill_graph import SKILL_DEPENDENCIES
    prerequisites = [pre for pre, dep in SKILL_DEPENDENCIES if dep.lower() == skill.lower()]
    dependants    = [dep for pre, dep in SKILL_DEPENDENCIES if pre.lower() == skill.lower()]
    level         = skill_graph.get_skill_level(skill)
    return {
        "skill":         skill,
        "level":         level,
        "prerequisites": prerequisites,
        "enables":       dependants,
    }


@router.get("/graph", summary="Return full dependency graph edges")
async def get_graph():
    from app.services.skill_graph import SKILL_DEPENDENCIES
    return {
        "nodes": skill_graph.get_all_skills(),
        "edges": [{"from": pre, "to": dep} for pre, dep in SKILL_DEPENDENCIES],
    }
