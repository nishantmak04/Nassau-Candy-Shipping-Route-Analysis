# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

## Abstract
This project analyzes shipment records for Nassau Candy Distributor to identify route efficiency patterns, geographic bottlenecks, factory performance differences, regional behavior and shipping-mode characteristics. The analysis uses Python, Pandas and Plotly, with an interactive Streamlit dashboard for exploration.

## Dataset Overview
The analysis-ready dataset contains 10,194 shipment records, 196 unique factory-to-destination routes and five mapped factories. The mapped factories are Lot's O' Nuts, Wicked Choccy's, Secret Factory, The Other Factory and Sugar Shack.

## Methodology
1. Prepared and validated the shipment dataset.
2. Mapped products to their corresponding factories.
3. Calculated lead time in days from the supplied order and ship dates.
4. Aggregated performance by factory, route, state/province, region and ship mode.
5. Calculated route efficiency scores using normalized lead-time performance, where lower lead time receives a higher score.
6. Identified geographic bottlenecks using lead time and shipment volume.
7. Built an interactive Streamlit dashboard with filters and drill-down tables.

## Key Findings
- Lot's O' Nuts has the highest shipment volume at 5,692 shipments.
- Wicked Choccy's is the second-largest factory at 4,152 shipments.
- The fastest identified routes include Secret Factory to Nebraska and Secret Factory to New Mexico, both at about 906 days.
- Sugar Shack to New Jersey is among the least efficient identified routes, at about 1,642 days.
- California has the highest state shipment volume in the state summary, with 2,001 shipments.
- New York has 1,128 shipments and the highest bottleneck score in the supplied geographic bottleneck analysis.
- Standard Class is the largest shipping mode with 6,120 shipments and a default delay frequency of 46.83%.
- Gulf has the lowest average regional lead time among the four regions at 1,311.37 days.

## Recommendations
- Prioritize high-volume, high-lead-time states such as New York and Washington for route review.
- Review high-volume factory-to-state combinations before low-volume routes because improvements can affect more shipments.
- Compare carrier and fulfillment processes behind the slowest routes.
- Monitor Standard Class because it carries the largest shipment volume and the highest listed delay frequency.
- Establish recurring route-performance monitoring through the dashboard.

## Limitations and Data Validation
The supplied source dates produce unusually large lead-time values of approximately 904–1,642 days. These values are retained for analysis consistency with the supplied dataset. Before operational decisions are made, the source date fields and business definition of lead time should be validated.

## Tools
Python, Pandas, Plotly, Streamlit.

## Conclusion
The project provides a practical route-efficiency view of Nassau Candy shipments. The combination of route scoring, geographic bottleneck analysis and interactive dashboarding helps identify where logistics performance should be investigated first.
