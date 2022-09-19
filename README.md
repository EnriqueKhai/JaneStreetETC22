# JaneStreetETC22

![jane_street_etc_2](https://user-images.githubusercontent.com/42400406/190888314-15209690-4a9d-4da1-a4e5-da077f6ef287.jpg)

> From left to right: Siyi, Zifeng, Tejas, and... me!

This weekend, my team and I took part in Jane Street's Electronic Trading Challenge 2022 and came in at 1st place!

The contest was held in Singapore, at the very luxurious *Shangri-La* hotel on 17/09/2022 from 10am till 6pm. Importantly, breakfast and lunch were catered (yum)!

## Table of Contents

- [Overview](#overview)
    - [Introduction to the Challenge](#introduction-to-the-challenge)
    - [Set up](#set-up)
- [Preparations](#preparations)
- [Phase 1: Finding the Way](#phase-1-finding-the-way)
    - [A Tale of Two Styles](#a-tale-of-two-styles)
    - [ADR Arbitrage](#adr-arbitrage)
    - [ETF Arbitrage](#etf-arbitrage)
    - [Gambles & Speculation](#gambles-speculation)
    - [The Winning Strategy](#the-winning-strategy)
- [Phase 2: The Final Hour](#phase-2-the-final-hour)
- [Closing Thoughts](#closing-thoughts)

## Overview

### Introduction to the Challenge

Provided by the organizers:

> etc is a programming challenge. The goal is to write a program that will make fake money by trading securities on a fake financial exchange. The market participants will include other people’s programs, as well as some programs provided by us (the “marketplace bots”).

### Set up

For the challenge, Jane Street provided each team with a secured Ubuntu Linux box in the cloud wherefrom we could interact with the production exchange to place buy and sell orders.

They also kindly provided us with a *Python3* convenience class `Exchange()`  that exposed general utility functions such as `.read_public_feed()`, `.send_order(order)` and `.cancel_order(id)`.

Lastly, there were two deployment environments `--production` and `--test` to which we could field our bots.

## Preparations

The event kicked off at 10am sharp with a briefing on **what** the challenge actually was (it was the first time for all of us).

Provided by the organizers:

> The challenge consists of a series of five minute matchups. In each matchup, you and another team compete to be the best market maker, providing liquidity to a third bot called the “marketplace”.
>
> The marketplace will send some orders around the fair value. Some orders will, like yours, be orders intended to provide liquidity. Other orders from the marketplace will be emulating liquidity demanders – people who just wish to buy or sell a certain amount of shares, and don’t care too much about the price they get.
>
> At the end of a matchup, the exchange closes and then reopens shortly afterwards for the next matchup, where you’ll be playing alongside a different team. We reset your cash and positions too.
>
> There will be two distinct competitions, with two distinct prizes.
>
> The first will run (more-or-less) continuously between 11:00 am and 5:00 pm. Scores during each phase of this competition will be weighted as shown below...
>
> At 4:00 pm we will start the second, simultaneous competition: “The Final Hour”. The winner of this competition is the team that has the highest cumulative score in just the last hour of competition.

Then, we were given handouts on various financial instruments like stocks, bonds and ADRs to study (we are programmers, not bankers). There was a lot to read and understand so I busied myself with the docs.

At 11am, the linux boxes were finally opened and, with palpable excitement in the air, we were off to the races!

## Phase 1: Finding the Way


### A Tale of Two Styles

In the challenge, there were four "regularly stocks" `[VALBZ, GS, MS, WFC]`. In addition, there was `VALE` (an [ADR](https://www.investopedia.com/terms/a/adr.asp) of `VALBZ`) and `XLF` (an [ETF](https://www.investopedia.com/terms/e/etf.asp) of `[GS, MS, WFC]`).

Immediately, it was clear to us that the assets divided themselves very naturally into two types: (1) ADRs and (2) ETFs.

Hence, we split ourselves further into two subteams. Zifeng and Si Yi drafted tactics for `[VALBZ, VALE]` while me and Tejas developed strategies for `[GS, MS, WFC, XLF]`.

### ADR Arbitrage

Zifeng and Si Yi were the quickest to enter the market; they prototyped their ADR arbitrage strategy and deployed it to production at breakneck speed.

Basically, 1 share of `VALE` can be converted to/from 1 share of `VALBZ` (with a conversion fee of $10). Then, if the prices of those two instruments ever differed significantly due to inefficiencies in the market, we could buy the cheaper of the two, convert it into the other and sell for higher!

The results were good too!

We were earning around $300 per round and were consistently ranking between 3rd - 7th!

### ETF Arbitrage

On our side, the idea was similar.

According to the specs, 10 shares of `XLF` could be converted to/from a basket of `[3 BOND, 2 GS, 3 MS, 2 WFC]` (with a conversion fee of $100). Then, if the sum of the underlying assets ever differed significantly from `XLF`, their aggregate, then we could buy the cheaper of the two, convert into the other and (again) sell for higher.

That said, the details of the implementation were not immediately clear to me so Tejas took on the Mathematics while I collated live data for each round.

The questions of interest included the following: (1) what are the opening and closing prices of each stock for each round and (2) how many trades of each stock took place per round.

It was here that I saw something suspicious.

### Gambles & Speculation

For a few rounds in a row, one of our bots in the test environment was steadily raking in profits while doing **no** trading at all!

Someone had bought 2 shares of `MS` and 12 shares of `XLF` previously but then forgot about it. That meant that just by holding those two stocks we were contributing towards our P&L via appreciation!

Then, we added a new strategy to production: at the start of each 5 minute round, buy as many shares of `MS` and `XLF` as we could and hold them all the way.

The result? Surprising. We were now earning roughly $600 per round and we didn't even know why HAHAHA (is it truly a trading challenge if there wasn't any speculation???)

It was around here, at 2pm, that we advanced to 2nd overall and gained some much needed confidence!

### The Winning Strategy

Halfway through the competition, we realized something.

There were roughly 5,000 trades per round. Instead of racking our brains trying to earn the maximum possible profit on a **single** trade, why not earn a dollar on **every** one of them? Instead of waiting for the market to be "ripe" for arbitrage (passive/ timing the market), we wanted a cut of every trade ever made (active/ time in the market).

In essence, we wanted to be market makers. For each asset, we would (A) compute its fair price and (B) place a buy order at `fair_price - 1` and another sell order at `fair_price + 1`, i.e., buy low and sell high.

Here, we set the delta to be `+/- 1` so as to keep the spread tight and ensure that our orders would always get filled first (and, in fact, every time).

There was just one problem. How do we compute the fair price? The most natural idea would be to take the average of the best buy and sell orders. We did not do that.

We felt that the order book was an aggregation of individual speculation. That is, it was likely not the best method to infer a fair price.

Instead, we took the last transacted price of the asset to be its fair price.

The result? Spectacular! We were now pulling in over $10,000 per round! They say that the biggest winners during the gold rush were the people who sold the shovels. Here? That seemed to check out.

By providing liquidity (always ensuring people could buy or sell their assets) and capturing the bid-ask spread, we pulled away from the competition entirely and were now comfortably in 1st place with two hours left to go.

## Phase 2: The Final Hour

At last, with our refined implementations all teams started the last leg of the competition.

All cash and positions were reset and the main event commenced.

Since deploying our market making strategy to production, we were earning an average of $10,000 per round. Would that continue to be the case?

Turns out our strategy was sufficient. We lead the event comfortably from the start, though that did nothing to assuage the anxiety that another team might come up from behind to overtake us.

It was only after all twelve rounds of the final event had concluded and we won with a P&L of $8,000,000 that we could breathe a sigh of relief!

## Closing Thoughts

This is my first experience with algorithmic trading and it was a great learning experience! If anything, seeing the number of trades per second executed by our trading bot truly opened my eyes to the world and prowess of high-frequency trading.

Seeing our P&L increase steadily at first and then dramatically towards the end was also super exhilarating! That said, trading at a loss was anxiety-inducing in equal measure... the day was a roller coaster-ride to be sure!

Overall, I felt the event was extremely well organized and very, very fun! The infrastructure alone must have been a humongous effort behind the scenes. The seamless execution to (1) ensure that the exchange ran smoothly and (2) rate-limited participants appropriately, (3) correctly servicing thousands of orders per minute and (4) broadcasting saids trades and other metadata to public feeds in a timely manner were especially impressive.

PS. I also found it particularly thoughtful of Jane Street to include only students that have never participated in previous iterations of their ETC before - they wanted a level playing field and a better experience for everyone there!
