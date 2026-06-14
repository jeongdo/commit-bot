# C:\Dropbox\Python\source\python3\src\venv>python -m venv inflearn
#
# C:\Dropbox\Python\source\python3\src\venv>
# C:\Dropbox\Python\source\python3\src\venv>cd inflearn
# C:\Dropbox\Python\source\python3\src\venv\inflearn>cd Scripts
# C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>activate           # 가상환경 실행

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>pip install -U pip

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>pip list
# Package    Version
# ---------- -------
# pip        20.1.1
# setuptools 47.1.0

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>pip install pendulum

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>pip list
# Package         Version
# --------------- -------
# pendulum        2.1.0
# pip             20.1.1
# python-dateutil 2.8.1
# pytzdata        2019.3
# setuptools      47.1.0
# six             1.15.0

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>pip install pytest

# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn>pytest test.py  #가상환경에서만 실행 가능
# ================================================= test session starts =================================================
# platform win32 -- Python 3.7.8, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
# rootdir: C:\Dropbox\Python\source\python3\src\venv\inflearn
# collected 0 items
#
# ================================================ no tests ran in 0.25s ================================================
#
# (inflearn) C:\Dropbox\Python\source\python3\src\venv\inflearn>

# C:\Dropbox\Python\source\python3\src\venv\inflearn\Scripts>deactivate.bat     # 가상환경 해제

# 콘솔에서 해당 디렉토리로 이동 후

# C:\Dropbox\Python\source\python3\src\venv\inflearn>python test.py
# <class 'pendulum.tz.timezone.Timezone'>
# Current Date Time in PST = 2020-07-01 19:32:53.992863-07:00
# Current Date Time in IST = 2020-07-02 11:32:53.993863+09:00
# <class 'pendulum.tz.timezone.Timezone'>

