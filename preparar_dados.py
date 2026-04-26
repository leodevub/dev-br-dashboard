import pandas as pd

df = pd.read_csv("survey_results_public.csv", low_memory=False)

colunas = [
    "Country", "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
    "ConvertedCompYearly", "WorkExp", "RemoteWork", "AISelect"
]
df_pequeno = df[colunas]
brasil_pequeno = df_pequeno[df_pequeno["Country"] == "Brazil"]
brasil_pequeno.to_csv("brasil_devs.csv", index=False)
print(f"Tamanho: {brasil_pequeno.shape}")