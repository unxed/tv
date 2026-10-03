# tv: Turbo Vision in Free Pascal

A translation into Pascal of the C++ library [magiblot/tvision](https://github.com/magiblot/tvision)
(commit `b4831e2`) in the style of Pascal Turbo Vision: `object`, `Init`/`Done`, `New(P, Init(...))`,
`TView.HandleEvent`. The text inside is UTF-8; single-byte strings are shown through a code
page (a setting). Free Pascal 3.2.x; targets: DOS (go32v2), Linux (x86_64, i386, aarch64), Windows (win32, win64).

## Where it comes from

TV was written while reviving DOS Navigator ([unxed/dn](https://github.com/unxed/dn), the DN OSP 2.14 sources, ported to Free Pascal)
on a modern library instead of the old Borland Turbo Vision (whose sources cannot be redistributed). Everything the revival needed from the
library was done here: the translation, the UTF-8 text inside, the backends (DOS, Unix terminals, Windows console, memory), the terminal
emulator view, the help system, the file dialogs. Then the library was split out of `dn` into this repository, because it is useful
without DN: a program on Turbo Vision needs TV, not a file manager.

`dn` uses this repository as the git submodule `tv/`. Nothing here depends on `dn`.

## License

- The translated units are a derivative work of magiblot/tvision, and so of the Turbo Vision 2.0
  release published by Borland: the Borland disclaimer and the MIT license of magiblot apply
  ([`COPYRIGHT.magiblot`](COPYRIGHT.magiblot)). The header of each such unit names the magiblot
  files it was translated from.
- The units written for this port (the backends `TvSys`, `TvMem`, `TvDos`, the terminal units, `TvUtil` in the part that was not
  translated from magiblot, the help compiler, the tests, the demos) are under the MIT license ([`LICENSE`](LICENSE)), so
  that the package as a whole has one clear license. Their header says "Written for this port".
- No code of DN is in this repository, and no code of this repository is copied into DN: `dn` links to it as a submodule.
  DN has its own license (see the `dn` repository).

## Contents

- `src/`: the units (the list and the correspondence to the magiblot files are in [`DESIGN.md`](DESIGN.md), in Russian);
- `tests/`: a test program per unit, `t_<unit>.pas`, on the "in memory" backend (`TvMem`); they run natively and under DOS; `tests/pty/`: tests of the Unix backend in a pseudo terminal (Python);
- `dostests/`: tests of the DOS backend (in DOSBox-X only);
- `demo/`: `tvdemo.pas` (windows, menus, status line; the smallest example) and `tvterm.pas` (a shell in a TV window);
- `tools/tvhc.pas`: the help compiler (`.htx` to `.hlp`, the format of the Borland help compiler).

The backends: `TvDos` (DOS: video memory, BIOS keyboard, INT 33h mouse), `TvUnix` with `TvTermIo`/`TvTermOs` (Unix terminals and the Windows console:
raw mode, ANSI output, key and mouse reports; the terminal protocols are in `DESIGN.md`), `TvMem` (tests). The embedded terminal: `TvVt` (emulator),
`TvPty` (a pty and the program), `TvVtKeys`, `TvVtView` (the view), `TvVtRun` (run a program on the whole screen and keep what it drew).

## Build and check

From the root of this repository, with `fpc` 3.2.x:

    cd tests
    for t in t_*.pas; do fpc -Fu../src -Fu. $t && ./${t%.pas}; done   # each prints "ALL OK"

This leaves `.o` and `.ppu` files next to the sources; `dn` has a script that builds them aside (`tools/tv-test.sh` in `dn`: `-FU`/`-FE` into a work
directory, another CPU with `TV_FPC` and `TV_RUN`).

Under DOS you need a go32v2 cross compiler and DOSBox-X: `tools/build-fpc-go32v2.sh` and `tools/dos-run.sh` (they live in the `dn` repository, see
`tools/` there; the CI of `dn` runs the whole set of tests, native, DOS, ARM under qemu, Windows).

## How to use it in your project

**A program on the TV API.** Add `src` to the unit path (`-Fu`); in the program use `TvApp` (the application), `TvViews`, `TvWindow`, `TvMenus`,
`TvDialog` and the like, and a backend: `TvDos` under DOS, `TvUnix` on Unix and Windows, `TvMem` in tests. The minimal example is
[`demo/tvdemo.pas`](demo/tvdemo.pas); `{$I src/tvdefs.inc}` sets the compiler mode (objfpc) the units expect. The unit names are `TvXxx`, not
the Borland names (`Views`, `Dialogs`, `App`...): see the next section if you have code that uses those.

**Code written for the Borland Turbo Vision (the shim units).** DN has about 160 files written for Borland TV, with `uses Views, Dialogs, App, Objects, ...`. To compile
them against this library without renaming everything, `dn` generates *shim units*: units with the Borland names that only give the names of the `Tv*` units. The tools
are in the `dn` repository (not here yet; this is documentation of where they are):

- `tools/gen-shim.py MAP_FILE OUT_DIR [TV_SRC_DIR]`: reads the interfaces of the listed `Tv*` units and writes `UNIT.pas` per shim: a type or a constant becomes an alias
  (the members of an enumeration become constants), a variable becomes `absolute` of the original, a procedure or a function becomes a wrapper. Nothing else is in a shim.
- `dn/shims/shims.map`: the map, one line per shim: `Views: TvGeom TvColors TvKeys TvEvents ... [+OwnUnit] [-Name] [-Prefix*]` (`+Unit` goes to the `uses` only,
  `-Name` is a name that is not given, `-Prefix*` all the names that begin so). It shows which Borland unit became which `Tv*` units (`Views`, `Dialogs`, `App`, `MsgBox`, `StdDlg`,
  `Objects`, `Collect`, `Streams`...).
- `dn/shims/manual/UNIT.inc` and `UNIT.impl.inc`: what is written by hand and included into the shim (the interface part and the implementation part): the names that the
  Borland unit had and `Tv*` has not, or has differently (`defines*.inc`, `collect*.inc`, `views*.inc`, `dialogs.inc`, `streams.inc`; about 500 lines).
- `tools/dn-env.sh` (`dn_gen_shims`): how the shims are generated into a build directory (not committed) and put on the unit path next to `tv/src`.

Differences from Borland TV that the shims cannot hide and that cost time in DN (worth knowing before you start): the fields `Command` and `KeyCode` of `TEvent` are not at the same place (`Message(R, evKeyDown, Key, nil)`
does nothing; DN has `MessageKey` for it); the text of a key is UTF-8 (`Text`, `TextLength`), not only a character; strings can be UTF-8 inside; the screen is 16-bit cells with attributes of
`TvCell`; resources (streams) use `TStreamRec` and deferred pointer fixups (`GetSubViewPtr` of `TView` is deferred, of `TGroup` immediate: a saved desktop depends on it).
The notes on what else was met during the revival are in `docs/MODERNIZATION-GUIDE.md` of `dn`.

**Other things in `dn` that could be reused (not done: only noted):**

- `tools/gen-codepage.py` (makes `src/tvcp.inc`, the tables byte to Unicode for DOS code pages) and `tools/gen-width.py` (makes `src/tvwidth.inc`, the widths of Unicode characters, from the Unicode
  database of Python): the generators of two files of this repository; they live in `dn` for now.
- `dn/src/drivers.pas` (DN's own compatibility layer over `Tv*`: the key code of DN with shift bits, `MessageKey`, double click, the screen of the user) and `dn/src/vpsyslow.pas` (the system layer
  of Virtual Pascal over `TvSys`: file names, the screen, running programs): their license is that of DN, see `dn/PROVENANCE.md` before taking anything.
- The cross compilers: `tools/build-fpc-go32v2.sh`, `build-fpc-i386-linux.sh`, `build-fpc-aarch64-linux.sh`, `build-fpc-windows.sh`: scripts that build an FPC 3.2.2 cross compiler from the sources.
- `tools/pty_screen.py`, `tools/render-dump.py`: a terminal screen for tests in a pty, and a picture of a DOS screen dump.

## History

This repository was split out of [unxed/dn](https://github.com/unxed/dn) (directory `tv/`). Its history is the history of that
directory in `dn` up to `dn` commit `b8f2bd1` (the commits that touched `tv/`, with their original messages and dates, so some
messages mention `PLAN.md` and other parts of `dn`; the hashes differ from the ones in `dn`).

**Development continues here, in this repository.** `dn` no longer has a copy of this code: it uses this repository as the git
submodule `tv/` (the commit recorded in `dn` is the version DN builds with). A change to TV is made and tested here; then `dn` moves
its pointer (`git -C tv pull && git add tv`).

Some comments in the sources and `DESIGN.md` still say `tv/src`, `tv/tests` (the old paths inside `dn`): read them without the `tv/`.
