## Text Editing Tools apply_patch (Mandatory)

When performing text editing, must use the `apply_patch` tool instead of running temporary scripts with Python commands to edit files. Your patch language is a stripped‑down, file‑oriented diff format designed to be easy to parse and safe to apply. You can think of it as a high‑level envelope:

*** Begin Patch
[ one or more file sections ]
*** End Patch

Within that envelope, you get a sequence of file operations.
You MUST include a header to specify the action you are taking.
Each operation starts with one of three headers:

*** Add File: - create a new file. Every following line is a + line (the initial contents).
*** Delete File: - remove an existing file. Nothing follows.
*** Update File: - patch an existing file in place (optionally with a rename).

Example patch:

`<br>*** Begin Patch<br>*** Add File: hello.txt<br>+Hello world<br>*** Update File: src/app.py<br>*** Move to: src/main.py<br>@@ def greet():<br>-print("Hi")<br>+print("Hello, world!")<br>*** Delete File: obsolete.txt<br>*** End Patch<br>`

It is important to remember:

- You must include a header with your intended action (Add/Delete/Update)
- You must prefix new lines with `+` even when creating a new file