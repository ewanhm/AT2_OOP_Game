from character import Character

class Rogue(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Rogue", armour = 7)
        # Additional attributes and methods specific to the Rogue class
        self.max_stamina = 100
        self.current_stamina = self.max_stamina
        self.stamina_regeneration = 10
        self.strength = 15
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Basic Attack": {"method": self.basic_attack, "stamina_cost": 10},
            "Shurikens": {"method": self.shurikens, "stamina_cost": 15},
            "Shadow Sneak": {"method": self.shadow_sneak, "stamina_cost": 30},
            "Sharpen Daggers": {"method": self.sharpen_daggers, "stamina_cost": 5}

        }

    def basic_attack(self, target):
        pass

    def shurikens(self, targets):
        pass

    def shadow_sneak(self, target):
        pass

    def sharpen_daggers(self):
        pass