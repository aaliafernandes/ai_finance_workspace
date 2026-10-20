"""Lab 07: comparable-company P/E calculation for the Asbury worked case.

Educational valuation exercise only; not personalized investment advice.
All prices are USD per share.  Inputs are frozen case inputs supplied in Lab 07.
"""

from statistics import median


# --------------------------- Editable inputs ---------------------------
TARGET = {
    "ticker": "ABG",
    "name": "Asbury Automotive",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"ticker": "AN", "name": "AutoNation", "price": 169.84, "diluted_eps": 16.92},
    {"ticker": "GPI", "name": "Group 1 Automotive", "price": 421.48, "diluted_eps": 36.81},
]
# ----------------------------------------------------------------------


def valid_positive_number(value):
    """Return True only for numeric, positive, non-Boolean values."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def pe_multiple(company):
    """Return price / diluted EPS, or None when that calculation is not meaningful."""
    if not valid_positive_number(company.get("price")) or not valid_positive_number(
        company.get("diluted_eps")
    ):
        return None
    return company["price"] / company["diluted_eps"]


def unique_peers(peers, target_ticker):
    """Keep the first entry per ticker and remove the target if it appears as a peer."""
    seen_tickers = {target_ticker.upper()}
    result = []
    for peer in peers:
        ticker = str(peer.get("ticker", "")).upper()
        if not ticker or ticker in seen_tickers:
            continue
        seen_tickers.add(ticker)
        result.append(peer)
    return result


def implied_price(multiple):
    """Return target EPS times the given multiple, or None if either input is unusable."""
    if multiple is None or not valid_positive_number(TARGET.get("diluted_eps")):
        return None
    return multiple * TARGET["diluted_eps"]


def money(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def multiple_text(value):
    return "not meaningful" if value is None else f"{value:.6f}x"


def print_implied_summary(peers):
    """Print range rules: one usable peer is a reference estimate, not a range."""
    usable_multiples = [pe_multiple(peer) for peer in peers if pe_multiple(peer) is not None]
    if not usable_multiples:
        print("No usable peers: no peer-implied estimate.")
        return None

    median_multiple = median(usable_multiples)
    median_estimate = implied_price(median_multiple)
    print(f"Peer median P/E: {multiple_text(median_multiple)}")
    if len(usable_multiples) == 1:
        print(f"One valid peer: reference estimate (no range): {money(median_estimate)}")
    else:
        print(
            "Peer-implied range (minimum to maximum peer P/E): "
            f"{money(implied_price(min(usable_multiples)))} to "
            f"{money(implied_price(max(usable_multiples)))}"
        )
        print(f"Target at peer median P/E: {money(median_estimate)}")
    return median_estimate


def main():
    peers = unique_peers(PEERS, TARGET["ticker"])
    print("Asbury Automotive Comparable-Company P/E Calculator")
    print("Frozen case inputs: December 31, 2024 close and FY2024 GAAP diluted EPS")
    print(f"Target: {TARGET['name']} ({TARGET['ticker']})")
    print(f"Target price: {money(TARGET.get('price'))}; diluted EPS: {money(TARGET.get('diluted_eps'))}")
    print("\nPeer P/E multiples")
    for peer in peers:
        print(f"{peer['name']} ({peer['ticker']}): {multiple_text(pe_multiple(peer))}")

    print("\nFull-peer result")
    full_estimate = print_implied_summary(peers)

    print("\nLeave-one-peer-out results")
    for removed_peer in peers:
        remaining_peers = [peer for peer in peers if peer is not removed_peer]
        remaining_multiples = [
            pe_multiple(peer) for peer in remaining_peers if pe_multiple(peer) is not None
        ]
        if not remaining_multiples:
            print(f"Remove {removed_peer['ticker']}: no remaining usable peers; no estimate.")
            continue
        remaining_estimate = implied_price(median(remaining_multiples))
        if full_estimate is None or remaining_estimate is None:
            change = "not meaningful"
        else:
            change = f"{remaining_estimate - full_estimate:+,.2f}"
        print(
            f"Remove {removed_peer['ticker']}: remaining median-implied price "
            f"{money(remaining_estimate)}; change from full-peer estimate: {change}"
        )


if __name__ == "__main__":
    main()
