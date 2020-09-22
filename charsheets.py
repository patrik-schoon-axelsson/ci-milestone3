# This file contains the models for the document object, CharacterSheets for Dungeons & Dragons. It is kept separated in this file because of separations
# of concerns, as this is a complex data-object with multiple nested arrays and embedded dicts, it would quickly make app.py unreadable.

from flask_wtf import *
from user import User
from flask_mongoengine import MongoEngine, Document
from flask_mongoengine.wtf import model_form
from wtforms.fields import FormField
db = MongoEngine()

# 'Attributes' are a dict of ints that can range from 1 to 20. All characters have a set of Attributes within this range. This will be passed
# to a jQuery script that will then calculate required values based on these database posts. As those values can be modified so frequently
# and are calculated from the base-attribute value, it is preferable to defer the modifier to the FrontEnd to save on r/w operations.


class CharAttributes(db.EmbeddedDocument):
    strength = db.IntField(min_value=1, max_value=20)
    dexterity = db.IntField(min_value=1, max_value=20)
    constitution = db.IntField(min_value=1, max_value=20)
    intelligence = db.IntField(min_value=1, max_value=20)
    wisdom = db.IntField(min_value=1, max_value=20)
    charisma = db.IntField(min_value=1, max_value=20)

# Saves is a list of booleans, represented in HTML as checkboxes. A save in the context of the rules is either true or false. If true, it adds a bonus based on
# proficiency modifier. As the modifier is calculated on the front-end, the database need only pass True or False to the front-end.


class Saves(db.EmbeddedDocument):
    StrSave = db.BooleanField()
    DexSave = db.BooleanField()
    ConSave = db.BooleanField()
    IntSave = db.BooleanField()
    WisSave = db.BooleanField()
    ChaSave = db.BooleanField()

# 'Skills' is a boolean list, represented in HTML as checkboxes. All characters use the list of skills, so it is a separate embedded document like attributes.
# The user will mark a number of skills as 'proficient' and when the data is passed to the front-end, values will be generated using jQuery
# to accurately calculate the exact numeric value based on proficiency. As this number can value based on modifiers, it is not worth writing exact
# numbers into the DB there, you can get accurate data for our purposes knowing just if it is proficient or not.


class Skills(db.EmbeddedDocument):
    Athletics = db.BooleanField()
    Acrobatics = db.BooleanField()
    Sleight = db.BooleanField()
    Stealth = db.BooleanField()
    Arcana = db.BooleanField()
    History = db.BooleanField()
    Investigation = db.BooleanField()
    Nature = db.BooleanField()
    Religion = db.BooleanField()
    AnimalHandling = db.BooleanField()
    Insight = db.BooleanField()
    Medicine = db.BooleanField()
    Perception = db.BooleanField()
    Survival = db.BooleanField()
    Deception = db.BooleanField()
    Intimidation = db.BooleanField()
    Performance = db.BooleanField()
    Persuasion = db.BooleanField()

# 'Armor' at its core represents an integer that theoretically has neither a maximum nor minimum value. However, numerous
# factors can alter armor-class and it is feasible for a user to want to save multiple 'Armor' objects to represent
# different equipment in a game. Therefore, Armor will be accessible through a EmbeddedDocument
# Field of multiple armor-items in
# the DB, which user can add, update or remove from at will. Some of the more basic rules are incorporated for ease-of-use
# in the form of the required boolean-fields.


class Armor(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    ACValue = db.IntField()
    HeavyArmor = db.BooleanField()
    MediumArmor = db.BooleanField()
    LightArmor = db.BooleanField()
    Shield = db.BooleanField()

# A list of Armor objects, that can be managed by the document owner.


class ArmorObjs(db.EmbeddedDocument):
    ArmorList = db.EmbeddedDocumentField(Armor)

# 'Attacks', much like Armor, are a class of what is essentially a collection of ints. An attack roll is a randomized number
# adding the modifier, the modifier being calculated client-side on the front-end, the object needs only save name, description, dice-type
# and defer all other math operations to the JavaScript component.


class Attacks(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DmgDie = db.IntField()


class AttackObjs(db.EmbeddedDocument):
    AttacksList = db.EmbeddedDocumentField(Attacks)

# The ClassObj contains name, description and level as well as an embedded list-item classes as "Ability", a catch-all term for character-abilities
# that the user must specify and keep updated themselves. Proficiency is a function of level/4 +1 (Rounded up) and is thus referred to the front-end which handles
# derived stats.


class Abilities(db.EmbeddedDocument):
    Name = db.StringField()
    Description = db.StringField()
    DieType = db.IntField()
    Attribute = db.EmbeddedDocumentField(CharAttributes)


class ClassObj(db.EmbeddedDocument):
    Name = db.StringField()
    Subclass = db.StringField()
    CharClass = db.StringField()
    Abilities = db.EmbeddedDocumentField('Abilities')


class AbilityObjs(db.EmbeddedDocument):
    AbilityList = db.EmbeddedDocumentField(Abilities)

# Finally, the char object contains StringFields for name, description, looks, an int-field for level and references to all other documents to embed.


class Char(db.Document):
    Name = db.StringField()
    CharClass = db.StringField()
    Subclass = db.StringField()
    Appearance = db.StringField()
    Description = db.StringField()
    ClassObjList = db.EmbeddedDocumentField(ClassObj)
    AttributeList = db.EmbeddedDocumentField(CharAttributes)
    SavesList = db.EmbeddedDocumentField(Saves)
    SkillsList = db.EmbeddedDocumentField(Skills)
    ArmorObjList = db.EmbeddedDocumentField(ArmorObjs)
    AttacksList = db.EmbeddedDocumentField(Attacks)
    AbilityObjsList = db.EmbeddedDocumentField(AbilityObjs)
    owner = db.ReferenceField(User)
