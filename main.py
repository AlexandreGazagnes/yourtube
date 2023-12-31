from src import create_app
import sys, os

from src.db import Db
from src.params import get_params, params

# from src.home.functions import HomeFunctions


# from src.videos.functions import fix_videos

from src.core.videos.functions import CoreVideoFuncions

app = create_app()


def main():
    """main function"""

    print(sys.argv[0])

    if len(sys.argv) < 3:
        print("Usage: python utils/reboot.py [dev|main] [create|drop|boot|reboot]")
        sys.exit()

    # argv1 : dev main

    if not sys.argv[1] in ["dev", "main"]:
        print("Error: unknown argument: ", sys.argv[1])
        sys.exit()

    params = get_params("main") if sys.argv[1] == "main" else get_params("dev")

    engine = Db.engine(params=params)
    # session = Db.session(params=params)

    functions_mapping = {
        "create": (Db.create_all, {"engine": engine}),
        "drop": (Db.drop_all, {"engine": engine}),
        "boot": (Db.boot, {"engine": engine}),
        "reboot": (Db.reboot, {"engine": engine}),
        # "fix": (HomeFunctions.fix, {"engine": engine}),
        "fix_videos": (CoreVideoFuncions.fix_old_videos, {"engine": engine}),
        "export": (Db.export, {"engine": engine}),
        "update": (
            CoreVideoFuncions.update,
            {"engine": engine, "new": True, "old": True, "random_": True},
        ),
        "update_new": (
            CoreVideoFuncions.update,
            {"engine": engine, "new": True, "old": False, "random_": True},
        ),
        "update_old": (
            CoreVideoFuncions.update,
            {"engine": engine, "new": False, "old": True, "random_": False},
        ),
        "update_all": (
            CoreVideoFuncions.update,
            {"engine": engine, "new": True, "old": True, "random_": False},
        ),
    }

    for arg_n in sys.argv[2:]:
        if arg_n in functions_mapping.keys():
            print(arg_n)
            func, kwargs = functions_mapping[arg_n]
            func(**kwargs)
        else:
            print("Error: unknown argument: ", arg_n)
            sys.exit()


if __name__ == "__main__":
    main()
