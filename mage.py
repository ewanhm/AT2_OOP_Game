from character import Character

class Mage(Character):
    def __init__(self, name, max_hp):
        """
        Initialise a Mage character with specified name and maximum HP.
        """
        super().__init__(name, "Mage", armor=5)  # Initialise parent Character class with mage-specific attributes
        self.max_mana = 100  # Set the maximum amount of mana
        self.current_mana = self.max_mana  # Initialise current mana to the maximum
        self.mana_regeneration = 10  # Rate at which mana regenerates (not used in this code)
        self.magic_power = 20  # Base magic power for the mage
        self.max_hp = max_hp  # Set the maximum HP for the mage
        self.current_hp = max_hp  # Initialise current HP to the maximum
        self.attacks = {  # Dictionary of mage's attacks with method references and mana costs
            "Fireball": {"method": self.fireball, "mana_cost": 20},
            "Ice Bolt": {"method": self.ice_bolt, "mana_cost": 15},
            "Lightning Strike": {"method": self.lightning_strike, "mana_cost": 30},
            "Mana Shield": {"method": self.mana_shield, "mana_cost": 10}
        }

    def fireball(self, target):
        """
        Perform a Fireball attack on the target if sufficient mana is available.
        """
        if self.current_mana >= 20:  # Check if enough mana is available
            damage = self.magic_power * 1.5  # Calculate damage
            print(f"{self.name} casts Fireball on {target.name} for {damage} damage!")
            target.take_damage(damage)  # Apply damage to the target
            self.current_mana -= 20  # Deduct mana cost
        else:
            print("Not enough mana for Fireball.")

    def ice_bolt(self, target):
        """
        Perform an Ice Bolt attack on the target if sufficient mana is available.
        """
        if self.current_mana >= 15:  # Check if enough mana is available
            damage = self.magic_power  # Calculate damage
            print(f"{self.name} casts Ice Bolt on {target.name} for {damage} damage!")
            target.take_damage(damage)  # Apply damage to the target
            self.current_mana -= 15  # Deduct mana cost
        else:
            print("Not enough mana for Ice Bolt.")

    def lightning_strike(self, target):
        """
        Perform a Lightning Strike attack on the target if sufficient mana is available.
        """
        if self.current_mana >= 30:  # Check if enough mana is available
            damage = self.magic_power * 2  # Calculate damage
            print(f"{self.name} casts Lightning Strike on {target.name} for {damage} damage!")
            target.take_damage(damage)  # Apply damage to the target
            self.current_mana -= 30  # Deduct mana cost
        else:
            print("Not enough mana for Lightning Strike.")

    def mana_shield(self):
        """
        Cast a Mana Shield to increase the mage's armour if sufficient mana is available.
        """
        if self.current_mana >= 10:  # Check if enough mana is available
            self.armor += 10  # Increase the mage's armour
            print(f"{self.name} casts Mana Shield, increasing armour to {self.armor}!")
            self.current_mana -= 10  # Deduct mana cost
        else:
            print("Not enough mana for Mana Shield.")
