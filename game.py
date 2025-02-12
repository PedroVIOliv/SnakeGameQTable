import random
import pygame

class SnakeGame:
    '''
    Implementation of the Snake game logic, primarily for reinforcement learning,
    but also supporting human playability and rendering.
    '''
    def __init__(self, grid_size=10, block_size=20, speed=10, human=False):
        self.grid_size = grid_size
        self.block_size = block_size
        self.speed = speed
        self.human = human
        self.window = None
        self.clock = None
        self.reset()

    def reset(self):
        # Initialize the snake in the middle of the grid
        self.snake = [(self.grid_size // 2, self.grid_size // 2)]
        self.direction = (0, -1)  # initial direction: up
        self.place_food()
        self.score = 0
        return self.get_state()
    
    def place_food(self):
        # Randomly place the food on the grid, ensuring it does not overlap with the snake.
        while True:
            self.food = (random.randint(0, self.grid_size - 1),
                         random.randint(0, self.grid_size - 1))
            if self.food not in self.snake:
                break

    def get_state(self):
        # Return the current state of the game: 0 for empty cells, 1 for snake, 2 for food.
        state = [[0] * self.grid_size for _ in range(self.grid_size)]
        for x, y in self.snake:
            state[x][y] = 1
        state[self.food[0]][self.food[1]] = 2
        return state
    
    def step(self, action):
        has_eaten = False
        new_direction = {
            0: (0, -1),  # up
            1: (1, 0),   # right
            2: (0, 1),   # down
            3: (-1, 0)   # left
        }.get(action, self.direction)
        self.direction = new_direction
        
        next_position = (self.snake[0][0] + self.direction[0],
                         self.snake[0][1] + self.direction[1])
        
        # Check for food consumption:
        if next_position == self.food:
            has_eaten = True
            self.snake.insert(0, next_position)
            self.place_food()
            self.score += 1
        else:
            # Move the snake: add new head and remove tail.
            self.snake.insert(0, next_position)
            self.snake.pop()

        # Check for collisions (self or wall):
        if (next_position in self.snake[1:] or
            next_position[0] < 0 or next_position[0] >= self.grid_size or
            next_position[1] < 0 or next_position[1] >= self.grid_size):
            return self.get_state(), -1, True
        
        return self.get_state(), 1 if has_eaten else 0, False
    
    def render(self):
        # Initialize pygame window and clock if not already set up.
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode(
                (self.grid_size * self.block_size, self.grid_size * self.block_size))
            self.clock = pygame.time.Clock()
        
        self.window.fill((0, 0, 0))
        # Draw the snake.
        for x, y in self.snake:
            pygame.draw.rect(
                self.window, (0, 255, 0),
                (x * self.block_size, y * self.block_size, self.block_size, self.block_size)
            )
        # Draw the food.
        pygame.draw.rect(
            self.window, (255, 0, 0),
            (self.food[0] * self.block_size, self.food[1] * self.block_size, self.block_size, self.block_size)
        )
        pygame.display.flip()
        self.clock.tick(self.speed)
        
        # Handle quit events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.window = None
                break
        
        return self.window
    
    def human_play(self):
        '''Allows a human to play the game using arrow keys.'''
        running = True
        while running:
            action = None
            # Process pygame events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Check for key presses.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                action = 0
            elif keys[pygame.K_RIGHT]:
                action = 1
            elif keys[pygame.K_DOWN]:
                action = 2
            elif keys[pygame.K_LEFT]:
                action = 3

            # If an action was detected, update the game state.
            if action is not None:
                state, reward, done = self.step(action)
                if done:
                    print("Game Over! Final Score:", self.score)
                    running = False

            # Always render the current state.
            self.render()
        self.close()
    
    def close(self):
        if self.window is not None:
            pygame.quit()
            self.window = None
        
    def __del__(self):
        self.close()


# To allow human play, run the game with human=True.
if __name__ == "__main__":
    game = SnakeGame(grid_size=20, block_size=20, speed=10, human=True)
    game.human_play()