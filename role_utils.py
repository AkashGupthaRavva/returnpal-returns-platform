import json

def get_user_role(email: str) -> str:
    try:
        with open("roles.json", "r") as f:
            roles = json.load(f)
        return roles.get(email.lower(), "unauthorized")
    except Exception as e:
        print("Error loading roles:", e)
        return "unauthorized"
