import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def read_data(path: Path, sep: str | None = "auto") -> pd.DataFrame:
    if sep in (None, "auto"):
        df = pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")
    else:
        df = pd.read_csv(path, sep=sep, encoding="utf-8-sig")
    expected = ["Область", "Місто/Район", "Значення"]
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}. Found: {list(df.columns)}")
    df["Значення"] = pd.to_numeric(df["Значення"], errors="coerce")
    return df.dropna(subset=["Значення"])

def plot_bar(df: pd.DataFrame, title: str, out_path: Path, horizontal: bool = False):
    df = df.sort_values("Значення", ascending=False)
    plt.figure(figsize=(12, 6))
    if horizontal:
        plt.barh(df["Місто/Район"], df["Значення"])
        plt.xlabel("Значення"); plt.ylabel("Місто/Район"); plt.gca().invert_yaxis()
    else:
        plt.bar(df["Місто/Район"], df["Значення"])
        plt.xlabel("Місто/Район"); plt.ylabel("Значення"); plt.xticks(rotation=45, ha="right")
    plt.title(title); plt.tight_layout(); plt.savefig(out_path, dpi=150); plt.show()

def main():
    p = argparse.ArgumentParser(description="CSV/TSV → Bar chart (Область/Місто/Район/Значення)")
    p.add_argument("--csv", default="input_data.csv")
    p.add_argument("--sep", default="auto")  # auto | \t | , | ;
    p.add_argument("--region", default=None)
    p.add_argument("--top", type=int, default=20)
    p.add_argument("--horizontal", action="store_true")
    p.add_argument("--output", default="charts/bar_chart.png")
    a = p.parse_args()

    src = Path(a.csv);  src.exists() or (_ for _ in ()).throw(FileNotFoundError(src))
    df = read_data(src, sep=None if a.sep=="auto" else a.sep)
    if a.region:
        df = df[df["Область"].astype(str).str.strip() == a.region.strip()]
        if df.empty: raise SystemExit(f"No data for region '{a.region}'.")
    if a.top and a.top < len(df): df = df.head(a.top)
    Path("charts").mkdir(exist_ok=True)
    title = f"Top {len(df)} — {a.region or 'All Regions'}"
    plot_bar(df, title, Path(a.output), horizontal=a.horizontal)

if __name__ == "__main__":
    main()
