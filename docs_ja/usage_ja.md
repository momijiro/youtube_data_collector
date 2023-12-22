# 主な機能
本ライブラリで収集できるのは、大きく以下の3つです。
1. [動画のメタデータ](#1-動画のメタデータの収集) : タイトル、概要など (`mode='movie'`)
2. [動画のコメント](#2-動画のコメントの収集) (`mode='comment'`)
3. [動画の統計データ](#3-動画の統計データの収集) :高評価数、視聴数など (`mode='stats'`)

## 全機能での共通点
どのデータを収集する際も、基本形は同じです。(実行する際には、先にQuick Startを御覧ください。)
``` Python
collector = YouTubeDataCollector(
    api_key=YOUTUBE_API_KEY, # 共通
    mode='movie', # 'movie', 'comment', 'stats'のいずれかを指定
    save = True, # True or False
    args={}, # modeによって異なる
    file_name = None, # 指定しない場合は自動で設定
    output_path = 'output' # 指定しない場合は自動で設定
)
collector.run()
df = collector.df
```
引数は以下です。
- 指定必須
    - `mode`によらず共通
        - `api_key` : 自分のAPIキーを入力
        - `save` : 収集データを保存するかどうか
    - `mode`により異なる
        - `mode` : `'movie'`, `'comment'`, `'stats'`のいずれかを指定
        - `args` : `mode`により異なる引数
- 指定しなくても良い
    - `file_name` : 保存するファイルの名前 (複数回実行する場合は、上書きされないように指定する)
    - `output_path` : 出力するフォルダ (指定しない場合、自動で`output`フォルダを作成)

引数以外にも、`mode`による相違点として以下の2つがあります。
- コメント・統計データを収集する場合は、先に動画のメタデータを収集する必要がある
- 保存のされ方

次の章からは、3種類の`mode`それぞれについて詳しく説明します。

## 1. 動画のメタデータの収集
動画のメタデータの収集には、`mode='movie'`を指定します。
``` Python
collector = YouTubeDataCollector(
    api_key=YOUTUBE_API_KEY,
    mode='movie',
    save=True,
    args = {
        'start': '2008-01',
        'end': '2008-01',
        'query': 'あけましておめでとう',
        # 'channel_id': 'specify_channel_id',
    }
)
collector.run()
df_movie = collector.df
df_movie
```

argsの中身として以下の4つがあるので、詳しく説明します。
- 必須
    - `start` : 取得する動画の開始日時
    - `end` : 取得する動画の終了日時
- 少なくとも1つ必要
    - `query` : 検索クエリ
    - `channel_id` : チャンネルID

### start / end
まず、取得する動画の開始日時と終了日時を指定する必要があります。ただし、`start`と`end`で単位が同じなら、年・月・日のどれを指定しても取得可能で、その単位ごとにデータが保存されます。

(例) 2010年から2012年のデータを収集したい場合
|`start` |`end`|保存名の例|
|---|---|---|
|`'2010'`|`'2010'`|`キーワード_2010_2012.csv`|
|`'2010-01'`  |`'2010-12'`|`キーワード_2010-01_2012-12.csv`|
|`'2010-01-01'`  |`'2010-12-31'`|`キーワード_2010-01-01_2012-12-31.csv`|


上記の3パターンはどれも結果としては(原理上)同じになります。なので長期間のデータを収集する場合は、API効率の観点からなるべく大きい単位 (年・月) を使用してください。 (詳しくは`note.md`をご覧ください)

### query / channel_id
次に、`query`・`channel`を指定します。`args`内で、少なくとも一方を指定するようにしてください。

1. `query`

    キーワード(`query`)は自由に設定可能で、複数羅列する場合は半角スペースで区切ります。Twitter API等と同様に、以下のように`AND`や`OR`を用いて検索することもできます。
    ```
    'query': '(今日 OR 明日) AND (晴れ OR 雨)'
    ```
    この例では、「今日・晴れ」を含む動画、「今日・雨」を含む動画、「明日・晴れ」を含む動画、「明日・雨」を含む動画が収集されます。

2. `channel_id`

    また、その動画を作成したチャンネル名で取得したい場合もあると思うので、`channel_id`でも指定できるようにしてあります。

    ただし、`'channel_id'`は、`'ChannelTitle'`や「@」で始まるものではなく、そのチャンネルに固有のランダムな英数字です。 [こちらの方の記事](https://ilr.jp/tech/485/)を使わせていただくと、チャンネルURLを入力することで取得できます。

### save
`movie`モードでは、以下のようなデータが出力されます。 (※本ドキュメントのデータは全て架空のデータです)

| video_id   | title   | description   | publish_time   | channel_title   |
|------------|---------|-------------|------------|----------------|
|ab12cd|あけましておめでとう動画|日の出の動画です|2008-01-01T01:23:45Z|Helloworld|
|zy34xw|新年あけましておめでとう|ハッピーニューイヤー！|2008-01-01T23:45:00Z|Dummies|

また、デフォルトは以下のように自動で`output/movie`を作成し保存します。
- `output/movie/あけましておめでとう_2008-01_2008-01.csv`

## 2. 動画のコメントの収集
コメント・統計データを収集する場合は、先に動画のメタデータを収集し、そのデータから`video_id_list`を作成する必要があります。
```
video_id_list = pickup_video_id(df_movie)
```
この`video_id_list`を用いて、`mode='comment'`としてコメントを収集します。
```
collector = YouTubeDataCollector(
        api_key=YOUTUBE_API_KEY,
        mode='comment',
        save=True,
        args={'video_id_list': video_id_list}
)
collector.run()
df_comment = collector.df
df_comment
```
argsに指定するのは `video_id_list`(動画IDのリスト、必須) のみです。

ちなみに収集途中でAPIが落ちた場合、収集時の最後の`video_id`を元に、以下のように`video_id_list`を更新し、続きから収集することができます。

```
last_id = 'LastSavedVideoId'
video_id_list = update_list(video_id_list, last_id)
```

### save
コメントモードでは以下のようなデータを取得できます。

| video_id | comment  |like_count | publish_time  |author_id|
|---|---|---|---|---|
|ab12cd|めでたいなぁ  |5 | 2008-01-02T10:20:30Z |AAAAAAAAAabbbbbbbCC||
|ab12cd|今年もよろしく|2|2013-01-23T12:34:56Z |DDDDDDDeeeeeeeeffffGG||

また、デフォルトは以下のように自動で`output/comment`を作成し保存します。(最後の`video_id`を使用)
- `output/comment/comment_ab12cd.csv`

## 3. 動画の統計データの収集
コメントと同様に、`video_id_list`を作成してから実行します。
```
collector = YouTubeDataCollector(
        api_key=YOUTUBE_API_KEY,
        mode='stats',
        save=True,
        args={'video_id_list': video_id_list}
)
collector.run()
df_stats = collector.df
df_stats
```
こちらもargsに指定するのは `video_id_list`(動画IDのリスト、必須) のみです。

### save
統計データモードでは以下のようなデータを取得できます。

|video_id  |View_count  |like_count  | comment_count|
|---|---|---|---|
|ab12cd|33333 |3|1|
|zy34xw|4321 |1|0|

また、デフォルトは以下のように自動で`output/stats`を作成し保存します。
- `output/stats/stats.csv`
