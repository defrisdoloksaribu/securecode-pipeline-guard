\# SecureCode Pipeline Guard



An automated security scanning pipeline that helps detect insecure Python code, vulnerable dependencies, and accidentally committed secrets before changes are merged.



\## Project Overview



SecureCode Pipeline Guard integrates security checks into a CI/CD workflow. It uses automated scanners to identify potential security issues and helps prevent problematic code from progressing through the pipeline.



\## Security Tools



\- \*\*Bandit (SAST):\*\* Scans Python source code for common security issues.

\- \*\*pip-audit (SCA):\*\* Checks Python package dependencies for known vulnerabilities.

\- \*\*Gitleaks:\*\* Detects potential secrets accidentally committed to the repository.

\- \*\*GitHub Actions:\*\* Automates security checks on pushes and pull requests.

\- \*\*Python unittest:\*\* Tests the custom security gate logic.



\## Security Gate



The custom security gate evaluates JSON security reports and blocks findings classified as `HIGH` or `CRITICAL`.



Current automated tests verify that:

\- Reports with no findings pass.

\- `LOW` findings pass.

\- `HIGH` findings fail.

\- `CRITICAL` findings fail.



\## Project Structure



```text

securecode-pipeline-guard/

├── .github/

│   └── workflows/

│       └── security.yml

├── app/

│   ├── main.py

│   └── security\_gate.py

├── tests/

│   └── test\_security\_gate.py

├── .gitignore

├── LICENSE

└── README.md

```



\## Run Locally



Create and activate a Python virtual environment, then install the security tools:



```bash

python -m pip install bandit pip-audit

```



Run the unit tests:



```bash

python -m unittest discover -s tests -v

```



Scan Python source code:



```bash

bandit -r app -ll

```



Audit installed Python packages:



```bash

pip-audit

```



Run Gitleaks on the application directory using the Gitleaks binary installed locally:



```bash

gitleaks dir app

```



\## Current Validation



The following local checks have been executed successfully during development:



\- Unit tests: 4 passed.

\- Bandit: no issues identified in the scanned application code.

\- pip-audit: no known vulnerabilities found in the checked environment.

\- Gitleaks: no leaks found in the `app/` directory.



These results describe the checks performed so far and do not guarantee that the entire project is free of security vulnerabilities.



\## CI/CD



The GitHub Actions workflow is configured to run unit tests, Bandit, pip-audit, and Gitleaks on repository events. The workflow must be executed on GitHub to confirm its end-to-end behavior.



\## Project Goals



\- Shift security checks earlier in the development lifecycle.

\- Detect potential security issues automatically.

\- Fail CI checks when configured security requirements are not met.

\- Demonstrate practical DevSecOps principles.



\## Disclaimer



This project is intended for educational and demonstration purposes. Security scanner results require review and do not replace a comprehensive security assessment.



