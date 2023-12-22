Here is the English translation of the `docs.md` section "実用に向けて":

---

# Practical Usage

In this document, we explain content that could be useful in practical use, such as knowledge about the YouTube API and the structure of this code.

## About the Daily API Usage Limit (quota)
The YouTube API has a concept of 'quota', and you are given 10,000 quota per day ([Official: API Overview](https://developers.google.com/youtube/v3/getting-started)). However, the amount of quota consumed varies by `mode`.
|`mode`    | Quota Consumed Per Request | Description in [Official Site](https://developers.google.com/youtube/v3/determine_quota_cost) | Maximum Retrieval per Day (※) |
|----------|----------------------------|------------------------------------------------------------|--------------------------------|
|`'movie'` | 100 quota                  | `Search-list`                                              | 100 years (month, day) of videos|
|`'comment'`| 1 quota                   | `Comment Threads-list`                                     | Comments of 10,000 videos       |
|`'stats'` | 1 quota                    | `Videos-list`                                              | Statistics of 10,000 videos     |

#### There are two important points to note due to this system:

1. <u>**In `movie` mode, consumption varies depending on how the period is specified**</u>
    
    　The ability to specify years, months, and days in this library is to increase quota efficiency by using larger units. For example, collecting three years of video data from 2020 to 2022 consumes quota as shown below, varying significantly even over the same period.
    |`start`|`end`|Number of Requests|Minimum Quota Consumption (※)|Minimum Days Required|
    |-------|-----|------------------|-------------------------------|---------------------|
    |`2020` |`2022`|`1*3=3` times    |`100*3=300` quota             |1 day                |
    |`2020-01`|`2022-12`|`12*3=36` times|`100*36=3,600` quota         |1 day                |
    |`2020-01-01`|`2022-12-31`|`365*3=1095` times|`100*1095=110,000` quota|11 days       |
    

2. <u>**The number of hits in a search can vary greatly depending on the search criteria**</u>

    　For example, when searching for recipe videos, it's easy to imagine that narrowing the criteria will result in fewer hits. In the case of `recipe` below, if there are 1,000 hits, multiple requests are needed to collect all the data.
    |`query`|Estimated Hits|Additional Requests Needed|
    |-------|--------------|--------------------------|
    |`recipe`|1,000        |Yes                       |
    |`recipe AND cabbage AND pork AND quick`|30|No    |
    


Thus, quota efficiency becomes crucial when collecting large amounts of data. Next, we explain "how often to make additional requests?"

※ The "Maximum Retrieval per Day" and "Minimum Quota Consumption per Request" assume no additional requests.

## About Additional Requests
　As mentioned in the previous chapter, when there are many hits, it's not possible to collect all data in one request. The maximum number of data retrievable per request (`maxResults`) is 50, but results exceeding 50 are common ([Official: Search function](https://developers.google.com/youtube/v3/docs/search/list)).
In such cases, the API indicates continuation with a 'PageToken' (similar to Twitter API and others).

　This library uses this mechanism to make additional requests as long as there's a `PageToken`. For example, in the 'recipe' case mentioned earlier, since there are 1,000 hits, a total of 1000/50 = 20 requests are made. This library displays the number of requests (`request_count`) for your reference.

## Can quota be increased?
　The daily quota limit is 10,000 quota (equivalent to 100 video retrieval requests or 10,000 comment requests). This library is designed to maximize quota efficiency within this limit.

However, some might wonder if it's possible to increase the quota. The answer is yes, you can apply to YouTube and increase your quota upon approval. For more details, please refer to the official site or other articles. However, I personally did not apply for an increase for the following reasons:
- The process is somewhat cumbersome
- There is not much information about quota increase
- After implementing this library, I realized that the amount of data was unnecessary for my research

Depending on your research or service, it might be beneficial to apply for a quota increase. I

 hope this article helps you in making that decision.

## Summary of Differences by `mode`
As a summary, here's a table showing the differences between each mode.

| `mode`    | `movie`                      | `comment`            | `stats`             |
|-----------|------------------------------|----------------------|---------------------|
| Specified in `args` | `start`, `end`, <br>`query`, `channel_id` | `video_id_list` | `video_id_list`    |
| Output    | Video Metadata               | Video Comments       | Video Statistical Data |
| When to Execute | First                     | After `movie`        | After `movie`       |
| Save Folder | `output/movie`              | `output/comment`     | `output/stats`      |
| Example Save Name | `keyword_2010_2010.csv` | `comment_lastvideoid.csv` | `stats_lastvideoid.csv` |
| Number of Requests | `n` times or more (※1,2) | At least `video_id` times (※1) | `video_id` times   |
| Quota Consumption per Request | 100        | 1                    | 1                   |


※1: Assuming no additional requests, this is the "minimum number of requests"  
※2: Assuming a collection period of n years, n months, or n days

### Directory Structure of this Code
```
youtube_data_collector
├── docs                # Collection of documents related to library execution (English)
│   ├── note.md         # Additional notes and precautions related to execution
│   └── usage.md        # Detailed usage instructions
├── docs_ja             # Collection of documents related to library execution (Japanese)
│   ├── note_ja.md
│   └── usage_ja.md
├── LICENSE             # License
├── README.md           # Overview
├── requirements.txt    # Dependencies
├── setup.py            # Setup
└── ytdc
    ├── __init__.py     # Initialization
    └── ytdc.py         # Main code
```

# Conclusion
　Thank you for reading this far. I hope this library is of some help to you all. If you found it useful, likes on the article and stars on GitHub are greatly appreciated.

Finally, a few points of caution:
- This code was implemented as of December 2023. Please check the latest information as needed. ([Official Site](https://developers.google.com/youtube/v3/getting-started))
- I cannot be held responsible for any loss or damage arising from obtaining the API key or using this library. Please proceed at your own risk and confirm official information.
- If you have any problems or questions, please feel free to contact me.

Thank you for your attention!
Contact: [X(Twitter)](https://twitter.com/kanure24)