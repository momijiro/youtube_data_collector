# Main Features
This library allows for the collection of three main types of data:
1. [Video Metadata](#1-collecting-video-metadata) : Title, description, etc. (`mode='movie'`)
2. [Video Comments](#2-collecting-video-comments) (`mode='comment'`)
3. [Video Statistical Data](#3-collecting-video-statistics) : Number of likes, views, etc. (`mode='stats'`)

## Commonalities Across All Features
Regardless of the data type being collected, the basic form is the same. (Please refer to the Quick Start section before running.)
``` Python
collector = YouTubeDataCollector(
                api_key=YOUTUBE_API_KEY, # Common for all modes
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
        - `save`: Whether to save the collected data or not
    - Varies by `mode`
        - `mode`: Specify either `'movie'`, `'comment'`, or `'stats'`
        - `args`: Parameters vary depending on the `mode`
- Optional
    - `file_name`: Name of the file to save (specify to prevent overwriting when running multiple times)
    - `output_path`: Folder to output the data (automatically creates an `output` folder if not specified)

Apart from the parameters, there are two main differences depending on the `mode`:
- When collecting comments and statistical data, you first need to collect video metadata
- The way the data is saved

The following sections explain each of the three `mode` types in detail.

## 1. Collecting Video Metadata
For collecting video metadata, specify `mode='movie'`.
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

Details of `args` include the following four:
- Mandatory
    - `start`: Start date of the videos to be collected
    - `end`: End date of the videos to be collected
- At least one required
    - `query`: Search query
    - `channel_id`: Channel ID

### start / end
First, you need to specify the start and end dates for the videos to be collected. However, if the units of `start` and `end` are the same, you can specify either year, month, or day, and the data will be saved in those units.

(Example) To collect data from 2010 to 2012
|`start` |`end`|Example Save Name|
|---|---|---|
|`'2010'`|`'2012'`|`keyword_2010_2012.csv`|
|`'2010-01'`  |`'2012-12'`|`keyword_2010-01_2012-12.csv`|
|`'2010-01-01'`  |`'2012-12-31'`|`keyword_2010-01-01_2012-12-31.csv`|
||

All three patterns will yield the same results in principle. Therefore, use larger units (year, month) for long-term data collection for API efficiency. (For more details, see `note.md`)

### query / channel_id
Next, specify `query` or `channel`. Ensure that at least one of these is specified in `args`.

1. `query`

    The keyword (`query`) can be freely set and separated by spaces for multiple queries. Similar to the Twitter API, you can use `AND` or `OR` for searching, as follows:
    ```
    'query': '(today OR tomorrow) AND (sunny OR rain)'
    ```
    This example will collect videos containing "today & sunny," "today & rain," "tomorrow & sunny," and "tomorrow & rain."

2. `channel_id`

    You can also specify by the channel ID that created the videos.

    However, the `'channel_id'` is not the `'ChannelTitle'` or something starting with '@', but a unique alphanumeric string for that