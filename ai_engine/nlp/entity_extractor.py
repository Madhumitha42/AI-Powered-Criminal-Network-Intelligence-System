import re
from typing import Dict, List, Any

try:
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = spacy.blank("en")
except ImportError:
    nlp = None

class EntityExtractor:
    def __init__(self):
        # Regex patterns for high-precision Indian security/investigation entities
        self.phone_pattern = re.compile(r'(\+91[\-\s]?\d{10}|\b\d{10}\b)')
        self.vehicle_pattern = re.compile(r'\b[A-Z]{2}[\-\s]?\d{2}[\-\s]?[A-Z]{1,2}[\-\s]?\d{4}\b')
        self.location_keywords = ['Bandra', 'Kurla', 'Hinjewadi', 'Pune', 'Thane', 'Nashik', 'Nagpur', 'Aurangabad', 'MIDC', 'Dock', 'Hub', 'Highway']

    def extract_entities_from_text(self, text: str) -> Dict[str, List[Dict[str, Any]]]:
        extracted = {
            "persons": [],
            "vehicles": [],
            "communications": [],
            "locations": [],
            "organizations": []
        }

        # Regex Extraction for Comms
        phones = self.phone_pattern.findall(text)
        for p in set(phones):
            extracted["communications"].append({"identifier": p, "type": "Phone"})

        # Regex Extraction for Vehicles (e.g. MH-02-AB-9901)
        vehicles = self.vehicle_pattern.findall(text)
        for v in set(vehicles):
            extracted["vehicles"].append({"plate_number": v, "type": "Vehicle"})

        # spaCy Extraction for Persons & Locations & Orgs
        if nlp:
            doc = nlp(text)
            for ent in doc.ents:
                if ent.label_ in ["PERSON", "PER"]:
                    if len(ent.text.strip()) > 2 and not any(p['name'] == ent.text for p in extracted["persons"]):
                        extracted["persons"].append({"name": ent.text.strip(), "confidence": 0.88})
                elif ent.label_ in ["GPE", "LOC", "FAC"]:
                    if not any(l['name'] == ent.text for l in extracted["locations"]):
                        extracted["locations"].append({"name": ent.text.strip(), "type": "Location"})
                elif ent.label_ == "ORG":
                    if not any(o['name'] == ent.text for o in extracted["organizations"]):
                        extracted["organizations"].append({"name": ent.text.strip(), "type": "Organization"})

        # Keyword Fallback for Locations if spaCy missed
        for kw in self.location_keywords:
            if kw.lower() in text.lower() and not any(l['name'].lower() == kw.lower() for l in extracted["locations"]):
                extracted["locations"].append({"name": kw, "type": "Location"})

        return extracted

entity_extractor = EntityExtractor()
