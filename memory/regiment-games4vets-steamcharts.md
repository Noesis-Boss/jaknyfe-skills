---
name: regiment-games4vets-steamcharts
description: SteamCharts player counts (current, 24h peak, all-time peak) for all 39 REGIMENT Games4Vets titles, captured 2026-07-31.
type: research
---

# Games4Vets — SteamCharts Player Data

Source: https://steamcharts.com (per-game pages) + Steam Web API (`ISteamUserStats/GetNumberOfCurrentPlayers`) + Wayback Machine. Captured 2026-07-31 ~17:00 Phoenix (2026-08-01 00:00 UTC).

| # | Game | Current | 24h Peak | All-Time Peak |
|---|------|---------|----------|---------------|
| 1 | Gray Zone Warfare | 2,895 | 3,472 | 71,503 |
| 2 | Sea of Thieves | 4,724 | 6,911 | 66,632 |
| 3 | Off The Grid | 8,255 | 10,795 | 15,247 |
| 4 | Kingdom Come: Deliverance | 2,924 | 4,481 | 95,863 |
| 5 | Kingdom Come: Deliverance 2 | 9,700 | 18,064 | 255,607 |
| 6 | Metalstorm | N/A | N/A | N/A |
| 7 | FragPunk | 938 | 1,174 | 113,243 |
| 8 | RAID: Shadow Legends | 825 | 1,288 | 1,892 |
| 9 | Squad | 13,195 | 16,412 | 38,573 |
| 10 | LOCKDOWN Protocol | 308 | 374 | 9,318 |
| 11 | Ready or Not | 6,431 | 9,305 | 55,174 |
| 12 | Two Falls (Outamanecka) | 0 | N/A | N/A |
| 13 | Bug Alliance | 1 | N/A | N/A |
| 14 | Goblintown: Really Hard Driving Game | 0 | N/A | N/A |
| 15 | Echoes of Elysium | 4 | 7 | 376 |
| 16 | Jump Space | 694 | 906 | 21,933 |
| 17 | World of Warships | 5,209 | 11,655 | 400,538 |
| 18 | POLYGON | 80 | 148 | 1,208 |
| 19 | Incursion Red River | 285 | 379 | 2,365 |
| 20 | Bellum | — | — | — |
| 21 | Don't Lose Aggro | 0 | N/A | N/A |
| 22 | Last Flag | 3 | N/A | N/A |
| 23 | Responding | 3 | 6 | 56 |
| 24 | Cool Story Bro | 0 | N/A | N/A |
| 25 | Maki's Adventure | 0 | N/A | N/A |
| 26 | Paddle Paddle Paddle | 24 | 50 | 385 |
| 27 | Riftwalker | N/A | N/A | N/A |
| 28 | Wildgate | 7 | N/A | 7,776* |
| 29 | Sunderfolk | 88 | 129 | 1,390 |
| 30 | Mechabellum | 1,108 | 1,623 | 7,740 |
| 31 | Lynked: Banner of the Spark | 5 | 6 | 289 |
| 32 | Deadhaus Sonata | 2 | 2 | 10 |
| 33 | The Caribou Trail | 11 | 13 | 215 |
| 34 | Space Aces | 219 | 488 | 877 |
| 35 | Arma Reforger | 14,700 | 17,825 | 24,632 |
| 36 | NBA 2K26 | 11,728 | 32,105 | 52,826 |
| 37 | PGA TOUR 2K25 | 1,661 | 2,106 | 6,619 |
| 38 | Infinity Rising | N/A | N/A | N/A |
| 39 | Borderlands 4 | 4,852 | 5,829 | 302,421 |

\* Wildgate all-time peak is from a Wayback Machine capture of the SteamCharts page (2026-01-02), not live SteamCharts data.

## Notes

- **N/A = not tracked by SteamCharts** (their `/app/<id>` pages return HTTP 500 for these apps; no data exists). Current players came from the Steam Web API where available.
- **Not on Steam:** Bellum (own launcher, pre-order tactical shooter at playbellum.com), Metalstorm (Steam app 2453200 returns no stats — result 42), Riftwalker (app 4109980, no stats), Infinity Rising (app 4022970, no stats).
- SteamDB was IP-banned during this lookup, so it could not be used as a fallback.
- Resolved Steam app IDs: Sea of Thieves 1172620 (2025 Edition), Off The Grid 3659280, Jump Space 1757300, Two Falls 1671740, Last Flag 2721340, NBA 2K26 3472040, PGA TOUR 2K25 2385530, Borderlands 4 1285190.
