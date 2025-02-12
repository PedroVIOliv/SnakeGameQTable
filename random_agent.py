# random_agent.py
import random
import pygame
from game import SnakeGame  # Make sure snake_game.py is in the same directory

def main():
    # Create a game instance with rendering enabled.
    # Set human=False since we are using an agent.
    game = SnakeGame(grid_size=20, block_size=20, speed=10, human=False, render=True)
    game.reset()
    
    done = False
    while not done:
        # Choose a random action: 0 = up, 1 = right, 2 = down, 3 = left.
        action = random.choice([0, 1, 2, 3])
        state, reward, done = game.step(action)
        
        # Render the game to visualize the snake's progress.
        game.render()
        pygame.event.pump()
        
        # Optionally, you can slow down the loop if needed.
        # pygame.time.wait(100)  # Wait for 100 milliseconds

    print("Game Over! Final Score:", game.score)
    game.close()
    pygame.quit()

if __name__ == "__main__":
    main()