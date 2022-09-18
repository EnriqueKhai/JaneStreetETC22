from market_maker import MarketMaker
from jane_street import Exchange


# ~~~~~============== CONFIGURATION  ==============~~~~~

team_name = "POOLCAPITAL"


# ~~~~~============== MAIN LOOP      ==============~~~~~

def main():
    args = parse_arguments()

    exchange = Exchange(args=args)
    mm = MarketMaker(exchange, logging=True)

    while True:
        message = exchange.read_message()
        mm.listen(message)

        if message["type"] == "close":
            print("the round has ended")
            break


def parse_arguments():
    pass


if __name__ == "__main__":
    # Check that [team_name] has been updated.
    assert (team_name != "REPLACEME")
    main()