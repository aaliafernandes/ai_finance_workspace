"""Lab 08: Apple comparable-company P/E calculation.

Educational valuation exercise only; not personalized investment advice.
All prices are USD per share. Inputs are frozen in the accompanying Lab 08
source record and use the September 10, 2026 comparison date.
"""

from statistics import median


# --------------------------- Editable inputs ---------------------------
TARGET = {
    "ticker": "AAPL",
    "name": "Apple",
    "price": 326.57,
    "diluted_eps": 7.46,
}

PEERS = [
    {"ticker": "MSFT", "name": "Microsoft", "price": 492.44, "diluted_eps": 17.95},
    {"ticker": "GOOGL", "name": "Alphabet Class A", "price": 332.60, "diluted_eps": 10.82},
]
# ----------------------------------------------------------------------


def valid_positive_number(value):
    """Return True only for numeric, positive, non-Boolean values."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def pe_multiple(company):
    """Return price / diluted EPS, or None when the calculation is not meaningful."""
    if not valid_positive_number(company.get("price")) or not valid_positive_number(
        company.get("diluted_eps")
    ):
        return None
    return company["price"] / company["diluted_eps"]


def unique_peers(peers, target_ticker):
    """Keep the first ticker occurrence and exclude the target from its own peers."""
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
    """Return target EPS times a multiple, or None when the calculation is not meaningful."""
    if multiple is None or not valid_positive_number(TARGET.get("diluted_eps")):
        return None
    return multiple * TARGET["diluted_eps"]


def money(value):
    return "not meaningful" if value is None else f"${value:,.2f}"


def multiple_text(value):
    return "not meaningful" if value is None else f"{value:.6f}x"


def print_implied_summary(peers):
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
    print(f"{TARGET['name']} Comparable-Company P/E Calculator")
    print("Comparison date: September 10, 2026; annual GAAP diluted EPS only")
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
        change = (
            "not meaningful"
            if full_estimate is None or remaining_estimate is None
            else f"{remaining_estimate - full_estimate:+,.2f}"
        )
        print(
            f"Remove {removed_peer['ticker']}: remaining median-implied price "
            f"{money(remaining_estimate)}; change from full-peer estimate: {change}"
        )


if __name__ == "__main__":
    main()
