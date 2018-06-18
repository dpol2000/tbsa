# The Beatles Songs Analysis Project

The Beatles Songs Analysis project aims to get some statistical information on the songs of the Beatles and implement some data science methods on the collected data.

The raw data to be collected includes name, authorship, lyrics, year, album, and duration for each song.

There are some pecularities which must be taken in consideration:

* The songs that were released before 1963 and after 1970 (i.e. before the first single and after the split of the band), instrumentals (for example, *Flying*), songs in German (*Komm, Gib Mir Deine Hand* and *Sie Liebt Dich*), and avangardist compositions (*Revolution 9*) are not taken into account in the analysis.

* Songs that were released on singles only, were collected on The Beatles Past Masters Vol. 1 and 2 albums (1988). In the analysis they get the respecting year, but not the name of the album.

* If a song is present on many albums, only the first occurence is counted as valid. Others are not taken into account.

* If a song is present on an album and on a single, the album version is one taken into account.

The script *get_data.py* gets The Beatles songs data from free web sources, adds some useful information and stores the result into a json file.

