"""
A little fake application to be used as a plantuml.jar dropin
It is used to capture the arguments plantuml is called with and returns a fake
'image' which stores the command line plantuml would have been called with for
that file.
"""
import sys
import os
import json
import file_locations

if __name__ == "__main__":
    # Generate the dummy image
    img_filename, _ = os.path.splitext(sys.argv[-1])
    if "-tsvg" in sys.argv:
        img_filename += ".svg"
    else:
        img_filename += ".png"

    # Dump the command line arguments and resulting image location in the
    # 'image file'. The tester can then check these for validity
    # We need to create an image file, so mdbook-plantuml has something to chew
    # on.
    open(img_filename, "w").write(" ".join(sys.argv))

    # Append command output to calls file
    try:
        prev_commands = json.load(open(file_locations.get_shell_calls_file()))
    except IOError:
        prev_commands = []

    prev_commands.append({
        "arguments": sys.argv[1:],
        "plantuml-code": open(sys.argv[-1], "rt").read().strip()
    })

    json.dump(
        prev_commands,
        open(file_locations.get_shell_calls_file(), "wt"),
        indent=2
    )
