from apiclient.discovery import build
import pandas as pd
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm
from pathlib import Path

######################## utils ########################
def pickup_video_id(df):
    """video_idのみのデータを作成"""
    video_id_list = df['video_id'].unique().tolist()
    print('video_id:', len(video_id_list))
    return video_id_list

def update_list(list_, las):
    """リストからx以前を削除"""
    print('before:', len(list_))
    while True:
        if x == list_[0]:
            list_.pop(0)
            break
        else:
            list_.pop(0)
    print('after:', len(list_))
    return list_

######################## collector ########################
class YouTubeDataCollector:
    """
    YouTube Data API v3を用いて、検索クエリにマッチする動画の情報を取得する

    Args:

        api_key (str): 自分のAPIキーを入力
        mode (str): 動画、コメントなどのモードを指定 (e.g., 'movie', 'comment', 'stats')
        save (bool): データを保存するかどうか
        args (dict): それぞれのモードに合わせて指定する引数を辞書形式で
        file_name (str): 保存するファイル名
        output_path (str): データを保存するパス

    Returns:

        df (pd.DataFrame): 取得した動画の情報をまとめたDataFrame

    """
    def __init__(self, api_key, mode, save, args, file_name=None, output_path='output'):
        self.api_key = api_key
        self.mode = mode
        self.save = save
        self.args = args
        self.file_name = file_name
        self.output_path = Path(output_path)
        self.service = build('youtube', 'v3', developerKey=api_key)

    ######################## common ########################
    def get_responses(self, params):
        """ 検索クエリにマッチするresponseを取得 """
        return self.youtube.list(**params).execute()

    def unit_request(self, f_params, f_extract):
        """ 1回のリクエストで実行 """
        all_items = []
        count = 0
        params = f_params()
        while True:
            response = self.get_responses(params)
            all_items.extend(f_extract(response))
            count += 1
            next_token = response.get('nextPageToken')
            if not next_token:
                break
            else:
                params['pageToken'] = next_token

        print(f"response_count: {count}")
        return all_items

    def data_to_df(self, data, cols, drop_dup):
        """ データをDataFrameに変換 """
        if len(data) > 0:
            self.df = pd.DataFrame(data, columns=cols)
            if drop_dup:
                self.df = self.df.drop_duplicates(subset='video_id').reset_index(drop=True)
            return True
        else:
            print("No data.")
            return False

    def get_file_name(self, prefix, suffix):
        if self.file_name is None:
            self.file_name = prefix
        return f"{self.file_name}_{suffix}.csv"

    def save_data(self, df, file_name):
        """ データを保存 """
        if self.save:
            save_path = Path(self.output_path) / self.mode
            os.makedirs(save_path, exist_ok=True)
            df.to_csv(save_path / file_name, index=False)
            print(f"Saved at: {save_path / file_name}, shape: {df.shape}")

    ######################## movie ########################
    def get_start_list(self, start, end):
        """ start, end から delta_list を生成 """
        date_formats = {
            4: ('%Y', 'year'),
            7: ('%Y-%m', 'month'),
            10: ('%Y-%m-%d', 'day')
        }

        # start, end のフォーマットを確認
        if len(start) != len(end) or len(start) not in date_formats:
            raise ValueError('Invalid date format for start or end.')

        # 単位を取得
        fmt, self.unit = date_formats[len(start)]
        self.delta = relativedelta(**{self.unit + 's': 1})

        # start, end -> datetime
        start_date = datetime.strptime(start, fmt)
        end_date = datetime.strptime(end, fmt) + self.delta - timedelta(days=1)

        # 日付リストを生成
        self.start_list = []
        while start_date <= end_date:
            self.start_list.append(start_date)
            start_date += self.delta

    def create_params_movie(self):
        date_to_str = lambda x: x.isoformat() + 'Z'
        self.start_time = date_to_str(self.current_date)
        self.end_time = date_to_str(self.current_date + self.delta)

        params = {
            'part': 'snippet', # searchリソースのプロパティを指定 (shippet: 全てのプロパティを取得)
            'type': 'video', # 検索対象のリソースタイプを指定 (channel, playlist, video)
            'order': "viewCount", # 視聴回数順に取得
            'regionCode': 'jp', # 「日本で視聴可能」に限定
            'publishedAfter': self.start_time, # 検索の開始時間 （例: 1970-01-01T00:00:00Z）
            'publishedBefore': self.end_time, # 検索の終了時間
            'maxResults': 50
        }

        if self.query:
            params['q'] = self.query
        if self.channel_id:
            params['channelId'] = self.channel_id
        return params

    def extract_movies(self, responses):
        """ responsesから動画データを抽出 """
        cols = ['title', 'description', 'publishTime', 'channelTitle']
        movies = []
        for item in responses['items']:
            data = [item['id']['videoId']] + [item['snippet'][x] for x in cols]
            movies.append(data)
        return movies

    def run_movie(self, start, end, query=None, channel_id=None):
        self.query = query
        self.channel_id = channel_id
        if self.query is None and self.channel_id is None:
            raise ValueError('specify query or channel_id.')
        self.get_start_list(start, end)
        self.youtube = self.service.search()

        all_movies = []
        for self.current_date in tqdm(self.start_list):
            try:
                movies = self.unit_request(self.create_params_movie, self.extract_movies)
                all_movies.extend(movies)
                print(f"collect: {self.current_date}, {len(movies)}")
            except Exception as e:
                print(f"quota exceed, {self.current_date}")

        cols = ['video_id', 'title', 'description', 'publish_time', 'channel_title']
        if self.data_to_df(all_movies, cols, drop_dup=True):
            self.df = self.df.sort_values('publish_time').reset_index(drop=True)
            name = self.query if self.query is not None else self.channel_id 
            file_name = self.get_file_name(name, f"{start}_{str(self.current_date)[:len(start)]}")
            self.save_data(self.df, file_name)

    ######################## comment ########################
    def create_params_comment(self):
        """ 検索クエリにマッチするresponseを取得 """
        params = {
            'part': 'snippet',
            'videoId': self.video_id,
            'textFormat': 'plainText',
            'order': 'time',
            'maxResults': 100
        }
        return params

    def extract_comments(self, responses):
        """ responsesからコメントデータを抽出 """
        cols = ['textDisplay', 'likeCount', 'publishedAt']
        comments = []
        for item in responses['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            data = [snippet.get(c, None) for c in cols] + [snippet['authorChannelId']['value']]
            comments.append(data)
        return comments

    def run_comment(self, video_id_list):
        self.video_id_list = video_id_list
        self.youtube = self.service.commentThreads()

        all_comments = []
        for self.video_id in tqdm(self.video_id_list):
            try:
                comments = self.unit_request(self.create_params_comment, self.extract_comments)
                all_comments.extend([[self.video_id] + x for x in comments])
                print(f"collect: {self.video_id}, {len(comments)}")

            except Exception as e:
                if "quota" in str(e):
                    print(f"quota exceed, {self.video_id}")
                    break
                else:
                    print(f"error, {self.video_id}")

        cols = ['video_id', 'comment', 'like_count', 'dislike_count', 'publish_time', 'author_id']
        if self.data_to_df(all_comments, cols, drop_dup=False):
            file_name = self.get_file_name("comment", self.video_id)
            self.save_data(self.df, file_name)

    ######################## stats ########################
    def create_params_stats(self):
        params = {
            'part': 'statistics', # searchリソースのプロパティを指定
            'id': self.video_id # video_idを指定
        }
        return params

    def extract_stats(self, responses):
        """ responsesから動画データを抽出 """
        cols = ['viewCount', 'likeCount', 'commentCount']
        stats = []
        for item in responses['items']:
            data = [item['id']] + [item['statistics'][x] for x in cols]
            stats.append(data)
        return stats

    def run_stats(self, video_id_list):
        self.video_id_list = video_id_list
        self.youtube = self.service.videos()

        all_stats = []
        for self.video_id in tqdm(self.video_id_list):
            try:
                stats = self.unit_request(self.create_params_stats, self.extract_stats)
                all_stats.extend(stats)
                print(f"collect: {self.video_id}, {len(stats)}")
            except Exception as e:
                if "quota" in str(e):
                    print(f"quota exceed, {self.video_id}")
                    break
                else:
                    print(f"no stat, {self.video_id}")
                    all_stats.append([self.video_id, 0, 0, 0])
                    continue

        cols = ['video_id', 'view_count', 'like_count', 'comment_count']
        if self.data_to_df(all_stats, cols, drop_dup=True):
            file_name = self.get_file_name("stats", self.video_id)
            self.save_data(self.df, file_name)

    ######################## run ########################
    def run(self):
        """ collectorを実行 """
        if self.mode == 'movie':
            return self.run_movie(**self.args)
        elif self.mode == 'comment':
            return self.run_comment(**self.args)
        elif self.mode == 'stats':
            return self.run_stats(**self.args)
        else:
            raise ValueError('Invalid mode.')
        return self.df

if __name__ == '__main__':
    YOUTUBE_API_KEY = 'AAAAAAAAAAAAAA'

    # movie
    collector = YouTubeDataCollector(
        api_key=YOUTUBE_API_KEY,
        mode='movie',  # 'comment', 'stats'
        save=True,
        args = {
            'start': '2008-01',
            'end': '2008-01',
            'query': 'あけましておめでとう',
        }
    )
    collector.run()
    df = collector.df
