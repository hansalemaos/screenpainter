from nutikacompile import compile_with_nuitka

wholecommand2 = compile_with_nuitka(
    pyfile=r"C:\ProgramData\anaconda3\envs\nu\screenpaint.py",
    icon=r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico",
    disable_console=True,
    file_version="1.0.0.4",
    onefile=True,
    outputdir="c:\\screenma",
    addfiles=[
r"C:\ProgramData\anaconda3\envs\nu\iconapp.ico",
r"C:\ProgramData\anaconda3\envs\nu\colordrawc.exp",
r"C:\ProgramData\anaconda3\envs\nu\colordrawc.lib",
r"C:\ProgramData\anaconda3\envs\nu\colordrawc.so",
r"C:\ProgramData\anaconda3\envs\nu\ctypesdrawconfig.ini",

    ],
    delete_onefile_temp=False,
    needs_admin=True,
    arguments2add="--msvc=14.3 --noinclude-numba-mode=nofollow --plugin-enable=tk-inter --jobs=1"
)
