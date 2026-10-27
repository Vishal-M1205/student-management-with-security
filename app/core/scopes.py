AVAILABLE_SCOPES = {
    "me": "Read and update personal profile",
    "student:read": "View students list and marks",
    "student:write": "Create, edit, or delete student records",
    "teacher:admin": "Administrative access for teachers",
}

ROLE_SCOPES_MAP = {
    "student": ["me", "student:read"],
    "teacher": ["me", "student:read", "student:write", "teacher:admin"],
}
