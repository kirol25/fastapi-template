import argparse
import json
import sys

import yaml
from uvicorn.importer import import_from_string


def parse_args():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(prog="extract-openapi.py")
    parser.add_argument(
        "app", help='App import string. Example: "main:app"', default="main:app"
    )
    parser.add_argument("--app-dir", help="Directory containing the app", default=None)
    parser.add_argument(
        "--out", help="Output file ending in .json or .yaml", default="openapi.yaml"
    )
    return parser.parse_args()


def main():
    """
    Main function to extract OpenAPI spec from a FastAPI application and write it to a file.
    """
    args = parse_args()

    if args.app_dir is not None:
        print(f"Adding {args.app_dir} to sys.path")
        sys.path.insert(0, args.app_dir)

    print(f"Importing app from {args.app}")
    app = import_from_string(args.app)
    openapi = app.openapi()
    version = openapi.get("openapi", "unknown version")

    print(f"Writing OpenAPI spec v{version}")
    with open(args.out, "w") as f:
        if args.out.endswith(".json"):
            json.dump(openapi, f, indent=2)
        else:
            yaml.dump(openapi, f, sort_keys=False)

    print(f"Spec written to {args.out}")


if __name__ == "__main__":
    main()
