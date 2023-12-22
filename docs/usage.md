Here is the English translation of the `docs.md`:

---

# Main Features
This library allows for the collection of three primary types of data:
1. [Video Metadata](#1-collecting-video-metadata): Titles, descriptions, etc. (`mode='movie'`)
2. [Video Comments](#2-collecting-video-comments) (`mode='comment'`)
3. [Video Statistical Data](#3-collecting-video-statistics): Number of likes, views, etc. (`mode='stats'`)

## Commonalities Across All Features
Regardless of the data type being collected, the basic form remains the same. (Please refer to Quick Start before executing.)
``` Python
collector = YouTubeDataCollector(
    api_key=YOUTUBE_API_KEY, # Common
    mode='movie', # Specify either 'movie', 'comment', or 'stats'
    save=True, # True or False
    args={}, # Varies depending on the mode
    file_name=None, # Automatically set if not specified
    output_path='output' # Automatically set if not specified
)
collector.run()
df = collector.df
```
The parameters are as follows:
- Mandatory
    - Common across all `mode`
        - `api_key`: Enter your API key
        - `save`: Whether to save the collected data
    - Varies by `mode`
        - `mode`: Specify either `'movie'`, `'comment'`, or `'stats'`
        - `args`: Parameters vary depending on the `mode`
- Optional
    - `file_name`: Name of the file to save (specify to prevent overwriting when executed multiple times)
    - `output_path`: Output folder (automatically creates an `output` folder if not specified)

In addition to the parameters, there are two main differences depending on the `mode`:
- When collecting comments and statistical data, you first need to collect video metadata
- The way data is saved

The following sections provide detailed explanations for each of the three `mode`.

## 1. Collecting Video Metadata
To collect video metadata, specify `mode='movie'`.
``` Python
collector = YouTubeDataCollector(
    api_key=YOUTUBE_API_KEY,
    mode='movie',
    save=True,
    args = {
        'start': '2008-01',
        'end': '2008-01',
        'query': 'Happy New Year',
        # 'channel_id': 'specify_channel_id',
    }
)
collector.run()
df_movie = collector.df
df_movie
```

The contents of `args` include the following four:
- Mandatory
    - `start`: Start date and time for the videos to be collected
    - `end`: End date and time for the videos to be collected
- At least one required
    - `query`: Search query
    - `channel_id`: Channel ID

### start / end
First, you need to specify the start and end dates for the videos to be collected. You can specify any combination of year, month, and day, and data will be saved according to these units.

(Example) To collect data from 2010 to 2012:
|`start` |`end`|Example Save Name|
|--------|-----|-----------------|
|`'2010'`|`'2012'`|`keyword_2010_2012.csv`|
|`'2010-01'`|`'2012-12'`|`keyword_2010-01_2012-12.csv`|
|`'2010-01-01'`|`'2012-12-31'`|`keyword_2010-01-01_2012-12-31.csv`|

All three patterns yield essentially the same results. Thus, for long-term data collection, it is advised to use larger units (year, month) for API efficiency. (For more details, see `note.md`)

### query / channel_id
Next, specify `query` or `channel`. Ensure to specify at least one in `args`.

1. `query`

    Keywords (`query`) can be freely set and separated by spaces for multiple queries. Similar to Twitter API, you can use `AND` or `OR` for searching.
    ```
    'query': '(today OR tomorrow) AND (sunny OR rain)'
    ```
    This example will collect videos containing "today & sunny," "today & rain," "tomorrow & sunny," and "tomorrow & rain."

2. `channel_id`

    If you wish to collect videos by channel name, you can specify it using `channel_id`.

    Note that `'channel_id'` is a unique alphanumeric string for the channel, not the `'ChannelTitle'` or something starting with '@'. You can obtain it by entering the channel URL as described in [this article](https://ilr.jp/tech/485/

).

### save
In `movie` mode, data like the following will be output (note: all data here is fictional):

| video_id | title                     | description           | publish_time          | channel_title |
|----------|---------------------------|-----------------------|-----------------------|---------------|
| ab12cd   | Happy New Year Video      | A video of the sunrise| 2008-01-01T01:23:45Z  | Helloworld    |
| zy34xw   | New Year's Greetings      | Happy New Year!       | 2008-01-01T23:45:00Z  | Dummies       |

By default, the following will be automatically created and saved:
- `output/movie/Happy_New_Year_2008-01_2008-01.csv`

## 2. Collecting Video Comments
When collecting comments and statistical data, you first need to collect video metadata and create a `video_id_list` from that data.
```
video_id_list = pickup_video_id(df_movie)
```
Use this `video_id_list` to collect comments with `mode='comment'`.
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
The only required parameter in `args` is `video_id_list` (list of video IDs).

If the API fails during collection, you can update the `video_id_list` using the last collected `video_id` and continue from there.
```
last_id = 'LastSavedVideoId'
video_id_list = update_list(video_id_list, last_id)
```

### save
In comment mode, you can retrieve data like this:

| video_id | comment           | like_count | publish_time          | author_id |
|----------|-------------------|------------|-----------------------|-----------|
| ab12cd   | Such a joyful one | 5          | 2008-01-02T10:20:30Z  | AAAAAAAAB |
| ab12cd   | Happy new year    | 2          | 2013-01-23T12:34:56Z  | CCCDDDEEE |

By default, the following will be automatically created and saved (using the last `video_id`):
- `output/comment/comment_lastvideoid.csv`

## 3. Collecting Video Statistical Data
Similar to comments, create a `video_id_list` and then execute the collection.
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
The only required parameter in `args` is `video_id_list` (list of video IDs).

### save
In statistics mode, you can retrieve data like this:

| video_id | View_count | like_count | comment_count |
|----------|------------|------------|---------------|
| ab12cd   | 33333      | 3          | 1             |
| zy34xw   | 4321       | 1          | 0             |

By default, the following will be automatically created and saved (using the last `video_id`):
- `output/stats/stats_lastvideoid.csv`
