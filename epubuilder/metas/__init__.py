# coding=utf-8

from .dcmes import Identifier, Language, Title
from .dcmes import Contributor, Coverage, Creator, Date, Description, Format, Publisher, Relation, Rights
from .dcmes import Source, Subject, Type

from .dcterms import get_dcterm

from .epub3_only import Meta3

from .epub2_only import Meta2, Cover
