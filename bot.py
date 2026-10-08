# bot.py — rule-based Snake bot: greedy toward food, with flood-fill and
# tail-reachability checks so it doesn't trap itself.

import collections

from snake import run_episode

DIRECTIONS = ["UP", "DOWN", "LEFT", "RIGHT"]
DIR_VEC = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}

class SnakeBot:
    def __init__(self):
        pass

    def next_move(self, state):
        head = state["snake"][0]
        food = state["food"]
        direction = state["direction"]

        options = self.get_safe_moves(state)
        if not options:
            return direction

        best_move = direction
        best_score = -float("inf")

        for move in options:
            dx, dy = DIR_VEC[move]
            new_head = (head[0] + dx, head[1] + dy)
            dist_to_food = abs(new_head[0] - food[0]) + abs(new_head[1] - food[1])
            space_score = self.flood_fill(new_head, state)
            tail_safe = self.reaches_tail(new_head, state)

            score = -dist_to_food + 0.2 * space_score + (100 if tail_safe else -100)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def get_safe_moves(self, state):
        head = state["snake"][0]
        body = state["snake"]
        board_w = state["board_width"]
        board_h = state["board_height"]
        direction = state["direction"]

        safe = []
        for move in DIRECTIONS:
            if move == OPPOSITE[direction]:
                continue
            dx, dy = DIR_VEC[move]
            nx, ny = head[0] + dx, head[1] + dy
            if (0 <= nx < board_w and 0 <= ny < board_h and (nx, ny) not in body):
                safe.append(move)
        return safe

    def flood_fill(self, start, state):
        board_w, board_h = state["board_width"], state["board_height"]
        snake = set(state["snake"])
        visited = set()
        q = collections.deque([start])
        count = 0

        while q and count < 100:
            x, y = q.popleft()
            if (x, y) in visited or (x, y) in snake:
                continue
            visited.add((x, y))
            count += 1
            for dx, dy in DIR_VEC.values():
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_w and 0 <= ny < board_h:
                    q.append((nx, ny))
        return count

    def reaches_tail(self, start, state):
        snake = list(state["snake"])
        tail = snake[-1]
        body = set(snake[:-1])
        board_w, board_h = state["board_width"], state["board_height"]
        visited = set()
        q = collections.deque([start])

        while q:
            x, y = q.popleft()
            if (x, y) == tail:
                return True
            if (x, y) in visited or (x, y) in body:
                continue
            visited.add((x, y))
            for dx, dy in DIR_VEC.values():
                nx, ny = x + dx, y + dy
                if 0 <= nx < board_w and 0 <= ny < board_h:
                    q.append((nx, ny))
        return False

if __name__ == "__main__":
    scores = []
    for i in range(200):
        bot = SnakeBot()
        score = run_episode(bot)["score"]
        scores.append(score)
        print(f"Run {i+1}: Score = {score}")
    print(f"\nAverage Score: {sum(scores)/len(scores):.2f}")
    print(f"Highest Score: {max(scores)}")
