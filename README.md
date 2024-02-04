# idstool
 Python Tool to create IDS (Information delivery specification) files for openBIM workflows.

 Currently built on IDS version 0.9.6


# Example

An example on how to use this library to create an IDS:

```python
import idstool as ids

spec1 = ids.Specification(name='Wall Specifications', ifc_version='IFC4',
                          applicability=ids.Applicability(facets=[ids.EntityFacet(ifc_class='IfcWall')]),
                          requirement=ids.Requirement(facets=[ids.AttributeFacet(name='Name')]))

spec2 = ids.Specification(name='Hackathon Pset', ifc_version='IFC4',
                          applicability=ids.Applicability(facets=[ids.EntityFacet(ifc_class='IfcWall')]),
                          requirement=ids.Requirement(facets=[ids.PropertyFacet(property_set='Hackathon2024', property_name='AEC_Hack', datatype='IFCTEXT')]))

ids_data = ids.InformationDeliverySpecification(
    title="AEC Hackathon Test IDS",
    version="0.1",
    purpose="Testing",
    specifications=[spec1, spec3]
)

ids.IDSSerializer.save_ids(filepath='example_ids', ids=ids_data)
```


# Limitations

- This README is still under construction =)
- Currently not all metadata for IDS files are actually written to file. author and date are skipped

# Next Steps

The following features will be added next:

- Utility functions to easily create simple Applicabilities and Requirements

