# %%
from fastfeatureflag.feature_flag import feature_flag


# %%
@feature_flag(activation="off", response="I responded")
def not_yet_finished_feature():
    return True


print(not_yet_finished_feature())


# %%
@feature_flag("on")
def not_yet_finished_feature():
    return True


not_yet_finished_feature()


# %%
@feature_flag("off", name="awesome_feature", response="Not finished yet")
def awesome_feature_1():
    return "I am feature 1"


@feature_flag(name="awesome_feature", response="Not finished yet")
def awesome_feature_2():
    return "I am feature 2"


awesome_feature_1()
awesome_feature_2()


# %%
@feature_flag("on", name="awesome_feature")
def awesome_feature_1():
    return "I am feature 1"


@feature_flag("off", name="awesome_feature")
def awesome_feature_2():
    return "I am feature 2"


awesome_feature_1()
awesome_feature_2()

# %%
