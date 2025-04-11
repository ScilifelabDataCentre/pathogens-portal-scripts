import requests
import datetime
import json
import time
import logging

# --- Constants ---
API_URL = "https://swecris-api.vr.se/v1/projects"
AUTH_TOKEN = "VRSwecrisAPI2024-1" # TODO: This is a testing token provided publically by VR. We need to get a new token for our own use.
PAGE_SIZE = 100
TODAY = datetime.date.today()
UNKNOWN = "Unknown"

# --- Topic keywords --- avoid acronymn
TOPIC_KEYWORDS = {
    "Antibiotic resistance": ["antibiotic resistance", "antimicrobial resistance", "antimicrobial"],
    "COVID-19": ["covid","SARS-CoV-2"],
    "Enteric viruses": ["norovirus", "rotavirus", "enteric virus"],
    "Infectious diseases": ["infectious disease", "pathogen"],
    "Influenza": ["influenza", "influensa", "H1N1", "H3N2"],
    "Mpox": ["mpox", "monkeypox"],
    "Respiratory Syncytial Virus (RSV)": ["respiratory syncytial virus"]
}

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Functions ---
def fetch_all_projects():
    """Fetch all projects from the SweCRIS API."""
    logging.info("Fetching projects from SweCRIS...")
    try:
        response = requests.get(
            API_URL,
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {AUTH_TOKEN}"
            }
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch projects: {e}")
        return []

    projects = response.json()
    logging.info(f"Fetched {len(projects)} projects.")
    return projects


def is_ongoing(project):
    """Check if a project is ongoing based on its start and end dates."""
    try:
        start = datetime.datetime.strptime(project["projectStartDate"].split()[0], "%Y-%m-%d").date()
        end = datetime.datetime.strptime(project["projectEndDate"].split()[0], "%Y-%m-%d").date()
        return start <= TODAY <= end
    except (KeyError, ValueError) as e:
        logging.warning(f"Error parsing dates for project {project.get('projectId', UNKNOWN)}: {e}")
        return False


def match_topics(project):
    """Match project topics based on keywords."""
    text = " ".join([
        str(project.get("projectTitleEn") or project.get("projectTitleSv", "")),
        str(project.get("projectAbstractEn", ""))
    ]).lower()

    matched_topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            matched_topics.append(topic)
    return matched_topics


def format_project(project, topics):
    """Format a project for output."""
    funder = project.get("fundingOrganisationNameEn", UNKNOWN)
    title = project.get("projectTitleEn") or project.get("projectTitleSv", UNKNOWN)

    amount = f"{project.get('fundingsSek', 0):,} kr".replace(",", " ")
    start = project.get("projectStartDate", "").split()[0]
    end = project.get("projectEndDate", "").split()[0]
    project_id = project.get("projectId", "")
    url = f"https://www.vr.se/english/swecris.html#/project/{project_id}"

    pi = UNKNOWN
    affiliation = UNKNOWN
    for person in project.get("peopleList", []):
        if person.get("roleEn") == "Principal Investigator":
            pi = person.get("fullName", pi)
            affiliation = project.get("coordinatingOrganisationNameEn", affiliation)
            break

    return {
        "topic": topics,
        "funder": funder,
        "project_title": title,
        "funding_amount": amount,
        "pi": pi,
        "pi_affiliation": affiliation,
        "startdate": start,
        "enddate": end,
        "url": url
    }


# --- Main Execution ---
if __name__ == "__main__":
    all_projects = fetch_all_projects()

    # Filter ongoing projects
    ongoing_projects = [p for p in all_projects if is_ongoing(p)]

    # Filter by topic
    final_output = []
    for project in ongoing_projects:
        topics = match_topics(project)
        if topics:
            formatted_project = format_project(project, topics)
            if formatted_project:
                final_output.append(formatted_project)

    # Prepare the final JSON structure
    output_data = {
        "last_updated": TODAY.isoformat(),
        "projects": final_output
    }

    # Save to JSON
    output_file = "ongoing_projects/data/ongoing_research_projects.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)

    logging.info(f"✅ Done. Saved {len(final_output)} topic-matched ongoing projects to: {output_file}")
