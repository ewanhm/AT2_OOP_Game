from character import Character

class Mage(Character):
    def __init__(self, name, max_hp):
        super().__init__(name, "Mage", armor=5)
        self.max_mana = 100
        self.current_mana = self.max_mana
        self.mana_regeneration = 10
        self.magic_power = 20
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attacks = {
            "Fireball": {"method": self.fireball, "mana_cost": 20},
            "Ice Bolt": {"method": self.ice_bolt, "mana_cost": 15},
            "Lightning Strike": {"method": self.lightning_strike, "mana_cost": 30},
            "Mana Shield": {"method": self.mana_shield, "mana_cost": 10}
        }

    def fireball(self, target):
        if self.current_mana >= 20:
            damage = self.magic_power * 1.5
            print(f"{self.name} casts Fireball on {target.name} for {damage} damage!")
            target.take_damage(damage)
            self.current_mana -= 20
        else:
            print("Not enough mana for Fireball.")

    def ice_bolt(self, target):
        if self.current_mana >= 15:
            damage = self.magic_power
            print(f"{self.name} casts Ice Bolt on {target.name} for {damage} damage!")
            target.take_damage(damage)
            self.current_mana -= 15
        else:
            print("Not enough mana for Ice Bolt.")

    def lightning_strike(self, target):
        if self.current_mana >= 30:
            damage = self.magic_power * 2
            print(f"{self.name} casts Lightning Strike on {target.name} for {damage} damage!")
            target.take_damage(damage)
            self.current_mana -= 30
        else:
            print("Not enough mana for Lightning Strike.")

    def mana_shield(self):
        if self.current_mana >= 10:
            self.armor += 10  # Example: Mana Shield increases mage's armor
            print(f"{self.name} casts Mana Shield, increasing armor to {self.armor}!")
            self.current_mana -= 10
        else:
            print("Not enough mana for Mana Shield.")
