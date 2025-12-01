python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
python app.py

git status
git add .
git commit -m "quick commit"
git push