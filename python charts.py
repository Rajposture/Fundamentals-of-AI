import pandas as pd
import matplotlib.pyplot as plt
 
df = pd.read_csv("Housing.csv")
 
# 7. Heatmap - correlation between numeric columns
numeric_df = df.select_dtypes(include="number")
corr = numeric_df.corr()
 
plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar()
plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
plt.yticks(range(len(corr.columns)), corr.columns)
plt.title("Correlation Heatmap")
 
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        plt.text(j, i, round(corr.iloc[i, j], 2), ha="center", va="center", fontsize=8)
 
plt.tight_layout()
plt.savefig("7_heatmap.png")
plt.close()
