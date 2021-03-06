from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal

import click
import pandas as pd
from sklearn.datasets import load_boston

import sys
sys.path.append("..")

from scripts import loads, cleans, feats, analyze, modeling, custom


HOME = Path(__file__).parent

@dataclass
class BaseConfig:
    #: 目的変数(1つのみ)
    target_name: str
    target_type: Literal['numerical', 'categorical']
    #: カテゴリ変数
    categorical_cols: List[str]
    #: データクレンジングで落とす列
    drop_cols: List[str]
    #: 最終モデル構築に使う列
    use_cols: List[str]
    datadir: Path = HOME / "data"
    outdir: Path = HOME / "result"
    suffix: str = "csv" #or "hdf"

    #: boruta
    p: float = 95.0


SELECTED_COLS = []

config = BaseConfig(
    target_name = "species",
    target_type = "categorical",
    categorical_cols = ["species", "island", "sex"],
    #target_name="bill_length_mm",
    #target_type = "numerical",
    drop_cols = [],
    use_cols= SELECTED_COLS,
    )


@click.group()
def cli():
    pass


@cli.command()
@click.option("--out_file", "-o", default="raw.csv", type=str)
@click.option("--sample", is_flag=True)
def load(out_file, sample):
    """ 生tableを取得する

    Args:
        out (Path): path to output dataset
        sample (bool): load sample dataset boston housing
    """
    out_path = config.datadir / "raw" / out_file
    loads.load(out_path, sample)


@cli.command()
@click.option("--input_file", "-i", default="raw.csv", type=str)
@click.option("--out_file", "-o", default="clean.csv", type=str)
def clean(input_file, out_file):
    """ 最低限のデータクレンジングを行う
        - 型異常への対処
        - テーブルの結合  など
    """
    input_path = config.datadir / "raw" / input_file
    out_path = config.datadir / "clean" / out_file
    cleans.clean(input_path, out_path)


@cli.command()
@click.option("--input_file", "-i", default="clean.csv", type=str)
def feat(input_file):
    """ 特徴量の追加
        - 不要な行の削除
        - ラベル無し列の削除
        - 多項式特徴量の追加
        - 特徴量の追加  など
    """
    input_path = config.datadir / "clean" / input_file
    out_dir = config.datadir / "processed"
    feats.feat(input_path, out_dir, config)


@cli.command()
@click.option("--filename", "-f", type=str, required=True)
@click.option("--profile", is_flag=True)
@click.option("--boruta", is_flag=True)
@click.option("--ga", is_flag=True)
@click.option("--xai", is_flag=True)
@click.option("--cluster", is_flag=True)
@click.option("--run_all", is_flag=True)
def eda(filename, profile, boruta, ga, xai, cluster, run_all):
    """
       この時点で特徴量数が多すぎるなら変数選択だけして(feature_selection)
       次iterにいったほうがよい
    """

    file_path = config.datadir / "processed" / filename
    assert file_path.exists()

    out_dir = config.outdir / file_path.stem
    if not out_dir.exists():
        out_dir.mkdir()

    if profile or run_all:
        analyze.profile(file_path, out_dir, config)

    if boruta or run_all:
        analyze.select_by_boruta(file_path, out_dir, config=config)

    if ga or run_all:
        analyze.select_by_ga(file_path, out_dir, config=config)

    if cluster or run_all:
        pass
        #analyze.cluster(file_path, out_dir, config)


@cli.command()
@click.option("--filename", "-f", type=str, required=True)
def preprocess(filename, dataset, modeling):j
    """ X.csvとy.csvを作成
    """

    file_path = config.datadir / "processed" / filename
    assert file_path.exists()

    outdir = config.datadir / "product"
    modeling.preprocess(filepath, outdir, config)


@cli.command()
@click.option("--filename", "-f", type=str, required=True)
def model(filename, dataset, modeling):j

    outdir = config.outdir / "model"
    if not outdir.exists():
        outdir.mkdir()

    modeling.train_model()


@cli.command()
def custom():
    custom.main()


if __name__ == "__main__":
    cli()
