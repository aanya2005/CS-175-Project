# Text2SQL-LeGoat

Text2SQL-LeGoat is a project for exploring text-to-SQL models and database interactions. This repository is set up for collaboration and reproducible development.

---

## Project Structure

```
Text2SQL-LeGoat/
├── data/
│   └── spider/
├── src/
│   ├── data_exploration.py
│   ├── visualization.py
│   └── utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Setup Instructions

1. **Clone the repository**
```powershell
git clone https://github.com/your-username/CS-175-Project.git
cd CS-175-Project
```

2. **Create and activate a virtual environment** (recommended)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

---

## Git Ignore

Make sure the `.gitignore` file contains:
```
# Python virtual environment
venv/

# Byte-compiled / cache files
__pycache__/
*.pyc
*.pyo
*.pyd

# Jupyter notebook checkpoints (if any)
.ipynb_checkpoints/

# PyTorch cache (optional)
*.pt
```

> Do **not** commit installed packages; collaborators can install them via `requirements.txt`.

---

## Collaboration Workflow

1. **Clone the repo**
```powershell
git clone https://github.com/your-username/LeGoat.git
cd LeGoat
```

2. **Create your own branch** (recommended for features/bugfixes)
```powershell
git checkout -b feature/your-feature-name
```

3. **Make changes, stage, and commit**
```powershell
git add .
git commit -m "Add feature XYZ"
```

4. **Push your branch and create a Pull Request**
```powershell
git push origin feature/your-feature-name
```
- Open a Pull Request on GitHub for review before merging to `main`.

5. **Keep your branch updated**
```powershell
git fetch origin
git merge origin/main
```

---

## Adding Collaborators

1. Go to **Settings → Manage Access** in the GitHub repo  
2. Click **Invite a collaborator**  
3. Enter the collaborator’s GitHub username or email  
4. Once they accept, they can clone, push, and create branches

---

## Notes

- Always work inside a **virtual environment** to avoid dependency conflicts  
- Use branches and pull requests for collaborative development  
- Keep `requirements.txt` updated when adding new dependencies
