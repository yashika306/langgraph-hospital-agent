from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# -----------------------------
# Step 1: Define State Schema
# -----------------------------
class PatientState(TypedDict):
    patient_name: str
    physician_notes: str
    cardiologist_notes: str
    surgeon_notes: str


# -----------------------------
# Step 2: Create Nodes
# -----------------------------
def general_physician_node(state: PatientState) -> dict:
    print(f"General Physician examining {state['patient_name']}")
    notes = "Patient reports chest pain, shortness of breath, heart rate elevated."
    return {"physician_notes": notes}


def cardiologist_node(state: PatientState) -> dict:
    print("Cardiologist reading Physician notes")
    print(f" -> {state['physician_notes']}")
    notes = "ECG shows irregularities, recommend surgery."
    return {"cardiologist_notes": notes}


def surgeon_node(state: PatientState) -> dict:
    print("Surgeon reading Physician & Cardiologist notes")
    print(f" -> Physician: {state['physician_notes']}")
    print(f" -> Cardiologist: {state['cardiologist_notes']}")
    notes = "Surgery completed successfully, patient stable."
    return {"surgeon_notes": notes}


# -----------------------------
# Step 3: Build the Graph
# -----------------------------
graph = StateGraph(PatientState)

graph.add_node("general_physician", general_physician_node)
graph.add_node("cardiologist", cardiologist_node)
graph.add_node("surgeon", surgeon_node)

graph.add_edge(START, "general_physician")
graph.add_edge("general_physician", "cardiologist")
graph.add_edge("cardiologist", "surgeon")
graph.add_edge("surgeon", END)

app = graph.compile()


# -----------------------------
# Step 4: Run the Application
# -----------------------------
if __name__ == "__main__":
    initial_state = {
        "patient_name": "Rajesh",
        "physician_notes": "",
        "cardiologist_notes": "",
        "surgeon_notes": "",
    }

    final_state = app.invoke(initial_state)

    print("\nFinal State:")
    print(final_state)