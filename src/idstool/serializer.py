
from pathlib import Path
from xml.etree import ElementTree as ET

from .ids_classes import *


class IDSSerializer:

    TranslatedType = ET.Element

    headers = {
        'xmlns:ids': "http://standards.buildingsmart.org/IDS",
        'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
        'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'xsi:schemaLocation': "http://standards.buildingsmart.org/IDS http://standards.buildingsmart.org/IDS/0.9.6/ids.xsd",
    }

    @classmethod
    def save_ids(cls, filepath: str | Path, ids: InformationDeliverySpecification) -> None:

        filepath = Path(filepath).with_suffix('.ids')
        
        ids_xml = cls.translate_ids(ids)
        ET.indent(ids_xml)
        ids_str = ET.tostring(ids_xml, encoding='utf-8')

        with open(filepath, mode='wb+') as file:
            file.write(b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
            file.write(ids_str)

    @classmethod
    def translate_ids(cls, ids: InformationDeliverySpecification) -> ET.Element:

        ids_root = ET.Element('ids:ids', attrib=cls.headers)

        # Info
        info_node = ET.SubElement(ids_root, 'ids:info')
        title_node = ET.SubElement(info_node, 'ids:title')
        title_node.text = ids.title

        if ids.copyright is not None:
            copyright = ET.SubElement(info_node, 'ids:copyright')
            copyright.text = ids.copyright

        if ids.version is not None:
            version = ET.SubElement(info_node, 'ids:version')
            version.text = ids.version

        if ids.description is not None:
            description = ET.SubElement(info_node, 'ids:description')
            description.text = ids.description

        # if ids.author is not None:
        #     author = ET.SubElement(info_node, 'ids:author')
        #     author.text = ids.author

        # if ids.date is not None:
        #     date = ET.SubElement(info_node, 'ids:date')
        #     date.text = ids.date

        if ids.purpose is not None:
            purpose = ET.SubElement(info_node, 'ids:purpose')
            purpose.text = ids.purpose

        if ids.milestone is not None:
            milestone = ET.SubElement(info_node, 'ids:milestone')
            milestone.text = ids.milestone

        # Specs
        specs_node = ET.SubElement(ids_root, 'ids:specifications')

        for spec in ids.specifications:
            spec_node = cls.translate_specification(spec)
            specs_node.append(spec_node)

        return ids_root

    @classmethod
    def translate_specification(cls, specification: Specification) -> ET.Element:

        spec_node = ET.Element('ids:specification', name=specification.name,
                               ifcVersion=specification.ifc_version)
        
        if specification.min_occurs == 0:
            spec_node.set('minOccurs', '0')
        elif specification.min_occurs == 1:
            spec_node.set('minOccurs', '1')
        else:
            raise ValueError(f'Illegal minOccurs for Specification {specification.min_occurs}')
        
        if specification.max_occurs == 0:
            spec_node.set('maxOccurs', '0')
        elif specification.max_occurs == 1:
            spec_node.set('maxOccurs', '1')
        elif specification.max_occurs == -1:
            spec_node.set('maxOccurs', 'unbounded')
        else:
            raise ValueError(f'Illegal maxOccurs for Specification {specification.min_occurs}')
        
        if specification.identifier is not None:
            spec_node.set('identifier', specification.identifier)

        if specification.description is not None:
            spec_node.set('description', specification.description)

        if specification.instructions is not None:
            spec_node.set('instructions', specification.instructions)

        appl = cls.translate_applicability(specification.applicability)
        spec_node.append(appl)

        req = cls.translate_requirement(specification.requirement)
        spec_node.append(req)

        if specification.requirement.description is not None:
            req_descr = specification.requirement.description
            req.set('description', req_descr)

        return spec_node

    @classmethod
    def translate_applicability(cls, applicability: Applicability) -> ET.Element:

        appl_node = ET.Element('ids:applicability')
        # Facets in Applicability are order-sensitive

        # 1 Entity Facets
        for facet in applicability.facets:
            if isinstance(facet, EntityFacet):
                facet_node = cls.translate_entity_facet(facet)
                appl_node.append(facet_node)
        
        # 2 PartOf Facets
        for facet in applicability.facets:
            if isinstance(facet, PartsFacet):
                facet_node = cls.translate_parts_facet(facet)
                appl_node.append(facet_node)
        
        # 3 Classification Facets
        for facet in applicability.facets:
            if isinstance(facet, ClassificationFacet):
                facet_node = cls.translate_classification_facet(facet)
                appl_node.append(facet_node)
        
        # 4 Attribute Facets
        for facet in applicability.facets:
            if isinstance(facet, AttributeFacet):
                facet_node = cls.translate_attribute_facet(facet)
                appl_node.append(facet_node)
        
        # 5 Property Facets
        for facet in applicability.facets:
            if isinstance(facet, PropertyFacet):
                facet_node = cls.translate_property_facet(facet)
                appl_node.append(facet_node)
        
        # 6 Material Facets
        for facet in applicability.facets:
            if isinstance(facet, MaterialFacet):
                facet_node = cls.translate_material_facet(facet)
                appl_node.append(facet_node)
        
        return appl_node

    @classmethod
    def translate_requirement(cls, requirement: Requirement) -> ET.Element:

        req_node = ET.Element('ids:requirements')

        for facet in requirement.facets:
            facet_node = cls.translate_facet(facet)
            req_node.append(facet_node)

            if facet.instructions is not None:
                facet_node.set('instructions', facet.instructions)
        
        return req_node

    @classmethod
    def translate_facet(cls, facet: Facet):
            
        match facet:
            case EntityFacet():
                value = cls.translate_entity_facet(facet)
            case AttributeFacet():
                value = cls.translate_attribute_facet(facet)
            case ClassificationFacet():
                value = cls.translate_classification_facet(facet)
            case PropertyFacet():
                value = cls.translate_property_facet(facet)
            case MaterialFacet():
                value = cls.translate_material_facet(facet)
            case PartsFacet():
                value = cls.translate_parts_facet(facet)
        
        return value

    @classmethod
    def translate_entity_facet(cls, facet: EntityFacet) -> ET.Element:
        
        entity_facet = ET.Element('ids:entity')

        name = ET.SubElement(entity_facet, 'ids:name')
        name_val = cls.translate_value(facet.ifc_class.upper())
        name.append(name_val)

        if facet.predefined_type is not None:
            predefined = ET.SubElement(entity_facet, 'ids:predefinedType')
            predefined_val = cls.translate_value(facet.predefined_type)
            predefined.append(predefined_val)
        
        return entity_facet

    @classmethod
    def translate_attribute_facet(cls, facet: AttributeFacet) -> ET.Element:
        
        attr_facet = ET.Element('ids:attribute')

        name = ET.SubElement(attr_facet, 'ids:name')
        name_val = cls.translate_value(facet.name)
        name.append(name_val)

        if facet.value is not None:
            value = ET.SubElement(attr_facet, 'ids:value')
            value_val = cls.translate_value(facet.value)
            value.append(value_val)
        
        return attr_facet

    @classmethod
    def translate_classification_facet(cls, facet: ClassificationFacet) -> ET.Element:

        class_facet = ET.Element('ids:classification')

        if facet.value is not None:
            value = ET.SubElement(class_facet, 'ids:value')
            value_val = cls.translate_value(facet.value)
            value.append(value_val)
        
        if facet.system is not None:
            system = ET.SubElement(class_facet, 'ids:system')
            system_val = cls.translate_value(facet.system)
            system.append(system_val)

        return class_facet

    @classmethod
    def translate_property_facet(cls, facet: PropertyFacet) -> ET.Element:
        
        property_facet = ET.Element('ids:property', datatype=facet.datatype)

        pset = ET.SubElement(property_facet, 'ids:propertySet')
        pset_val = cls.translate_value(facet.property_name)
        pset.append(pset_val)

        name = ET.SubElement(property_facet, 'ids:name')
        name_val = cls.translate_value(facet.property_set)
        name.append(name_val)

        if facet.value is not None:
            value = ET.SubElement(property_facet, 'ids:value')
            value_val = cls.translate_value(facet.value)
            value.append(value_val)

        return property_facet    

    @classmethod
    def translate_material_facet(cls, facet: MaterialFacet) -> ET.Element:
        
        material_facet = ET.Element('ids:material')

        if facet.value is not None:
            value = ET.SubElement(material_facet, 'ids:value')
            value_val = cls.translate_value(facet.value)
            value.append(value_val)

        return material_facet

    @classmethod
    def translate_parts_facet(cls, facet: PartsFacet) -> ET.Element:

        property_facet = ET.Element('ids:partOf')

        if facet.relationship is not None:
            property_facet.set('relation', facet.relationship)

        entity = ET.SubElement(property_facet, 'ids:entity')
        entity_val = cls.translate_value(facet.name)
        entity.append(entity_val)

        return property_facet

    @classmethod
    def translate_value(cls, value: str) -> ET.Element:

        element = ET.Element('ids:simpleValue')
        element.text = str(value)

        return element
