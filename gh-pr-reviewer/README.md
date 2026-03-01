# GhPrReviewer: Profesional GitHub Agent 🚀⚖️

Este proyecto es un agente especializado en revisión de código basado en **CrewAI** y **Ollama**. Está diseñado para detectar, analizar, comentar y mergear Pull Requests asignadas a ti de forma totalmente automática y agnóstica (funciona en cualquier repositorio).

## 📋 Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener:

1.  **Python 3.10+**
2.  **GitHub CLI (`gh`)**: Instalado y autenticado (`gh auth login`).
3.  **Ollama**: Instalado y con el modelo `deepseek-coder-v2:16b` descargado (`ollama pull deepseek-coder-v2:16b`).

## 🛠️ Instalación y Configuración

Sigue estos pasos para montar el entorno en un ordenador nuevo:

1.  **Clonar/Mover el proyecto**:
    Copia la carpeta del proyecto a tu nuevo equipo.

2.  **Crear el entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # venv\Scripts\activate   # En Windows
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar el PYTHONPATH**:
    Para que las importaciones internas funcionen correctamente:
    ```bash
    export PYTHONPATH=$PYTHONPATH:$(pwd)/src
    ```

## 🚀 Uso

El agente tiene dos modos de ejecución profesionales:

### 1. Modo CRON (Bucle continuo)
Escanea PRs asignadas cada 60 segundos, las analiza y las mergea automáticamente.
```bash
python src/gh_pr_reviewer/main.py
```

### 2. Modo Ejecución Única (`--once`)
Útil para ejecuciones puntuales o disparadores externos. Procesa las PRs actuales y finaliza.
```bash
python src/gh_pr_reviewer/main.py --once
```

## 🏗️ Estructura del Proyecto

-   `src/gh_pr_reviewer/config/`: Contiene `agents.yaml` y `tasks.yaml` para definir el comportamiento del agente.
-   `src/gh_pr_reviewer/tools/`: Herramientas personalizadas para interactuar con GitHub CLI.
-   `src/gh_pr_reviewer/crew.py`: Lógica de orquestación de CrewAI.
-   `src/gh_pr_reviewer/main.py`: Punto de entrada con control de modo de ejecución.

## ⚖️ Filosofía del Agente
El agente está configurado para ser **objetivo y proporcional**. No genera resúmenes exagerados; reporta hechos técnicos verificables del diff y garantiza que las PRs se integren de forma limpia.

---
**Revisado y procesado automáticamente por Antigravity.**
