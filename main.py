from src import create_app
import sys, os

from src.db import Db
from src.params import get_params, params

app = create_app()


def main():
    """main function"""

    print(sys.argv[0])

    if len(sys.argv) < 3:
        print("Usage: python utils/reboot.py [dev|main] [create|drop|boot|reboot]")
        sys.exit()

    # argv1 : dev main
    if sys.argv[1] == "main":
        params = get_params("main")
    else:
        params = get_params("dev")

    engine = Db.engine(params=params)
    session = Db.session(params=params)

    # argv2 : function
    if sys.argv[2] == "create":
        Db.create_all(engine=engine)
    elif sys.argv[2] == "drop":
        Db.drop_all(engine=engine)
    elif sys.argv[2] == "boot":
        Db.boot(engine=engine)
    elif sys.argv[2] == "reboot":
        Db.reboot(engine=engine)


if __name__ == "__main__":
    main()
