"""Utility helpers for the `store` app.

Keep small, well-tested helpers here to reduce duplication in views.
"""
from typing import Dict


def get_cart(session) -> Dict[str, int]:
    """Return the cart dict stored in the session.

    Cart keys are product ids (string) and values are quantities (int).
    """
    return session.get('cart', {})


def save_cart(session, cart: Dict[str, int]) -> None:
    """Persist the cart back into the user's session."""
    session['cart'] = cart


def total_items(cart: Dict[str, int]) -> int:
    """Return total number of items in a cart."""
    return sum(cart.values())
