class Item():
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self):
        return (
            f"{self.name}\n"
            f"=====\n"
            f"{self.description}\n"
            f"Value: {self.value}"
        )


class Gold(Item):
    def __init__(self, amt):
        self.amt = amt
        super().__init__(name="Gold",
                         description=f"a round coin with {self.amt} stamped on the front",
                         value=self.amt)

    def __repr__(self):
        return f"Gold ({self.amt})"
