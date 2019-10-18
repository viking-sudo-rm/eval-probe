class Entity:

    def __init__(self,
                 is_crying: bool = False,
                 is_running: bool = False):
        self.is_crying = is_crying
        self.is_running = is_running

        self.mother: Entity = None
        self.father: Entity = None

    def __hash__(self):
        """Hash this object by identity, not value.

        This is necessary if we want to add these objects to sets.
        """
        return id(self)


def null_escaped(predicate):
    """Make a predicate return None if any arguments are None."""
    def wrapped_predicate(*args):
        if any(arg is None for arg in args):
            return None
        else:
            return predicate(*args)
    return wrapped_predicate


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
    # TODO: Nouns should really be type entity -> truth_value.
    "mother": null_escaped(lambda x: x.mother),
    "father": null_escaped(lambda x: x.father),

    # Define intransitive verbs.
    "cry": null_escaped(lambda x: x.is_crying),
    "run": null_escaped(lambda x: x.is_running),

    # Define transitive verbs.
    "like": null_escaped(lambda x, y: (x, y) in like),
    "watch": null_escaped(lambda x, y: (x, y) in watch),

    # Define the copula.
    "is": null_escaped(lambda x, y: x == y),
}
