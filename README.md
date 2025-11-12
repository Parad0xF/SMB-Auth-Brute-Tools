# SMB Auth Brute Tools

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-TBD-lightgrey.svg)

A lightweight Python utility for rapidly testing large username/password wordlists against an SMB endpoint. The script uses the excellent [pysmb](https://pysmb.readthedocs.io/en/latest/) library under the hood and reports every authentication attempt in a format that is easy to parse or log.

## Features
- Pure-Python CLI that runs anywhere `pysmb` does (Linux, macOS, Windows, WSL).
- Prints share names for every successful login to speed up post-auth recon.
- Configurable delay between attempts to stay under SOC/SIEM thresholds.
- Clean output (`VALID`, `INVALID`, `ERROR`) that is trivial to grep or pipe elsewhere.

## Requirements
- Python 3.10+
- `pysmb` (install via `pip install pysmb`)

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # or simply: pip install pysmb
```

If you do not keep a `requirements.txt`, you can install dependencies directly:
```bash
pip install pysmb
```

## Usage
```bash
python3 smb_brute_auth.py <server> <usernames.txt> <passwords.txt> [options]
```

| Argument | Description |
| --- | --- |
| `server` | Target SMB server IP or hostname. |
| `usernames` | Path to newline-delimited username list. Blank lines are ignored. |
| `passwords` | Path to newline-delimited password list. Blank lines are ignored. |
| `--domain DOMAIN` | Optional domain/workgroup (default: empty string). |
| `--port PORT` | SMB port (default: 445). |
| `--timeout SECONDS` | Connection timeout (default: 10). |
| `--delay SECONDS` | Wait between attempts to avoid lockouts (default: 0). |

### Example
```bash
python3 smb_brute_auth.py 10.0.0.10 users.txt passwords.txt --domain ACME --delay 0.5
```

## Output Reference
```
VALID: user:pass
  Shares: ADMIN$,C$
INVALID: user:pass
ERROR: user:pass -> Failed to establish SMB session
```

- `VALID` means the credentials worked and any enumerated shares are printed on the following line.
- `INVALID` means the SMB server rejected the credentials.
- `ERROR` indicates networking or server-side issues (firewall, throttling, etc.).

## Wordlists
Sample `users.txt` and `passwords.txt` files are included to illustrate the expected format. Replace them with your own curated wordlists for real engagements. Blank lines are skipped automatically.

## Best Practices & Safety
- **Authorized use only.** Ensure you have a signed engagement letter or explicit permission before touching a target.
- Respect account lockout policies. Use the `--delay` flag to slow down attempts when necessary.
- Log your activity. The clean output format is easy to redirect into files or SIEM-friendly formats.
- Pair this script with blue-team monitoring to validate detections.

## Development
Contributions and feedback are welcome. If you have ideas for smarter throttling, better output integrations, or improved documentation, open an issue or PR.

## License
The project currently lacks an explicit license. Add one (MIT, Apache-2.0, etc.) before distributing binaries or incorporating the code into other tooling.
