
# Youtube Data Collector

This library utilizes the [YouTube API v3](https://developers.google.com/youtube/v3/docs) to allow for easy collection of "video metadata, comments, and statistical data." Depending on your purpose, please refer to the following pages:
- For those who want to try it out right away -> See "Quick Start" below
- For those who want to know about the main features (collecting videos, comments, and statistics) -> `docs_en/usage.md`
- For practical use (explanations about API and quota) -> `docs_en/note.md`
- For those who want to read an article explaining the whole thing -> [Qiita article]

### Quick Start

Here are the steps to quickly start collecting YouTube data:
1. Install the library
   ```python
   # Import the library
   !git clone https://github.com/momijiro/youtube_data_collector
   # Change directory (assuming execution in a notebook)
   %cd youtube_data_collector
   # Install related libraries
   !pip install -r requirements.txt
   ```
2. Obtain a YouTube API key from the [Google Cloud Console](https://console.cloud.google.com/) (for details, see the article)

3. Replace `YOUTUBE_API_KEY` with your own API key and run the following code
   ``` Python
   # Import the library
   from ytdc import YouTubeDataCollector, pickup_video_id, update_list

   # Execute
   YOUTUBE_API_KEY = 'YOUR_API_KEY'  # Replace with your own API key
   collector = YouTubeDataCollector(
      api_key=YOUTUBE_API_KEY,
      mode='movie',
      save=False,
      args = {
         'start': '2008-01',
         'end': '2008-01',
         'query': 'Happy New Year',
      }
   )
   collector.run()
   df_movie = collector.df
   df_movie
   ```
4. You can collect video data from January 2008 that includes "Happy New Year" like the following:

   | video_id   | title   | description   | publish_time   | channel_title   |
   |------------|---------|-------------|------------|----------------|
   |ab12cd|Happy New Year Video|A video of the sunrise|2008-01-01T01:23:45Z|Helloworld|
   |zy34xw|New Year's Greetings|Happy New Year!|2008-01-01T23:45:00Z|Dummies|

      ※Note: The year 2008 is used to avoid consuming too much quota. (For details, see: `docs_en/note.md`)


### Wrap up
For other details on how to use it, please see the docs/article. Also, if you find any errors, questions, or unclear points, please contact us at [X(Twitter)](https://twitter.com/kanure24).

Thank you again for taking a look at this code. I would be happy if you could give me a star if you liked it!

# Youtube Data Collector (日本語版)

本ライブラリは、[YouTube API v3](https://developers.google.com/youtube/v3/docs?hl=ja)を活用し、「動画のメタデータ・コメント・統計データ」を簡単に収集できるように実装したものです。目的に応じて、以下のページをご覧ください。
- とりあえず使ってみたい方 -> 以下の「Quick Start」
- 主な機能 (動画・コメント・統計の収集)を知りたい方 -> `docs_ja/usage.md`
- 実用に向けて (APIやquotaに関する説明) -> `docs_ja/note.md`
- 全体を説明した記事が読みたい方 -> [Qiita記事]

### Quick Start

最短でYouTubeデータの収集までを実行できる手順を説明します。
1. ライブラリをインストール
   ```python
   # 本ライブラリをインポート
   !git clone https://github.com/momijiro/youtube_data_collector
   # ディレクトリを変更 (notebookでの実行を想定)
   %cd youtube_data_collector
   # 関係するライブラリをインストール
   !pip install -r requirements.txt
   ```
1. [Google Cloud Console](https://console.cloud.google.com/)で、YouTube APIキーを取得 (詳しくは記事をご覧ください)

2. `YOUTUBE_API_KEY`を自分の取得したAPIキーに修正し、下記のコードを実行
   ``` Python
   # ライブラリをインポート
   from ytdc import YouTubeDataCollector, pickup_video_id, update_list

   # 実行
   YOUTUBE_API_KEY = 'YOUR_API_KEY'  # 自分の API キーに置き換えてください
   collector = YouTubeDataCollector(
      api_key=YOUTUBE_API_KEY,
      mode='movie',
      save=False,
      args = {
         'start': '2008-01',
         'end': '2008-01',
         'query': 'あけましておめでとう',
      }
   )
   collector.run()
   df_movie = collector.df
   df_movie
   ```
4. 以下のような「あけましておめでとう」を含む2008年1月の動画データが収集できます。

   | video_id   | title   | description   | publish_time   | channel_title   |
   |------------|---------|-------------|------------|----------------|
   |ab12cd|あけましておめでとう動画|日の出の動画です|2008-01-01T01:23:45Z|Helloworld|
   |zy34xw|新年あけましておめでとう|ハッピーニューイヤー！|2008-01-01T23:45:00Z|Dummies|

      ※ちなみに、quota を消費しすぎないように2008年としています。(詳しくは: `docs_ja/note.md`)


### 最後に
その他の詳しい使い方はdocs・記事をご覧ください。また、間違い・疑問点・不明点等ありましたら、[X(Twitter)](https://twitter.com/kanure24)までご連絡いただけると幸いです。

改めて、本コードをご覧いただき、ありがとうございます。良かったらStarをいただけると嬉しいです！