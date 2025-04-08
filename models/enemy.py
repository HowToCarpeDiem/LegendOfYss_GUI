class Enemy:
    def __init__(self, name, health, attack, gold_reward, exp_reward, loot, initiative, armor):
        self.name = name
        self.health = health
        self.attack = attack
        self.gold_reward = gold_reward
        self.exp_reward = exp_reward
        self.loot = loot
        self.initiative = initiative
        self.armor = armor
        
    def is_alive(self):
        return self.health > 0