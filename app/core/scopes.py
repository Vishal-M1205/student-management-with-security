AVAILABLE_SCOPES = {
    "me": "Read and update personal profile",
    "student:read": "View students list and marks",
    "student:write": "Create, edit, or delete student records",
    "teacher:admin": "Administrative access for teachers",
}

ROLE_SCOPES_MAP = {
    "student": ["me", "student:read", "subject:read", "result:read"],
    "teacher": [
        "teacher",
        "student:read",
        "student:write",
        "subject:read",
        "subject:manage",
        "result:read",
    ],
}
