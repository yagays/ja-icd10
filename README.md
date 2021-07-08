# ja-ICD10


## 使い方
まず、ICDクラスのインスタンスを作成します。

```python
icd = ICD()
```

### ICD-10のカテゴリー情報を取得する
ICD-10のカテゴリー名から情報を取得します。ICD-10のカテゴリー表記は、`A000`,`A00.0`どちらも可能です。

```python
In []: print(icd["A000"])
<ICD Category:[A00.0] コレラ菌によるコレラ>

In []: icd["A000"].name
Out[]: 'コレラ菌によるコレラ'

In []: icd["A000"].code
Out[]: 'A00.0'
```

また、登録されているカテゴリーの中分類であれば、範囲指定も可能です。

```python
In []: icd["A00-A09"]
Out[]: <ICD Category:[A00-A09] 腸管感染症>

In []: icd["A00-A09"].is_block
Out[]: True

In []: icd["A00-B99"]
Out[]: <ICD Category:[A00-B99] 感染症及び寄生虫症>

In []: icd["A00-B99"].is_chapter
Out[]: True
```

### 名称からICD-10カテゴリーを探す
索引を元にカテゴリーを検索します。

```python
In []: icd.find_categories_by_name("頭痛")
Out[]: [<ICD Category:[R51] 頭痛>]

In []: icd.find_categories_by_name("吐き気")
Out[]: [<ICD Category:[R11] 悪心及び嘔吐>]
```

`partial_match=True`を指定することで、すべてのカテゴリー名からの部分検索ができます。

```python
In []: icd.find_categories_by_name("頭痛", partial_match=True)
Out[]:
[<ICD Category:[G43] 片頭痛>,
 <ICD Category:[G43.0] 前兆＜アウラ＞を伴わない片頭痛［普通型片頭痛］>,
 <ICD Category:[G43.1] 前兆＜アウラ＞を伴う片頭痛［古典型片頭痛］>,
 <ICD Category:[G43.2] 片頭痛発作重積状態>,
 <ICD Category:[G43.3] 合併症を伴う片頭痛>,
 <ICD Category:[G43.8] その他の片頭痛>,
 <ICD Category:[G43.9] 片頭痛，詳細不明>,
 <ICD Category:[G44] その他の頭痛症候群>,
 <ICD Category:[G44.0] 群発頭痛症候群>,
 <ICD Category:[G44.1] 血管性頭痛，他に分類されないもの>,
 <ICD Category:[G44.2] 緊張性頭痛>,
 <ICD Category:[G44.3] 慢性外傷後頭痛>,
 <ICD Category:[G44.4] 薬物誘発性頭痛，他に分類されないもの>,
 <ICD Category:[G44.8] その他の明示された頭痛症候群>,
 <ICD Category:[O29.4] 妊娠中の脊髄又は硬膜外麻酔誘発性頭痛>,
 <ICD Category:[O74.5] 分娩における脊髄麻酔及び硬膜外麻酔誘発性頭痛>,
 <ICD Category:[O89.4] 産じょく＜褥＞における脊髄麻酔及び硬膜外麻酔誘発性頭痛>,
 <ICD Category:[R51] 頭痛>]
```

### 傷病情報を取得する
病名管理番号から傷病名を検索します。

```python
In []: icd.get_disease_by_byomei_id("20088330").name
Out[]: '外傷性横隔膜ヘルニア・胸腔に達する開放創合併あり'

In []: icd.get_disease_by_byomei_id("20088330").code
Out[]: 'S2781'

In []: icd.get_disease_by_byomei_id("20088330").name_kana
Out[]: 'ガイショウセイオウカクマクヘルニア・キョウクウニタッスルカイホウソウガッペイアリ'

In []: icd.get_disease_by_byomei_id("20088330").name_abbrev
Out[]: '外傷性横隔膜ヘルニア・胸腔開放創あり'
```


### カテゴリーの下の階層の傷病を取得する
指定したICD-10のカテゴリーの階層下にある傷病をすべて取得します。


```python
In []: print(icd.get_diseases_by_code("A000"))
[<Disease:[A00.0][20050788] アジアコレラ>,
<Disease:[A00.0][20065915] 真性コレラ>]

In []: print(icd.get_diseases_by_code("A00"))
[<Disease:[A00.0][20050788] アジアコレラ>,
 <Disease:[A00.0][20065915] 真性コレラ>,
 <Disease:[A00.1][20051356] エルトールコレラ>,
 <Disease:[A00.9][20051879] コレラ>,
 <Disease:[A00.9][20058027] 偽性コレラ>]
```

### カテゴリー以下の階層のカテゴリーと傷病を取得する
指定したICD-10のカテゴリーの階層下にあるカテゴリーと傷病をすべて取得します。

```python
In []: icd.get_diseases_and_categories_by_code("A000")
Out[]:
[<ICD Category:[A00.0] コレラ菌によるコレラ>,
 <Disease:[A00.0][20050788] アジアコレラ>,
 <Disease:[A00.0][20065915] 真性コレラ>]

In []: icd.get_diseases_and_categories_by_code("A00")
Out[]:
[<ICD Category:[A00] コレラ>,
 <ICD Category:[A00.0] コレラ菌によるコレラ>,
 <Disease:[A00.0][20050788] アジアコレラ>,
 <Disease:[A00.0][20065915] 真性コレラ>,
 <ICD Category:[A00.1] エルトールコレラ菌によるコレラ>,
 <Disease:[A00.1][20051356] エルトールコレラ>,
 <ICD Category:[A00.9] コレラ，詳細不明>,
 <Disease:[A00.9][20051879] コレラ>,
 <Disease:[A00.9][20058027] 偽性コレラ>] 
```

