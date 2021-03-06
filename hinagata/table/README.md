
## ひな形：テーブルデータ分析

- ReadableでReproduceableなモデル開発Biolerplate

- MentenaceableではなくMLOpsではない

<br>

1. 最低限のクレンジング
2. プロファイリングとGBT系での簡易モデル化によって重要特徴を絞り込む
3. 変数削減した後に、Poly, Categorical Encodingなどで変数を追加
4. 2へ戻る, このときプロジェクトを複製する(manage.py restartproject projname)




## Best practice

- 目的変数ごとにディレクトリを分ける

- 1iterごとにディレクトリを分ける

  つまり複数回同じコマンドを使うことを想定していない

No U Turn!


## How to use

```
#!/bin/bash

NAME="Version1"

# 1. load raw dataset
poetry run python command.py load -o "${NAME}.csv"

# 2. Minimum data cleansing
poetry run python command.py clean -i "${NAME}.csv" -o "${NAME}.csv"


# 3. Create Features
poetry run python command.py feat -i "${NAME}.csv"

# 4.  Run analysis
poetry run python command.py eda -i "filename.csv" --run_all

```


## Links

pandas_bokeh:<br>
https://github.com/PatrikHlobil/Pandas-Bokeh


## ToDO
install failed on windows:

- dtale
- dtreeviz / graphviz
