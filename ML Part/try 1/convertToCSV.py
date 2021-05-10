import pandas as pd 
df = pd.read_json("my-new-file.json")
t="index"
t+=df.to_csv()
f = open("dataset.csv", "w")
f.write(t)
f.close()
