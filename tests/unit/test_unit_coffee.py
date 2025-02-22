from eth_utils import to_wei
import boa
from tests.conftest import SEND_VALUE

RANDOM_USER = boa.env.generate_address("non-owner")

def test_price_feed_is_correct(coffee_funded, eth_usd):
    assert coffee.PRICE_FEED() == eth_usd.address


def test_starting_value(coffee_funded, account):
    assert coffee.MINIMUM_USD() == to_wei(5, "ether")
    assert coffee.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee_funded):
    with boa.reverts("You must spend more ETH!"):
        coffee.fund()

def test_fund_with_money(coffee_funded):
    # Arrange
    boa.env.set_balance(account.address, SEND_VALUE)
    # Act
    coffee.fund(value=SEND_VALUE)
    # Assert
    funder = coffee.funders(0)
    assert funder == account.address
    assert coffee.funder_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded):
    with boa.env.pranks(RANDOM_USER):
    with boa.reverts("Not the contract owner!"):
    coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded):
    with boa.env.pranks(coffee_funded.OWNER()):
    coffee_funded.withdraw()
    assert boa.env.get_balance(coffee_funded.address) == 0

def test_get_rate(coffee):
    assert coffee.get_eth_usd_rate(SEND_VALUE) > 0