"""
Triage system for the emergency department.

Current behaviour:
  - Patients are seen in arrival order (FIFO).
  - The first available doctor is assigned, regardless of who the patient is.
  - One consultation per patient at a time.

This module is intentionally simple. Extensions should add richer matching
without rewriting the fundamentals here unless there is a clear reason to.
"""

from typing import Dict, List, Optional
from .models import Patient, Doctor, Consultation, Severity

class TriageQueue:
    """
    Manages the ED patient queue and doctor assignment.

    Responsibilities:
      - Holds the ordered waiting list of patients
      - Holds the registered doctor pool
      - Matches patients to doctors and tracks consultations

    Matching strategy: arrival-order patient + first-available doctor (FIFO × FIFO).
    """

    def __init__(self):
        self._waiting: List[Patient]               = []
        self._doctors: Dict[str, Doctor]           = {}
        self._consultations: List[Consultation]    = []

    def register_doctor(self, doctor: Doctor) -> None:
        """Add a doctor to the pool."""
        self._doctors[doctor.doctor_id] = doctor

    def add_patient(self, patient: Patient) -> None:
        """Enqueue a patient. Position reflects arrival order."""
        self._waiting.append(patient)

    def _pick_priority_patient(self) -> Optional[Patient]:
        if not self._waiting:
            return None
        patient = min(self._waiting, key=lambda p: (p.severity.value, p.arrived_at))
        self._waiting.remove(patient)
        return patient

    def assign_next(self) -> Optional[Consultation]:

        available_doctor = next(
            (d for d in self._doctors.values() if d.is_available),
            None
        )
        if available_doctor is None:
            return None

        patient = self._pick_priority_patient()
        if patient is None:
            return None
        available_doctor.is_available = False
        consultation = Consultation(patient=patient, doctor=available_doctor)
        self._consultations.append(consultation)
        return consultation



    # ------------------------------------------------------------------ #
    # Completion                                                           #
    # ------------------------------------------------------------------ #

    def complete_consultation(self, consultation: Consultation, notes: str) -> None:
        """
        Close a consultation. Frees the doctor for new assignments.
        Raises ValueError if the consultation is not managed by this queue.
        Raises RuntimeError (from Consultation.complete) if already completed.
        """
        if consultation not in self._consultations:
            raise ValueError("Consultation not managed by this triage queue.")
        consultation.complete(notes)

    # ------------------------------------------------------------------ #
    # Queries                                                              #
    # ------------------------------------------------------------------ #

    def get_waiting(self) -> List[Patient]:
        """Snapshot of the current waiting list, in queue order."""
        return list(self._waiting)

    def get_active_consultations(self) -> List[Consultation]:
        """All consultations that have not yet been completed."""
        return [c for c in self._consultations if c.is_active]

    def get_completed_consultations(self) -> List[Consultation]:
        """All consultations that have been completed."""
        return [c for c in self._consultations if not c.is_active]

    def all_consultations(self) -> List[Consultation]:
        """Every consultation ever created by this queue."""
        return list(self._consultations)
