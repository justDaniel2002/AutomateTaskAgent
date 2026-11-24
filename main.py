

from client.db.database import init_db
from client.pipeline.runner import runner


def main():
    runner()

if __name__ == "__main__":
    init_db()
    main()
