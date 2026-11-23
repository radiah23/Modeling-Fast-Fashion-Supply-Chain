"""
Turn the CEPII BACI download into the edge files for our network.

Keeps only clothing (HS chapter 61 = knitted, 62 = woven), our top 5 producers
(China, Bangladesh, Vietnam, Turkey, India) and 2 markets (EU = 27 member states added together, USA).

Usage (laptop or Colab):
    python baci_to_edges.py BACI_HS92_V202601.zip            # every year in the zip
    python baci_to_edges.py BACI_HS92_V202601.zip 2024       # one year only

Output (written next to the script, in fast_fashion_dataset/):
    edges_baci_all_years.csv   producer, consumer, year, value_usd_bn, tonnes
    edges_baci.csv             same, latest year only (drop-in for edges_estimated.csv)
"""
import sys, os, re, zipfile
import pandas as pd

PRODUCERS = ["CHN", "BGD", "VNM", "TUR", "IND"]          # top 5 clothing exporters (WTO 2024)
EU27 = ["AUT", "BEL", "BGR", "HRV", "CYP", "CZE", "DNK", "EST", "FIN", "FRA", "DEU", "GRC", "HUN",
        "IRL", "ITA", "LVA", "LTU", "LUX", "MLT", "NLD", "POL", "PRT", "ROU", "SVK", "SVN", "ESP", "SWE"]
MARKETS = {**{c: "EU" for c in EU27}, "USA": "USA"}      # EU (27 countries added together) and USA

def country_map(z):
    """BACI uses numeric country codes; the country_codes file maps them to ISO3."""
    name = next(n for n in z.namelist() if "country_codes" in n.lower())
    cc = pd.read_csv(z.open(name), dtype=str)
    code_col = next(c for c in cc.columns if c.lower() in ("country_code", "i", "code"))
    iso_col = next(c for c in cc.columns if "iso3" in c.lower() or "iso_3" in c.lower())
    return dict(zip(cc[code_col].astype(int), cc[iso_col].str.upper()))

def main(path, only_year=None):
    out = []
    with zipfile.ZipFile(path) as z:
        code2iso = country_map(z)
        exp_codes = {k for k, v in code2iso.items() if v in PRODUCERS}
        imp_codes = {k for k, v in code2iso.items() if v in MARKETS}
        files = sorted(n for n in z.namelist() if re.search(r"BACI_HS\d+_Y\d{4}_V", n))
        if only_year:
            files = [n for n in files if f"_Y{only_year}_" in n]
        for name in files:
            year = int(re.search(r"_Y(\d{4})_", name).group(1))
            print("reading", name)
            # read in chunks: one year is several million rows
            for chunk in pd.read_csv(z.open(name), dtype={"k": str}, chunksize=2_000_000):
                chunk["k"] = chunk["k"].str.zfill(6)        # keep leading zeros of HS codes
                keep = (chunk.k.str[:2].isin(["61", "62"])
                        & chunk.i.isin(exp_codes) & chunk.j.isin(imp_codes))
                c = chunk[keep]
                if len(c):
                    out.append(pd.DataFrame({"year": year,
                                             "producer": c.i.map(code2iso),
                                             "consumer": c.j.map(code2iso).map(MARKETS),
                                             "v": c.v, "q": pd.to_numeric(c.q, errors="coerce")}))
    df = pd.concat(out)
    edges = (df.groupby(["producer", "consumer", "year"], as_index=False)
               .agg(value_usd_bn=("v", lambda s: s.sum() / 1e6),   # v is in thousand USD
                    tonnes=("q", "sum")))
    os.makedirs("fast_fashion_dataset", exist_ok=True)
    edges.to_csv("fast_fashion_dataset/edges_baci_all_years.csv", index=False)
    last = edges[edges.year == edges.year.max()].drop(columns="year")
    last["source"] = f"BACI {os.path.basename(path)}, HS 61+62, year {edges.year.max()}"
    last.to_csv("fast_fashion_dataset/edges_baci.csv", index=False)
    print(f"\n{len(edges)} rows, years {edges.year.min()}-{edges.year.max()}")
    print("Exports to the EU and USA, latest year (USD bn):")
    print(last.groupby("producer").value_usd_bn.sum().sort_values(ascending=False).round(2).to_string())

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
