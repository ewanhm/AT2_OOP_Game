from character import Character

class Rogue(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Rogue", armor=7)
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 12
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Shurikens": {"method": self.shurikens, "stamina_cost": 15},
            "Shadow Sneak": {"method": self.shadow_sneak, "stamina_cost": 30},
            "Sharpen Daggers": {"method": self.sharpen_daggers, "stamina_cost": 5}
        }

    def basic_attack(self, target):
        damage = self.strength
        print(f"{self.name} performs a basic attack on {target.name} for {damage} damage!")
        target.take_damage(damage)

    def shurikens(self, targets):
        total_damage = 0
        for target in targets:
            damage = self.strength * 1.5  # Example: Shurikens deal 1.5 times the rogue's strength
            total_damage += damage
            print(f"{self.name} throws shurikens at {target.name} for {damage} damage!")
            target.take_damage(damage)
        print(f"{self.name} dealt a total of {total_damage} damage with shurikens!")

    def shadow_sneak(self, target):
        if self.current_stamina >= 30:
            damage = self.strength * 2  # Example: Shadow Sneak deals double the rogue's strength
            print(f"{self.name} sneaks up on {target.name} and deals {damage} damage!")
            target.take_damage(damage)
            self.current_stamina -= 30
        else:
            print("Not enough stamina for Shadow Sneak.")

    def sharpen_daggers(self):
        self.strength += 5  # Example: Sharpen Daggers increases the rogue's strength
        print(f"{self.name} sharpens their daggers, increasing strength to {self.strength}!")
