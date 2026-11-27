# Test log — news-image-20261126

- 2026-11-27 01:24 UTC: `python3 generate_entry.py` → entry.png 1024x1024, 158,956 bytes, sha256 47816c95…
- Visual check: lead badge overlapped the 4th body line; Ukraine card body spilled past the card edge ("Odesa." clipped).
- Fix (second message): trimmed lead body to 3 lines, moved badge down, shortened Ukraine body, capped card bodies at 3 lines.
- 2026-11-27 01:25 UTC: `python3 generate_entry.py` twice → identical sha256 02fca16b…
- `python3 main.py /tmp/out1/entry.png` and `/tmp/out2/entry.png` → both sha256 02fca16b…, identical to entry.png.
- Visual check of final image: all six stories complete, no overlap, no clipping.
