# The Beatles Songs Analysis Project

The Beatles Songs Analysis project aims to get some statistical information on the songs of the Beatles and implement some data science methods on the collected data.

The raw data to be collected includes name, authorship, lyrics, year, album, and duration for each song.

There are some pecularities which must be taken in consideration:

* The songs that were released before 1963 and after 1970 (i.e. before the release of the first single and after the split of the band), instrumentals (for example, *Flying*), songs in German (*Komm, Gib Mir Deine Hand* and *Sie Liebt Dich*), and avangardist compositions (*Revolution 9*) are not taken into account in the analysis.

* Songs that were released on singles only, were collected on The Beatles Past Masters Vol. 1 and 2 albums (1988). In the analysis they get the respecting year, but not the name of the album.

* If a song is present on many albums, only the first occurence is counted as valid. Others are not taken into account.

* If a song is present on an album and on a single, the album version is one taken into account.

The script *get_data.py* gets the Beatles songs data from free web sources, adds some useful information and stores the result into a json file.

**Step 1. Second by Second: Length above All**. Here I analyze statistical information about songs length as a simple but interesting attribute.

**Step 2. Words, Words, Words...** Here I conduct the comparison of general statistical information about word numbers in titles and lyrics, taking into consideration such parameters as release year and originality.

**Step 3. Whose Voice is Soothing?**. We know that all the four Beatles members were singers. But they sang both alone and together in different songs. So, here I analyze vocals data.

**Step 4. Authors**. Here I do some analysis of the Beatles songs authorship. Only official authorship data is analyzed, i.e., all non-cover songs belong to Lennon-McCartney, Harrison, or Starkey. Sure, the lion share of the Beatles songs is attributed to Lennon-McCartney. But there is some interesting information behind it to reveal.

**Step 5. Word Frequency: You and I**. This step contains analysis of word frequency in the Beatles songs.

**Step 6. Word Frequency: Love and Know**. Here I continue to explore the word frequency in the Beatles lyrics. Let's remove stopwords and see what happens.

**Step 7. Parts of Speech**. This step contains analysis of parts of speech (POS) frequency in the Beatles songs.

**Step 8. Parts of Speech 2**. Here I explore the most frequent words in the songs of the Beatles according to their classes and semantics.