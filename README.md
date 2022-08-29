# youaresafe

[youaresafe!](https://github.com/youaresafe/youaresafe) (YAS!) is a cross-platform Flutter app that allows you to look up trigger warnings for movies and TV shows.

YAS! is based on publically available [IMDb data files](https://datasets.imdbws.com) and uses [Firebase](https://firebase.google.com) as a backend.

## Database Initialisation

Before compiling the project, you need to download the IMDb data. To do so, you can use the script [`scripts/init_db.py`](scripts/init_db.py):

```shell
$ python scripts/init_db.py assets/imdb.sqlite
```

## Note

This project is heavily work in progress. 😌