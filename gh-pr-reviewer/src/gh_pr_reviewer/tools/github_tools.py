import subprocess
import json
from crewai.tools import tool

class GitHubTools:
    @tool("search_assigned_prs")
    def search_assigned_prs() -> str:
        """Busca todas las Pull Requests abiertas asignadas al usuario actual en cualquier repositorio."""
        try:
            # Buscamos PRs abiertas asignadas a mí de forma global
            cmd = ["gh", "search", "prs", "--assignee", "@me", "--state", "open", "--json", "number,title,repository,url"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout
        except Exception as e:
            return f"Error buscando PRs: {str(e)}"

    @tool("get_pr_diff")
    def get_pr_diff(repo: str, pr_number: int) -> str:
        """Obtiene el diff de una Pull Request específica usando el nombre del repositorio y el número de PR."""
        try:
            cmd = ["gh", "pr", "diff", str(pr_number), "-R", repo]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout[:5000]
        except Exception as e:
            return f"Error obteniendo diff: {str(e)}"

    @tool("review_and_approve_pr")
    def review_and_approve_pr(repo: str, pr_number: int, summary: str) -> str:
        """Aprueba una Pull Request con un comentario resumen técnico."""
        try:
            # Intentamos aprobar
            cmd = ["gh", "pr", "review", str(pr_number), "-R", repo, "--approve", "-b", summary]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Fallback si no se puede aprobar (voto propio)
            if result.returncode != 0:
                cmd = ["gh", "pr", "review", str(pr_number), "-R", repo, "--comment", "-b", summary]
                subprocess.run(cmd, capture_output=True, text=True, check=True)
                return "PR comentada exitosamente (autorevisión)."
            
            return "PR aprobada exitosamente."
        except Exception as e:
            return f"Error en revisión: {str(e)}"

    @tool("merge_pr")
    def merge_pr(repo: str, pr_number: int) -> str:
        """Realiza el merge (squash) de una Pull Request y elimina la rama de origen."""
        try:
            cmd = ["gh", "pr", "merge", str(pr_number), "-R", repo, "--squash", "--delete-branch"]
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            return "PR mergeada exitosamente."
        except Exception as e:
            return f"Error en merge: {str(e)}"
