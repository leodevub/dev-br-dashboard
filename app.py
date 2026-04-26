import pandas as pd

df = pd.read_csv("survey_results_public.csv", low_memory=False)

brasil = df[df["Country"] == "Brazil"]
print(f"Respostas do Brasil: {len(brasil)}")

# Separar as linguagens e contar cada uma individualmente
linguagens = brasil["LanguageHaveWorkedWith"].dropna().str.split(";").explode()
print("\nTop 10 linguagens mais usadas no Brasil:")
print(linguagens.value_counts().head(10))

# Salário médio por linguagem no Brasil
brasil_salario = brasil[brasil["ConvertedCompYearly"].notna()]

# Pega só quem tem salário preenchido
print(f"Brasileiros com salário informado: {len(brasil_salario)}")

# Salário médio geral
print(f"Salário médio anual: US$ {brasil_salario['ConvertedCompYearly'].mean():,.0f}")
print(f"Salário mediano anual: US$ {brasil_salario['ConvertedCompYearly'].median():,.0f}")

# Salário por anos de experiência
salario_exp = brasil_salario.groupby("WorkExp")["ConvertedCompYearly"].median().sort_values(ascending=False)
print("\nSalário mediano por anos de experiência:")
print(salario_exp.head(10))