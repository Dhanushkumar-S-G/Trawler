from socialscan.util import Platforms, sync_execute_queries

queries = ["dhanushkumar.20cs@kct.ac.in"]
platforms = [Platforms.GITHUB, Platforms.INSTAGRAM,Platforms.YAHOO,Platforms.TWITTER ,Platforms.REDDIT,Platforms.SNAPCHAT]
results = sync_execute_queries(queries, platforms)
for result in results:
    print(result.query ,result.success , result.platform)