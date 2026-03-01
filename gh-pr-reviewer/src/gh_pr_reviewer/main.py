import sys
import time
import json
import os
import argparse

# Ajustar PYTHONPATH para permitir importaciones locales si no está instalado como paquete
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from gh_pr_reviewer.crew import GhPrReviewerCrew
from gh_pr_reviewer.tools.github_tools import GitHubTools

def run_crew():
    """
    Realiza una única ejecución de la Crew sobre todas las PRs asignadas.
    """
    print(f"\n🔍 [{time.strftime('%Y-%m-%d %H:%M:%S')}] Buscando PRs asignadas globalmente...")
    
    # 1. Descubrir PRs asignadas de forma agnóstica
    prs_json = GitHubTools.search_assigned_prs.run()
    prs = json.loads(prs_json) if prs_json and not prs_json.startswith("Error") else []
    
    if not prs:
        print("📭 No hay PRs asignadas en ningún repositorio.")
        return False

    for pr in prs:
        num = pr['number']
        repo = pr['repository']['nameWithOwner']
        title = pr['title']
        
        print(f"📄 Procesando PR #{num} en {repo}: {title}")
        
        # 2. Obtener el diff para inyectarlo en la tarea
        diff = GitHubTools.get_pr_diff.run(repo=repo, pr_number=num)
        
        if not diff or diff.startswith("Error"):
            print(f"⚠️ No se pudo obtener el diff para PR #{num}. Saltando...")
            continue

        # 3. Ejecutar la Crew para esta PR específica
        inputs = {
            'pr_number': num,
            'repo_name': repo,
            'pr_title': title,
            'diff_content': diff
        }
        
        # Instanciamos la Crew y ejecutamos
        crew_instance = GhPrReviewerCrew().crew()
        result = crew_instance.kickoff(inputs=inputs)
        summary = str(result)
        
        # 4. Revisión y Aprobación final
        print(f"✍️ Publicando revisión en {repo}...")
        GitHubTools.review_and_approve_pr.run(repo=repo, pr_number=num, summary=summary)
        
        print(f"🚀 Realizando merge de PR #{num}...")
        GitHubTools.merge_pr.run(repo=repo, pr_number=num)
        
        print(f"✅ PR #{num} finalizada con éxito.")
    
    return True

def start_cron():
    """
    Ejecuta el proceso de revisión en un bucle infinito cada 60 segundos.
    """
    print("🤖 Iniciando GhPrReviewer Professional Agent (Modo CRON - 60s)...")
    print("Presiona Ctrl+C para detener el agente.")
    
    while True:
        try:
            run_crew()
        except Exception as e:
            print(f"❌ Error inesperado en el ciclo: {e}")
        
        print("😴 Esperando 60 segundos...")
        time.sleep(60)

def main():
    parser = argparse.ArgumentParser(description="GhPrReviewer: Agente de revisión de PRs profesional.")
    parser.add_argument('--once', action='store_true', help='Ejecuta la revisión una sola vez y finaliza.')
    
    args = parser.parse_args()
    
    if args.once:
        print("🚀 Ejecución puntual de GhPrReviewer...")
        run_crew()
    else:
        start_cron()

if __name__ == "__main__":
    main()
