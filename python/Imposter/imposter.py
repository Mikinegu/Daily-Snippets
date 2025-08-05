import random
import time
import os

class ImposterGame:
    def __init__(self):
        self.players = []
        self.imposter = None
        self.votes = {}
        self.game_over = False
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def add_players(self):
        print("=== IMPOSTER GAME ===")
        print("Enter player names (type 'done' when finished):")
        
        while True:
            name = input(f"Player {len(self.players) + 1}: ").strip()
            if name.lower() == 'done':
                if len(self.players) < 3:
                    print("You need at least 3 players to start!")
                    continue
                break
            if name and name not in self.players:
                self.players.append(name)
            elif name in self.players:
                print("That name is already taken!")
                
        print(f"\nPlayers: {', '.join(self.players)}")
        
    def assign_roles(self):
        self.imposter = random.choice(self.players)
        
        print("\n=== ROLES ASSIGNED ===")
        print("Check your role secretly!")
        
        for player in self.players:
            input(f"\n{player}, press Enter to see your role...")
            self.clear_screen()
            
            if player == self.imposter:
                print(f"🎭 {player}, you are the IMPOSTER!")
                print("Your goal: Blend in and avoid being voted out!")
            else:
                print(f"👨‍🚀 {player}, you are a CREW MEMBER!")
                print("Your goal: Find the imposter!")
                
            input("Press Enter to continue...")
            self.clear_screen()
            
    def voting_phase(self):
        print("=== VOTING PHASE ===")
        print("Discuss and vote for who you think is the imposter!")
        print("Players:", ', '.join(self.players))
        
        self.votes = {}
        
        for player in self.players:
            input(f"\n{player}, press Enter to vote...")
            self.clear_screen()
            
            print(f"{player}, who do you think is the imposter?")
            for i, candidate in enumerate(self.players, 1):
                print(f"{i}. {candidate}")
                
            while True:
                try:
                    choice = int(input("Enter your choice (number): ")) - 1
                    if 0 <= choice < len(self.players):
                        voted_player = self.players[choice]
                        self.votes[voted_player] = self.votes.get(voted_player, 0) + 1
                        print(f"You voted for {voted_player}")
                        break
                    else:
                        print("Invalid choice! Try again.")
                except ValueError:
                    print("Please enter a valid number!")
                    
            input("Press Enter to continue...")
            self.clear_screen()
            
    def count_votes(self):
        print("=== VOTE RESULTS ===")
        
        for player, votes in self.votes.items():
            print(f"{player}: {votes} votes")
            
        max_votes = max(self.votes.values())
        eliminated = [player for player, votes in self.votes.items() if votes == max_votes]
        
        if len(eliminated) > 1:
            print(f"\nTie! {', '.join(eliminated)} received the most votes.")
            print("No one is eliminated this round!")
            return None
        else:
            eliminated_player = eliminated[0]
            print(f"\n{eliminated_player} has been eliminated!")
            return eliminated_player
            
    def check_win_condition(self, eliminated_player):
        if eliminated_player == self.imposter:
            print("\n🎉 CREW MEMBERS WIN! 🎉")
            print(f"The imposter {self.imposter} has been caught!")
            self.game_over = True
            return True
        else:
            self.players.remove(eliminated_player)
            if len(self.players) <= 2:
                print("\n💀 IMPOSTER WINS! 💀")
                print(f"The imposter {self.imposter} has eliminated all crew members!")
                self.game_over = True
                return True
            else:
                print(f"\n{len(self.players)} players remaining...")
                return False
                
    def play_game(self):
        self.add_players()
        self.assign_roles()
        
        round_num = 1
        
        while not self.game_over:
            print(f"\n=== ROUND {round_num} ===")
            print(f"Players remaining: {', '.join(self.players)}")
            
            print("\nPlayers are completing tasks and investigating...")
            time.sleep(2)
            
            self.voting_phase()
            eliminated = self.count_votes()
            
            if eliminated:
                self.check_win_condition(eliminated)
                
            round_num += 1
            
            if not self.game_over:
                input("\nPress Enter to continue to next round...")
                self.clear_screen()
                
        print("\n=== GAME OVER ===")
        print("Thanks for playing Imposter Game!")

def main():
    while True:
        game = ImposterGame()
        game.play_game()
        
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
