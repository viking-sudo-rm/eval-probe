class Entity:

    def __init__(self,
                 is_crying: bool = False,
                 is_running: bool = False):
        self.is_crying = is_crying
        self.is_running = is_running

        self.mother: Entity = None
        self.father: Entity = None

    def __hash__(self):
        """Hash this object by identity, not value."""
        return id(self)


john = Entity()
mary = Entity()
john.mother = mary


# Argument order is reversed here.
like = {(john, mary)}
watch = {(mary, john)}


model_dict = {
    # Define some entities.
    "john": john,
    "mary": mary,

    # Define nouns, which map entity -> entity.
    "mother": lambda x: x.mother,
    "father": lambda x: x.father,

    # Define intransitive verbs.
    "cry": lambda x: x.is_crying,
    "run": lambda x: x.is_running,

    # Define transitive verbs.
    "like": lambda x, y: (x, y) in like,
    "watch": lambda x, y: (x, y) in watch,

    # Define the copula.
    "is": lambda x, y: x == y,
}
