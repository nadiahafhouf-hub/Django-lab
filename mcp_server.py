import os
import django
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionConference.settings')
django.setup()

# Importation des modèles Django après initialisation
from ConferenceApp.models import Conference
from SessionApp.models import Session

# Créer un MCP server
mcp = FastMCP("Conference Assistant")

# === TOOLS ===

@mcp.tool()
async def list_conferences():
    """Liste toutes les conférences disponibles."""
    @sync_to_async
    def get_conferences():
        return list(Conference.objects.all())
    
    conferences = await get_conferences()
    if not conferences:
        return "Aucune conférence disponible."
    return "\n".join([f"{conf.conference_id}: {conf.name} ({conf.start_date})" for conf in conferences])


@mcp.tool()
async def get_conference_details(name: str) -> str:
    """Récupère les détails d'une conférence par son nom."""
    @sync_to_async
    def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"
        
    conference = await _get_conference()
    if conference == "MULTIPLE":
        return f"Plusieurs conférences trouvées avec le nom '{name}'. Veuillez préciser."
    if not conference:
        return f"Aucune conférence trouvée avec le nom '{name}'."
    
    return (
        f"Détails de la conférence '{conference.name}':\n"
        f"Theme: {conference.theme}\n"
        f"Date: {conference.start_date} to {conference.end_date}\n"
        f"Lieu: {conference.location}\n"
        f"Description: {conference.description}"
    )


@mcp.tool()
async def list_sessions(conference_name: str) -> str:
    """Liste toutes les sessions d'une conférence donnée."""
    @sync_to_async
    def _get_sessions():
        try:
            conference = Conference.objects.get(name__icontains=conference_name)
            return list(Session.objects.filter(conference=conference)), conference
        except Conference.DoesNotExist:
            return None, None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE", None

    result, conference = await _get_sessions()
    if result == "MULTIPLE":
        return f"Plusieurs conférences trouvées avec le nom '{conference_name}'. Veuillez préciser."
    if conference is None:
        return f"Conference '{conference_name}' not found."
    
    sessions = result
    if not sessions:
        return f"Aucune session trouvée pour la conférence '{conference.name}'."

    session_list = []
    for s in sessions:
        session_list.append(
            f"- {s.title} ({s.start_time} - {s.end_time}) in {s.room}\n"
            f"  Topic: {s.topic}"
        )
    return "\n".join(session_list)

@mcp.tool()
async def filter_conferences_by_duration(min_days: int = 1, max_days: int = 3) -> str:
    """Filtre les conférences dont la durée est comprise entre min_days et max_days."""
    @sync_to_async
    def _get_filtered():
        conferences = Conference.objects.all()
        filtered = [
            c for c in conferences
            if (c.end_date - c.start_date).days + 1 >= min_days
            and (c.end_date - c.start_date).days + 1 <= max_days
        ]
        return filtered
    
    filtered = await _get_filtered()
    if not filtered:
        return f"Aucune conférence trouvée avec une durée entre {min_days} et {max_days} jours."
    
    return "\n".join([
        f"{c.name}: {c.start_date} to {c.end_date} ({(c.end_date - c.start_date).days + 1} jours)"
        for c in filtered
    ])



# === Lancement du serveur ===
if __name__ == "__main__":
    mcp.run(transport="stdio")