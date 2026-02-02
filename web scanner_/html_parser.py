from bs4 import BeautifulSoup
from typing import List, Dict


def parse_html(html: str) -> BeautifulSoup:
    """
    Parse raw HTML into a DOM tree.
    """
    return BeautifulSoup(html, "html.parser")


def extract_forms(dom: BeautifulSoup) -> List[Dict]:
    """
    Extract forms and their inputs from the DOM.
    Returns a list of forms with method, action, and inputs.

    If no forms are found, returns an empty list and logs a note.
    """
    forms_data = []

    forms = dom.find_all("form")

    if not forms:
        # Informational note, not an error
        print(
            "[INFO] No HTML <form> elements found. "
            "Note: Modern JavaScript-driven sites may render forms dynamically."
        )
        return forms_data

    for form in forms:
        method = form.get("method", "get").lower()
        action = form.get("action", "")

        inputs_data = []
        inputs = form.find_all("input")
        for inp in inputs:
            input_type = inp.get("type", "text").lower()
            inputs_data.append({
                "name": inp.get("name"),
                "type": input_type,
                "hidden": input_type == "hidden"
            })

        forms_data.append({
            "method": method,
            "action": action,
            "inputs": inputs_data
        })

    return forms_data