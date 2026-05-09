# Example Scenario: Designing Test Cases (Step-by-Step)

This example illustrates how you should present the work step-by-step in your report.

## Scenario

> In an online video game, a player wants to unlock a new playable character from the in-game store. Characters come in three rarities: Common, Rare, or Legendary. Common characters can be unlocked by any player. Rare characters require the player to have at least 1000 in-game coins. Legendary characters require BOTH at least 1000 in-game coins AND that the player has reached account level 20. Premium subscribers can always unlock any character without any other requirement.

Design all relevant test cases for this scenario using the test design technique.

---

## Step 1: Identify Actions and Conditions

The scenario contains one action:

> Unlocking the character := [successful; unsuccessful]

The conditions that can affect the outcome of the action are:

1. Character rarity := [Common; Rare; Legendary]
2. In-game coins := [<1000; >=1000]
3. Account level := [<20; >=20]
4. Premium subscription := [yes; no]

## Step 2: Construct Combinations

The four conditions (one with three values and three with two values) produce in total $3 \times 2^3 = 24$ valid combinations.

| ID | Character rarity | In-game coins | Account level | Premium subscription |
|---|---|---|---|---|
| 1 | Common | <1000 | <20 | No |
| 2 | Common | <1000 | <20 | Yes |
| 3 | Common | <1000 | >=20 | No |
| 4 | Common | <1000 | >=20 | Yes |
| 5 | Common | >=1000 | <20 | No |
| 6 | Common | >=1000 | <20 | Yes |
| 7 | Common | >=1000 | >=20 | No |
| 8 | Common | >=1000 | >=20 | Yes |
| 9 | Rare | <1000 | <20 | No |
| 10 | Rare | <1000 | <20 | Yes |
| 11 | Rare | <1000 | >=20 | No |
| 12 | Rare | <1000 | >=20 | Yes |
| 13 | Rare | >=1000 | <20 | No |
| 14 | Rare | >=1000 | <20 | Yes |
| 15 | Rare | >=1000 | >=20 | No |
| 16 | Rare | >=1000 | >=20 | Yes |
| 17 | Legendary | <1000 | <20 | No |
| 18 | Legendary | <1000 | <20 | Yes |
| 19 | Legendary | <1000 | >=20 | No |
| 20 | Legendary | <1000 | >=20 | Yes |
| 21 | Legendary | >=1000 | <20 | No |
| 22 | Legendary | >=1000 | <20 | Yes |
| 23 | Legendary | >=1000 | >=20 | No |
| 24 | Legendary | >=1000 | >=20 | Yes |

## Step 3: Denote Expected Outcome

Reading the scenario, the expected outcome of *unlocking the character* is successful if at least one of the following holds: the player has a Premium subscription; or the character is Common; or the character is Rare and the player has at least 1000 coins; or the character is Legendary and the player has at least 1000 coins and is at least account level 20. Otherwise, the action is unsuccessful.

Filling in the expected outcome for each of the 24 combinations gives the following:

| ID | Character rarity | In-game coins | Account level | Premium subscription | Unlocking the character |
|---|---|---|---|---|---|
| 1 | Common | <1000 | <20 | No | Successful |
| 2 | Common | <1000 | <20 | Yes | Successful |
| 3 | Common | <1000 | >=20 | No | Successful |
| 4 | Common | <1000 | >=20 | Yes | Successful |
| 5 | Common | >=1000 | <20 | No | Successful |
| 6 | Common | >=1000 | <20 | Yes | Successful |
| 7 | Common | >=1000 | >=20 | No | Successful |
| 8 | Common | >=1000 | >=20 | Yes | Successful |
| 9 | Rare | <1000 | <20 | No | Unsuccessful |
| 10 | Rare | <1000 | <20 | Yes | Successful |
| 11 | Rare | <1000 | >=20 | No | Unsuccessful |
| 12 | Rare | <1000 | >=20 | Yes | Successful |
| 13 | Rare | >=1000 | <20 | No | Successful |
| 14 | Rare | >=1000 | <20 | Yes | Successful |
| 15 | Rare | >=1000 | >=20 | No | Successful |
| 16 | Rare | >=1000 | >=20 | Yes | Successful |
| 17 | Legendary | <1000 | <20 | No | Unsuccessful |
| 18 | Legendary | <1000 | <20 | Yes | Successful |
| 19 | Legendary | <1000 | >=20 | No | Unsuccessful |
| 20 | Legendary | <1000 | >=20 | Yes | Successful |
| 21 | Legendary | >=1000 | <20 | No | Unsuccessful |
| 22 | Legendary | >=1000 | <20 | Yes | Successful |
| 23 | Legendary | >=1000 | >=20 | No | Successful |
| 24 | Legendary | >=1000 | >=20 | Yes | Successful |

## Step 4: Collapse to the Relevant Test Cases

Several rows lead to the same outcome regardless of the value of one or more conditions. Collapsing those rows (using `-` to denote any value of the condition) yields the final, optimized set of relevant test cases:

| ID | Character rarity | In-game coins | Account level | Premium subscription | Unlocking the character |
|---|---|---|---|---|---|
| 1 | - | - | - | Yes | Successful |
| 2 | Common | - | - | No | Successful |
| 3 | Rare | >=1000 | - | No | Successful |
| 4 | Rare | <1000 | - | No | Unsuccessful |
| 5 | Legendary | >=1000 | >=20 | No | Successful |
| 6 | Legendary | >=1000 | <20 | No | Unsuccessful |
| 7 | Legendary | <1000 | - | No | Unsuccessful |

How the collapse was derived:

1. Row 1 captures the rule that a Premium subscription always succeeds, so the other three conditions become irrelevant. This single row replaces all twelve rows in Step 3 where Premium = Yes.
2. Row 2 captures that for non-premium players, Common characters always succeed, so coins and level become irrelevant. This replaces the four Common + Premium = No rows.
3. Row 3 captures that Rare characters succeed for non-premium players when the player has at least 1000 coins. Account level is irrelevant for Rare characters, so this single row covers two Step 3 rows.
4. Row 4 captures that Rare characters fail for non-premium players when the player has fewer than 1000 coins, again with account level irrelevant.
5. Row 5 captures the only Legendary success path for non-premium players: at least 1000 coins AND account level 20 or above.
6. Row 6 separates the case where a non-premium player has enough coins for a Legendary character but is below level 20, which leads to failure.
7. Row 7 captures that for Legendary characters, having fewer than 1000 coins fails regardless of account level (the level becomes irrelevant once the coin requirement is unmet).

This collapsed table is the deliverable of the test design technique for this scenario, containing exactly the relevant test cases to implement.
