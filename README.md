# EECE435L-Final-Project

All the following steps are done inside `EECE435L-Final-Project` directory:
* Clone the GitHub Repository
* `pip install requirements.txt`
* To run all Pytest scripts: `pytest tests/`
* To run coverages:
    - Memory Profiler: `python -m memory_profiler profiling/memory_profile.py`
    - Performance Profiler: `python -m profiling.performance_profile`
    - Coverage: (will run this after codes are done during Report Composition step)
        ```bash
        coverage run -m pytest tests/
        coverage report -m
        coverage html
        python -m webbrowser -t htmlcov/index.html
        ```