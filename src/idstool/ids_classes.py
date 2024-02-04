from dataclasses import dataclass
from typing import Optional, Any


class Facet:
    pass


@dataclass
class EntityFacet(Facet):
    ifc_class: str
    predefined_type: Optional[str] = None
    instructions: Optional[str] = None


@dataclass
class AttributeFacet(Facet):
    name: str
    value: Optional[Any] = None
    instructions: Optional[str] = None


@dataclass
class ClassificationFacet(Facet):
    system: Optional[str] = None
    value: Optional[Any] = None
    instructions: Optional[str] = None


@dataclass
class PropertyFacet(Facet):
    property_set: str
    property_name: str
    datatype: str
    value: Optional[str] = None
    instructions: Optional[str] = None


@dataclass
class MaterialFacet(Facet):
    value: Optional[str] = None
    instructions: Optional[str] = None


@dataclass
class PartsFacet(Facet):
    entity: str
    relationship: Optional[Any] = None
    instructions: Optional[str] = None

    def __post_init__(cls):

        relation = cls.relationship.upper()
        cls.relationship = relation

        allowed_relations = {'IFCRELAGGREGATES', 'IFCRELASSIGNSTOGROUP', 
                             'IFCRELCONTAINEDINSPATIALSTRUCTURE',
                             'IFCRELNESTS', 'IFCRELVOIDSELEMENT',
                             'IFCRELFILLSELEMENT'}

        if relation is not None and relation not in allowed_relations:
            raise ValueError(f'Illegal relation {relation}')


@dataclass
class SpecificationPart:
    facets: list[Facet]

    def __post_init__(cls):

        num_entity = sum([isinstance(f, EntityFacet) for f in cls.facets])
        num_material = sum([isinstance(f, MaterialFacet) for f in cls.facets])

        if num_entity > 1:
            raise ValueError("Only 1 EntityFacet allowed!")

        if num_material > 1:
            raise ValueError("Only 1 MaterialFacet allowed!")


@dataclass
class Applicability(SpecificationPart):
    pass


@dataclass
class Requirement(SpecificationPart):
    description: Optional[str] = None


@dataclass
class Specification:
    applicability: Applicability
    requirement: Requirement

    name: str
    ifc_version: str
    identifier: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    min_occurs: int = 0
    max_occurs: int = -1

    def __post_init__(cls):

        ifc_version = cls.ifc_version.upper()
        cls.ifc_version = ifc_version

        allowed_ifc_version = {'IFC2X3', 'IFC4', 'IFC4X3'}

        if ifc_version not in allowed_ifc_version:
            raise ValueError(f'Illegal IFC version {ifc_version}')


@dataclass
class InformationDeliverySpecification:
    title: str
    copyright: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    purpose: Optional[str] = None
    milestone: Optional[str] = None

    specifications: list[Specification] = ()
