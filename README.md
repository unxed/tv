# tv: Turbo Vision in Free Pascal (the first translation)

This repository holds the first translation into Pascal of [magiblot/tvision](https://github.com/magiblot/tvision) (commit `b4831e2`),
made with `object` types for the revival of DOS Navigator ([unxed/dn](https://github.com/unxed/dn)).

**The work continues in [unxed/tv3](https://github.com/unxed/tv3)** (the library with classes); dn and the Free Pascal IDE of
[unxed/sp](https://github.com/unxed/sp) use tv3. This repository is kept for its history and is not developed further.

## The history

On 2026-10-08 the history was rewritten: some files were removed from every commit, together with the programs compiled from them;
the commits themselves (their dates, authors and messages) are kept, so some of them are empty now and the tree of an old commit
may not build. The old ids and the new ones: [docs/REWRITE-MAP.md](docs/REWRITE-MAP.md).

To check the tree and every commit of the history against the reference corpora: `tools/audit/run.sh` (it fetches the corpora once
into `~/.cache/tv-audit`; see `tools/audit/fetch-corpora.sh`).

## License

See [LICENSE](LICENSE) and [COPYRIGHT.magiblot](COPYRIGHT.magiblot).
