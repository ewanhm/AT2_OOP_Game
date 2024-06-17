from character import Character

class Healthbar:

    def __init__(self, character):
        self.character = character
        self.max_hit_points = character.hit_points
        self.current_hit_points = character.hit_points

    def update(self):
        self.current_hit_points = self.character.hit_points

    def display(self):
        health_ratio = self.current_hit_points / self.max_hit_points
        bar_length = 10
        filled_length = int(bar_length * health_ratio)
        bar = '█' * filled_length + '-' * (bar_length - filled_length) #Temporary text representation of healthbar
        print(f"{self.character.name}'s Health: [{bar}] {self.current_hit_points}/{self.max_hit_points}")

    def take_damage(self, amount):
        self.character.take_damage(amount)
        self.update()
        self.display()

if __name__ == "__main__":
    character = Character("Test", "Warrior", 0) #Test character
    health_bar = Healthbar(character)

    health_bar.take_damage(3)
    
