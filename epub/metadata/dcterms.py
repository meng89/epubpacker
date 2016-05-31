"""Dublin Core Metadata Initiative"""

from .dcmes import _Meta


def always_true():
    pass


def w3c_date(string):
    return True


l = [
    'abstract', 'accessRights', 'accrualMethod', 'accrualPeriodicity', 'accrualPolicy', 'alternative', 'audience',
    'available',
    'bibliographicCitation',
    'conformsTo', 'contributor', 'coverage', 'created', 'creator',
    'date', 'dateAccepted', 'dateCopyrighted', 'dateSubmitted', 'description',
    'educationLevel', 'extent',
    'format',
    'hasFormat', 'hasPart', 'hasVersion',
    'identifier', 'instructionalMethod',
    'isFormatOf', 'isPartOf', 'isReferencedBy', 'isReplacedBy', 'isRequiredBy', 'issued', 'isVersionOf',
    'language', 'license',
    'mediator', 'medium', 'modified',
    'provenance', 'publisher',
    'references', 'relation', 'replaces', 'requires', 'rights', 'rightsHolder',
    'source', 'spatial', 'subject',
    'tableOfContents', 'temporal', 'title', 'type',
    'valid'
]


check_funcs = {
    'modified': w3c_date,
}


check_funcs.update(dict((one, always_true) for one in l if one not in check_funcs.keys()))


_classes = {}


class _MyMeta:
    def element(self):
        pass


for k, v in check_funcs.items():
    _class = type(k, (), {'check_func': v})
    _classes[k] = _class


def get_class(name):
    return _classes[name]
