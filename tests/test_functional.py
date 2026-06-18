import requests

BASE_URL = "http://localhost:8080"


def test_player_buy_spaceship():
    response = requests.post(f"{BASE_URL}/player/new/toto")
    assert response.status_code == 200
    playerKey = response.json()["key"]
    playerId = response.json()["playerId"]
    print(playerKey)

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    totoMoney = allPlayer.json()[f"{playerId}"]["money"]
    assert totoMoney == 72000.0

    stations = allPlayer.json()[f"{playerId}"]["stations"]
    totoStationId = next(iter(stations))

    ships = requests.get(
        f"{BASE_URL}/station/{totoStationId}/shipyard/list",
        headers={"Simeis-Key": playerKey},
    ).json()["ships"]
    firstShipId = ships[0]["id"]
    buySpaceshipResponse = requests.post(
        f"{BASE_URL}/station/{totoStationId}/shipyard/buy/{firstShipId}",
        headers={"Simeis-Key": playerKey},
    )
    assert buySpaceshipResponse.status_code == 200

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    totoMoney = allPlayer.json()[f"{playerId}"]["money"]
    assert totoMoney == 7000.0


def test_player_buy_ship_upgrade():
    response = requests.post(f"{BASE_URL}/player/new/titi")
    assert response.status_code == 200
    playerKey = response.json()["key"]
    playerId = response.json()["playerId"]

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    stations = allPlayer.json()[f"{playerId}"]["stations"]
    titiStationId = next(iter(stations))

    ships = requests.get(
        f"{BASE_URL}/station/{titiStationId}/shipyard/list",
        headers={"Simeis-Key": playerKey},
    ).json()["ships"]
    firstShipId = ships[0]["id"]
    buySpaceshipResponse = requests.post(
        f"{BASE_URL}/station/{titiStationId}/shipyard/buy/{firstShipId}",
        headers={"Simeis-Key": playerKey},
    )
    assert buySpaceshipResponse.status_code == 200

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    titiMoneyBefore = allPlayer.json()[f"{playerId}"]["money"]

    shipBefore = requests.get(
        f"{BASE_URL}/ship/{firstShipId}", headers={"Simeis-Key": playerKey}
    ).json()
    cargoCapacityBefore = shipBefore["cargo"]["capacity"]

    buyUpgradeResponse = requests.post(
        f"{BASE_URL}/station/{titiStationId}/shipyard/upgrade/{firstShipId}/CargoExpansion",
        headers={"Simeis-Key": playerKey},
    )
    assert buyUpgradeResponse.status_code == 200
    assert buyUpgradeResponse.json()["cost"] == 2400.0

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    titiMoneyAfter = allPlayer.json()[f"{playerId}"]["money"]
    assert titiMoneyAfter == titiMoneyBefore - 2400.0

    shipAfter = requests.get(
        f"{BASE_URL}/ship/{firstShipId}", headers={"Simeis-Key": playerKey}
    ).json()
    cargoCapacityAfter = shipAfter["cargo"]["capacity"]
    assert cargoCapacityAfter == cargoCapacityBefore + 120.0


def test_player_buy_heavy_ship_not_enough_money():
    response = requests.post(f"{BASE_URL}/player/new/tata")
    assert response.status_code == 200
    playerKey = response.json()["key"]
    playerId = response.json()["playerId"]

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    tataMoneyBefore = allPlayer.json()[f"{playerId}"]["money"]
    assert tataMoneyBefore == 72000.0

    stations = allPlayer.json()[f"{playerId}"]["stations"]
    tataStationId = next(iter(stations))

    ships = requests.get(
        f"{BASE_URL}/station/{tataStationId}/shipyard/list",
        headers={"Simeis-Key": playerKey},
    ).json()["ships"]
    heavyShip = next(
        ship
        for ship in ships
        if ship["reactor_power"] == 10 and ship["cargo_capacity"] == 1200.0
    )
    assert heavyShip["price"] > tataMoneyBefore

    buySpaceshipResponse = requests.post(
        f"{BASE_URL}/station/{tataStationId}/shipyard/buy/{heavyShip['id']}",
        headers={"Simeis-Key": playerKey},
    )
    assert buySpaceshipResponse.status_code == 200
    assert buySpaceshipResponse.json()["type"].startswith("NotEnoughMoney")

    allPlayer = requests.get(f"{BASE_URL}/gamestats")
    tataMoneyAfter = allPlayer.json()[f"{playerId}"]["money"]
    assert tataMoneyAfter == tataMoneyBefore

    tataPlayer = requests.get(
        f"{BASE_URL}/player/{playerId}", headers={"Simeis-Key": playerKey}
    ).json()
    assert tataPlayer["ships"] == []
