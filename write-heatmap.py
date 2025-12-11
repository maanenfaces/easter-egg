import os
import subprocess
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# ---------------- CONFIGURATION ----------------
TEXT = "MAANEN FACES"
FONT_SIZE = 12  # Taille de la font pour la matrice
COMMITS_PER_SQUARE = 5  # Plus = carré plus foncé
YEAR = 2025  # Année des commits
BRANCH = "main"  # Branche pour les commits
REPO_PATH = "."  # Chemin vers ton repo git
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"  # Font monospace


# ------------------------------------------------

def text_to_matrix(text, font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text)
    width = bbox[2] - bbox[0]  # droite - gauche
    height = bbox[3] - bbox[1]  # bas - haut
    img = Image.new("1", (width, height), 1)  # 1 = blanc
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, font=font, fill=0)  # 0 = noir
    # Redimensionner pour s'adapter à un maximum de 52x7
    img = img.resize((52, 7), Image.NEAREST)
    return np.array(img)


def generate_commit_dates(matrix, year):
    # Commence à partir du dimanche le plus proche du 1er janvier
    start = datetime(year, 1, 1)
    while start.weekday() != 6:  # 6 = dimanche
        start -= timedelta(days=1)

    # Centrer verticalement et horizontalement
    offset_y = (7 - matrix.shape[0]) // 2
    offset_x = (52 - matrix.shape[1]) // 2

    dates = []
    for x in range(matrix.shape[1]):  # colonnes = semaines
        for y in range(matrix.shape[0]):  # lignes = jours
            if matrix[y, x] == 0:
                day = start + timedelta(weeks=x + offset_x, days=y + offset_y)
                # S'assurer que la date est dans l'année
                if datetime(year, 1, 1) <= day <= datetime(year, 12, 31):
                    dates.append(day)
    return dates


def make_commits(dates, commits_per_square, repo_path, branch):
    os.chdir(repo_path)
    subprocess.run(["git", "checkout", branch])
    for date in dates:
        for _ in range(commits_per_square):
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = date.isoformat()
            env["GIT_COMMITTER_DATE"] = date.isoformat()
            subprocess.run(
                ["git", "commit", "--allow-empty", "-m", f"Commit for {TEXT}"],
                env=env)


def main():
    matrix = text_to_matrix(TEXT, FONT_PATH, FONT_SIZE)
    dates = generate_commit_dates(matrix, YEAR)
    print(
        f"Generating {len(dates) * COMMITS_PER_SQUARE} commits for year {YEAR}...")
    make_commits(dates, COMMITS_PER_SQUARE, REPO_PATH, BRANCH)
    print("Done! Push your changes with `git push`.")


if __name__ == "__main__":
    main()
