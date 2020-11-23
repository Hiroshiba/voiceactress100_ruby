# 読み仮名（ルビ）つき声優統計コーパス音素バランス文

## index.html作成方法
```bash
python ruby.py
```

その後、ミスを手で修正し、`valid.py`を実行して再確認。

## ファイル説明
* ruby.py: 読み仮名を付けるためのコード
* transcript_utf8.txt: [JSUT](https://sites.google.com/site/shinnosuketakamichi/publication/jsut)内の[声優統計コーパス](https://voice-statistics.github.io/)音素バランス文のテキスト
* voiceactoress100_spaced.txt: [jvs_hiho](https://github.com/Hiroshiba/jvs_hiho)内のテキスト
