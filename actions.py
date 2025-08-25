from pydantic import BaseModel
from typing import Literal


class BaseAdminAction(BaseModel):
    user_id: str

    class Config:
        extra = "ignore"  

    async def get_user(self, user_id: str):
        for user in users:
            if user["user_id"] == user_id:
                return user
        return None

class KillAction(BaseAdminAction):
    action: str = Literal["kill"] 

    async def execute(self):
        user = await self.get_user(self.user_id)
        if user:
            user["alive"] = False
            print(f"[DEBUG] Убит игрок {self.user_id}")


class RevealAction(BaseAdminAction):
    action: str = Literal["reveal"]
    user_id : str
    stat: str

    async def execute(self):
        user = await self.get_user(self.user_id)
        if user:
            for room in rooms:
                if user["room_id"] == room["room_id"]:
                    for card in room["cards"]:
                        if card["card_owner"] == user["user_id"]:
                            card["card"][self.stat]["revealed"] = True
                            print(f"[DEBUG] Открыта характеристика {card["card"][self.stat]} для {self.user_id}")


class SwapAction(BaseAdminAction):
    action: str = Literal["swap"]
    stat: str
    target_user_id : str

    async def execute(self):
        user = await self.get_user(self.user_id)
        target_user = await self.get_user(self.target_user_id)
        if user:
            for room in rooms:
                if user["room_id"] == room["room_id"] and target_user["room_id"] == room["room_id"]:
                    user_card = next(card for card in room["cards"] if card ["card_owner"] == user["user_id"])
                    target_user_card = next(card for card in room["cards"] if card ["card_owner"] == target_user["user_id"])
                    user_value = user_card["card"][self.stat]
                    target_value = target_user_card["card"][self.stat]
                    user_card["card"][self.stat], target_user_card["card"][self.stat] = target_value, user_value

                    print(f"[DEBUG] Поменян параметр {self.stat} между карточками {user_card["card_id"]}{target_user_card["card_id"]}")

