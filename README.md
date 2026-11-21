# Raw Signal — feed host

Machine-readable pieces of the **Raw Signal** podcast: the RSS feed listeners and
podcast apps subscribe to, the cover art, and the page at
<https://rawqubit.github.io/raw-signal-feed/>.

- Feed: <https://rawqubit.github.io/raw-signal-feed/feed.xml>
- Show page (canonical): <https://srinikhilchakilam.com/rawsignal/>
- Spotify: <https://open.spotify.com/show/4oXU0Gpsb1gU2VoVPzM8TH>

`index.html` is generated from `feed.xml` with
`python3 tools/podcast/build.py feed.xml index.html …` in the portfolio repo, so
the episode list on this page and the feed can never disagree. `.nojekyll` keeps
GitHub Pages from running Jekyll over the generated file.

Rebuild the feed itself with `python3 build_mirror.py --base-url https://rawqubit.github.io/raw-signal-feed/`.
