import random
import pygame

class SnakeGame:
    '''
    Implementation of the Snake game logic, supporting both RL and human play.
    '''
    def __init__(self, grid_size=10, block_size=20, speed=10, human=False, render=False):
        self.grid_size = grid_size
        self.block_size = block_size
        self.speed = speed
        self.human = human  # if True, assume a human will play and require rendering.
        self.shouldRender = human or render
        self.window = None
        self.clock = None
        self.reset()

    def reset(self):
        # Initialize the snake in the middle of the grid.
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (0, -1)  # initial direction: up
        self.place_food()
        self.score = 0
        return self.get_state()

    def place_food(self):
        # Randomly place the food on the grid ensuring it doesn't overlap with the snake.
        while True:
            self.food = (random.randint(0, self.grid_size - 1),
                         random.randint(0, self.grid_size - 1))
            if self.food not in self.snake:
                break

    def get_state(self):
        # Return a representation of the game state.
        state = [[0] * self.grid_size for _ in range(self.grid_size)]
        for x, y in self.snake:
            state[x][y] = 1
        state[self.food[0]][self.food[1]] = 2
        return state
    
    def step(self, action):
        # Determine the new direction from the action.
        new_direction = {
            0: (0, -1),  # up
            1: (1, 0),   # right
            2: (0, 1),   # down
            3: (-1, 0)   # left
        }.get(action, self.direction)
        self.direction = new_direction

        # Calculate the next head position.
        next_position = (self.snake[0][0] + self.direction[0],
                        self.snake[0][1] + self.direction[1])
        
        # Check for collisions before updating the snake.
        if (next_position in self.snake or
            next_position[0] < 0 or next_position[0] >= self.grid_size or
            next_position[1] < 0 or next_position[1] >= self.grid_size):
            return self.get_state(), -100, True

        # Update the snake and the game state.
        if next_position == self.food:
            self.snake.insert(0, next_position)
            self.place_food()
            self.score += 1
            reward = 1
        else:
            self.snake.insert(0, next_position)
            self.snake.pop()
            reward = -1

        return self.get_state(), reward, False

    def render(self):
        # Initialize the pygame window and clock if needed.
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode(
                (self.grid_size * self.block_size, self.grid_size * self.block_size))
            self.clock = pygame.time.Clock()

        # Draw the game elements.
        self.window.fill((0, 0, 0))
        for x, y in self.snake:
            pygame.draw.rect(
                self.window, (0, 255, 0),
                (x * self.block_size, y * self.block_size, self.block_size, self.block_size)
            )
        pygame.draw.rect(
            self.window, (255, 0, 0),
            (self.food[0] * self.block_size, self.food[1] * self.block_size, self.block_size, self.block_size)
        )
        pygame.display.flip()
        self.clock.tick(self.speed)

    def human_play(self):
        '''Allows a human to play the game using arrow keys.'''
        # Ensure pygame and the display are initialized before processing events.
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode(
                (self.grid_size * self.block_size, self.grid_size * self.block_size))
            self.clock = pygame.time.Clock()

        running = True
        while running:
            # Process events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Process key presses.
            keys = pygame.key.get_pressed()
            action = None
            if keys[pygame.K_UP]:
                action = 0
            elif keys[pygame.K_RIGHT]:
                action = 1
            elif keys[pygame.K_DOWN]:
                action = 2
            elif keys[pygame.K_LEFT]:
                action = 3

            # Update game state if an action is detected.
            if action is not None:
                state, reward, done = self.step(action)
                if done:
                    print("Game Over! Final Score:", self.score)
                    running = False
            if self.shouldRender:
                self.render()
        self.close()

    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None

    def __del__(self):
        self.close()

# Example usage:
if __name__ == "__main__":
    # When human=True, the game will render and allow for keyboard input.
    game = SnakeGame(grid_size=20, block_size=20, speed=10, human=True)
    game.human_play()