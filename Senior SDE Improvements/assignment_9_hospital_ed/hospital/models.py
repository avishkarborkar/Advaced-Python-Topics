"""
Core models for the hospital emergency department.

Supports a single ED with severity-agnostic triage (FIFO arrival order),
first-available doctor assignment, and consultation lifecycle.
"""

from enum import Enum
from datetime import datetime
from typing import Optional


class Severity(Enum):
    """
    Clinical severity, lower number = more critical.

    CRITICAL must be seen immediately.
    MINIMAL can wait longest.
    """
    CRITICAL = 1
    HIGH     = 2
    MODERATE = 3
    LOW      = 4
    MINIMAL  = 5


class Patient:
    """
    A patient who has arrived at the ED.

    severity reflects clinical acuity at arrival — it does not change
    unless a clinician reassesses and updates it directly.
    """

    def __init__(self, patient_id: str, name: str, severity: Severity):
        self.patient_id  = patient_id
        self.name        = name
        self.severity    = severity
        self.arrived_at  = datetime.now()

    def __repr__(self) -> str:
        return f"Patient({self.name}, {self.severity.name})"


class Doctor:
    """
    A doctor available for consultations.

    Doctors are either available or occupied with a consultation.
    There is no notion of specialty, shift, or department yet.
    """

    def __init__(self, doctor_id: str, name: str):
        self.doctor_id    = doctor_id
        self.name         = name
        self.is_available = True

    def __repr__(self) -> str:
        status = "available" if self.is_available else "busy"
        return f"Doctor({self.name}, {status})"


class Consultation:
    """
    An active or completed encounter between a patient and a doctor.

    Lifecycle: created → active → completed.
    A consultation is active until complete() is called.
    Completing it frees the doctor and records the outcome notes.
    """

    def __init__(self, patient: Patient, doctor: Doctor):
        self.patient      = patient
        self.doctor       = doctor
        self.started_at   = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.notes: Optional[str]             = None

    @property
    def is_active(self) -> bool:
        return self.completed_at is None

    def complete(self, notes: str) -> None:
        """
        Close this consultation. Frees the doctor and records notes.
        Raises RuntimeError if already completed.
        """
        if not self.is_active:
            raise RuntimeError(
                f"Consultation for {self.patient.name} is already completed."
            )
        self.notes        = notes
        self.completed_at = datetime.now()
        self.doctor.is_available = True

    def __repr__(self) -> str:
        status = "active" if self.is_active else "completed"
        return f"Consultation({self.patient.name} ↔ {self.doctor.name}, {status})"
