import math
import sys
from dataclasses import dataclass

# Navigate the treacherous currents of the Maelstrom! Plunder floating treasure chests,
# manage your ship's cargo inertia, and blast enemy corsairs back into the whirlpool.

MAELSTROM_RADIUS = 380.0
EYE_SAFE_RADIUS = 135.0
PORT_RETURN_CLOSE_DIST = 290.0
FIRE_RANGE = 435.0
SAFE_SELF_BLAST_DIST = 130.0


@dataclass(frozen=True)
class Pos:
    x: int
    y: int

    def distance_to(self, other: "Pos") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class Ship:
    id: int
    owner: int
    pos: Pos
    vx: int
    vy: int
    gold: int
    cooldown: int


@dataclass(frozen=True)
class Chest:
    id: int
    pos: Pos
    gold: int


def maelstrom_current(pos: Pos, maelstrom: Pos, league_level: int) -> tuple[float, float]:
    """Return the rotational swirl + inward pull current vector at `pos` (Wood 2/1 only)."""
    if league_level > 2:
        return 0.0, 0.0
    rx = maelstrom.x - pos.x
    ry = maelstrom.y - pos.y
    r = math.hypot(rx, ry)
    if r <= 1e-3 or r > MAELSTROM_RADIUS:
        return 0.0, 0.0
    urx, ury = rx / r, ry / r
    utx, uty = -ury, urx
    intensity = 1.0 - (r / MAELSTROM_RADIUS)
    swirl = 18.0 + 26.0 * intensity
    pull = 10.0 + 22.0 * intensity
    return utx * swirl + urx * pull, uty * swirl + ury * pull


def pick_chest(ship: Ship, drift_x: float, drift_y: float, chests: list[Chest], claimed: set[int], my_port: Pos, maelstrom: Pos, league_level: int) -> Chest | None:
    best_chest = None
    best_score = -1e9
    for c in chests:
        if c.id in claimed:
            continue
        if league_level <= 2 and c.pos.distance_to(maelstrom) < 100.0:
            continue
        d_ship = math.hypot(c.pos.x - drift_x, c.pos.y - drift_y)
        d_port = c.pos.distance_to(my_port)
        score = c.gold * 180.0 - d_ship - 0.35 * d_port
        if score > best_score:
            best_score = score
            best_chest = c
    return best_chest


def choose_fire_command(
    ship: Ship,
    enemy_ships: list[Ship],
    self_next_x: float,
    self_next_y: float,
    maelstrom: Pos,
    league_level: int,
) -> str:
    if league_level != 1 or ship.cooldown > 0:
        return ""
    for e in enemy_ships:
        ecx, ecy = maelstrom_current(e.pos, maelstrom, league_level)
        px = int(round(e.pos.x + e.vx + ecx))
        py = int(round(e.pos.y + e.vy + ecy))
        if math.hypot(px - ship.pos.x, py - ship.pos.y) <= FIRE_RANGE and math.hypot(px - self_next_x, py - self_next_y) > SAFE_SELF_BLAST_DIST:
            if e.gold > 0 or math.hypot(px - maelstrom.x, py - maelstrom.y) < 200.0:
                return f" FIRE {px} {py} MSG BOOM!"
    return ""


def main() -> None:
    width, height, league_level = [int(i) for i in input().split()]
    my_port_x, my_port_y, opp_port_x, opp_port_y, maelstrom_x, maelstrom_y = [int(i) for i in input().split()]
    my_port = Pos(my_port_x, my_port_y)
    maelstrom = Pos(maelstrom_x, maelstrom_y)

    while True:
        _turn = int(input())
        ship_count = int(input())
        my_ships: list[Ship] = []
        enemy_ships: list[Ship] = []
        for _ in range(ship_count):
            ship_id, owner, x, y, vx, vy, gold, cooldown = [int(j) for j in input().split()]
            s = Ship(ship_id, owner, Pos(x, y), vx, vy, gold, cooldown)
            if owner == 0:
                my_ships.append(s)
            else:
                enemy_ships.append(s)

        chest_count = int(input())
        chests: list[Chest] = []
        for _ in range(chest_count):
            chest_id, cx, cy, chest_gold = [int(j) for j in input().split()]
            chests.append(Chest(chest_id, Pos(cx, cy), chest_gold))

        claimed: set[int] = set()
        for ship in my_ships:
            cx, cy = maelstrom_current(ship.pos, maelstrom, league_level)
            drift_x = ship.pos.x + ship.vx + cx
            drift_y = ship.pos.y + ship.vy + cy

            target = my_port
            dist_to_port = ship.pos.distance_to(my_port)
            return_home = (ship.gold >= 4) or (ship.gold >= 2 and dist_to_port < PORT_RETURN_CLOSE_DIST) or not chests

            if not return_home:
                chosen = pick_chest(ship, drift_x, drift_y, chests, claimed, my_port, maelstrom, league_level)
                if chosen is not None:
                    claimed.add(chosen.id)
                    target = chosen.pos

            err_x = target.x - drift_x
            err_y = target.y - drift_y

            if league_level <= 2:
                pred_eye_dist = math.hypot(drift_x - maelstrom.x, drift_y - maelstrom.y)
                if pred_eye_dist < EYE_SAFE_RADIUS:
                    ux = (drift_x - maelstrom.x) / max(1.0, pred_eye_dist)
                    uy = (drift_y - maelstrom.y) / max(1.0, pred_eye_dist)
                    err_x = ux * 400.0
                    err_y = uy * 400.0

            aim_x = int(round(ship.pos.x + err_x))
            aim_y = int(round(ship.pos.y + err_y))
            mass_factor = 1.0 + 0.15 * ship.gold
            power = min(100, max(10, int(round(math.hypot(err_x, err_y) * mass_factor))))

            err_norm = max(1.0, math.hypot(err_x, err_y))
            self_next_x = drift_x + (err_x / err_norm) * (power / mass_factor)
            self_next_y = drift_y + (err_y / err_norm) * (power / mass_factor)
            fire_cmd = choose_fire_command(ship, enemy_ships, self_next_x, self_next_y, maelstrom, league_level)

            print(f"SAIL {aim_x} {aim_y} {power}{fire_cmd}", flush=True)


if __name__ == "__main__":
    main()
