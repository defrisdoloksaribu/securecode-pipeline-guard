
import os


def get_app_info():
    return {
        "application": "SecureCode Pipeline Guard",
        "environment": os.getenv("APP_ENV", "development"),
        "status": "running",
    }


if __name__ == "__main__":
    print(get_app_info())
