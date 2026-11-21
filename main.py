

from client.db.database import init_db
from client.pipeline.steps import ask_ai


def main():
    ask_ai()

if __name__ == "__main__":
    init_db()
    main()
